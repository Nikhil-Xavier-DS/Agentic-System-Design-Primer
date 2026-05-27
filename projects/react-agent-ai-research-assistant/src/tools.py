from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


@dataclass(frozen=True)
class ToolResult:
    tool: str
    query: str
    content: str
    sources: list[str]


class ResearchTool:
    name: str
    description: str

    def run(self, query: str) -> ToolResult:
        raise NotImplementedError


class LocalKnowledgeTool(ResearchTool):
    name = "local_knowledge_search"
    description = "Searches a curated local knowledge base for agent architecture facts."

    def __init__(self, corpus_path: Path):
        self.corpus_path = corpus_path
        self.documents = self._load_documents()

    def run(self, query: str) -> ToolResult:
        query_terms = set(_tokenize(query))
        ranked: list[tuple[int, dict[str, str]]] = []
        for document in self.documents:
            text = f"{document['title']} {document['content']}"
            score = len(query_terms.intersection(_tokenize(text)))
            if score:
                ranked.append((score, document))
        ranked.sort(key=lambda item: item[0], reverse=True)
        selected = [document for _, document in ranked[:3]] or self.documents[:2]
        content = "\n\n".join(
            f"{document['title']}: {document['content']}" for document in selected
        )
        return ToolResult(
            tool=self.name,
            query=query,
            content=content,
            sources=[document["source"] for document in selected],
        )

    def _load_documents(self) -> list[dict[str, str]]:
        with self.corpus_path.open(encoding="utf-8") as file:
            return [json.loads(line) for line in file if line.strip()]


class WebSearchTool(ResearchTool):
    name = "web_search"
    description = "Searches the public web through DuckDuckGo's lightweight HTML endpoint."

    def __init__(self, timeout_seconds: float = 10.0):
        self.timeout_seconds = timeout_seconds

    def run(self, query: str) -> ToolResult:
        encoded = urllib.parse.urlencode({"q": query})
        url = f"https://duckduckgo.com/html/?{encoded}"
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "production-agent-engineering/0.1 research-assistant",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                html = response.read().decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001 - tool results should surface operational failure
            return ToolResult(
                tool=self.name,
                query=query,
                content=f"Web search failed: {exc}",
                sources=[],
            )

        parser = DuckDuckGoHTMLParser()
        parser.feed(html)
        results = parser.results[:5]
        if not results:
            return ToolResult(
                tool=self.name,
                query=query,
                content="Web search returned no parseable results.",
                sources=[],
            )
        content = "\n".join(f"- {title}: {href}" for title, href in results)
        return ToolResult(
            tool=self.name,
            query=query,
            content=content,
            sources=[href for _, href in results],
        )


class DuckDuckGoHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[tuple[str, str]] = []
        self._capture_title = False
        self._current_href: str | None = None
        self._title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = attributes.get("class", "")
        if tag == "a" and "result__a" in classes:
            self._capture_title = True
            self._current_href = attributes.get("href")
            self._title_parts = []

    def handle_data(self, data: str) -> None:
        if self._capture_title:
            self._title_parts.append(data.strip())

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._capture_title:
            title = " ".join(part for part in self._title_parts if part)
            href = _normalize_duckduckgo_href(self._current_href or "")
            if title and href:
                self.results.append((title, href))
            self._capture_title = False
            self._current_href = None
            self._title_parts = []


def _normalize_duckduckgo_href(href: str) -> str:
    if not href:
        return ""
    parsed = urllib.parse.urlparse(href)
    query = urllib.parse.parse_qs(parsed.query)
    if "uddg" in query:
        return query["uddg"][0]
    return href


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())
