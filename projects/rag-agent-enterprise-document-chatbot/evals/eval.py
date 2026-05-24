from __future__ import annotations

GOLDEN_TASKS = [
    "Explain the workflow state.",
    "List likely failure modes.",
    "Recommend observability signals.",
]


def main() -> None:
    for task in GOLDEN_TASKS:
        print({"task": task, "status": "pending-human-review"})


if __name__ == "__main__":
    main()
