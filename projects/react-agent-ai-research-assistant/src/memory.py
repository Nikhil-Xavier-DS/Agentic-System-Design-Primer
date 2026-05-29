from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class MemoryRecord:
    id: int
    kind: str
    key: str
    value: str
    score: int


class SQLiteResearchMemory:
    """Durable memory and storage for ReAct research runs.

    This intentionally uses SQLite so the project remains local-first and easy
    to run, while still modeling production concerns: durable run history,
    observations, source provenance, and reusable semantic-ish notes.
    """

    def __init__(self, database_path: Path):
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def create_run(self, task: str, metadata: dict[str, str]) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO research_runs(task, metadata_json, created_at)
                VALUES (?, ?, ?)
                """,
                (task, json.dumps(metadata, sort_keys=True), _utc_now()),
            )
            return int(cursor.lastrowid)

    def save_step(
        self,
        run_id: int,
        step_number: int,
        thought: str,
        action: str,
        action_input: str,
        observation: str,
        sources: list[str],
    ) -> None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO research_steps(
                    run_id, step_number, thought, action, action_input, observation, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (run_id, step_number, thought, action, action_input, observation, _utc_now()),
            )
            step_id = int(cursor.lastrowid)
            connection.executemany(
                """
                INSERT INTO research_sources(step_id, source)
                VALUES (?, ?)
                """,
                [(step_id, source) for source in sources],
            )

    def save_final_answer(self, run_id: int, answer: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE research_runs
                SET final_answer = ?, completed_at = ?
                WHERE id = ?
                """,
                (answer, _utc_now(), run_id),
            )

    def remember(self, kind: str, key: str, value: str, source: str | None = None) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO memories(kind, key, value, source, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(kind, key)
                DO UPDATE SET value = excluded.value, source = excluded.source, updated_at = excluded.updated_at
                """,
                (kind, key, value, source, _utc_now(), _utc_now()),
            )

    def search_memories(self, query: str, limit: int = 5) -> list[MemoryRecord]:
        terms = set(_tokenize(query))
        if not terms:
            return []
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, kind, key, value
                FROM memories
                ORDER BY updated_at DESC
                LIMIT 100
                """
            ).fetchall()
        scored: list[MemoryRecord] = []
        for row in rows:
            text = f"{row['kind']} {row['key']} {row['value']}"
            score = len(terms.intersection(_tokenize(text)))
            if score:
                scored.append(
                    MemoryRecord(
                        id=int(row["id"]),
                        kind=str(row["kind"]),
                        key=str(row["key"]),
                        value=str(row["value"]),
                        score=score,
                    )
                )
        scored.sort(key=lambda record: record.score, reverse=True)
        return scored[:limit]

    def recent_runs(self, limit: int = 5) -> list[dict[str, str]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, task, final_answer, created_at, completed_at
                FROM research_runs
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS research_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    final_answer TEXT,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                );

                CREATE TABLE IF NOT EXISTS research_steps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL REFERENCES research_runs(id),
                    step_number INTEGER NOT NULL,
                    thought TEXT NOT NULL,
                    action TEXT NOT NULL,
                    action_input TEXT NOT NULL,
                    observation TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS research_sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    step_id INTEGER NOT NULL REFERENCES research_steps(id),
                    source TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kind TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    source TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(kind, key)
                );

                CREATE INDEX IF NOT EXISTS idx_research_steps_run_id
                ON research_steps(run_id);

                CREATE INDEX IF NOT EXISTS idx_memories_kind_key
                ON memories(kind, key);
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _tokenize(text: str) -> list[str]:
    return [token for token in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split()]
