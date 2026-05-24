from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()
    print({"dataset": args.dataset, "metric": "nDCG@5", "status": "template"})


if __name__ == "__main__":
    main()
