"""Runnable institutional-sequence demo."""

import json

from .pipeline import HunterPiggyPipeline


SAMPLE = """
A temporary committee review delayed the referral for several months. Budget
screening reduced resources, while responsibility was transferred between two
agencies. The provisional administrative arrangement became normal practice.
"""


def main() -> None:
    result = HunterPiggyPipeline().analyze(SAMPLE)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

