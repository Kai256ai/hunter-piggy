"""Transparent first-pass signal extraction.

The router detects markers. It never treats a marker as proof or a verdict.
"""

from __future__ import annotations

import re

from .models import Signal


class SignalRouter:
    TERMS = {
        "procedure": ("committee", "referral", "procedure", "review", "approval", "administrative"),
        "structure": ("department", "agency", "board", "authority", "organisation", "organization"),
        "culture": ("legitimate", "priority", "efficient", "normal practice", "obligation"),
        "fiscal": ("budget", "cost", "funding", "allocation", "financial", "resources"),
        "jurisdiction": ("jurisdiction", "responsibility", "mandate", "transfer", "competence"),
        "temporal": ("delay", "temporary", "provisional", "deadline", "years", "months", "sequence"),
    }

    def analyze(self, text: str) -> tuple[Signal, ...]:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Input must be non-empty text")
        lowered = re.sub(r"\s+", " ", text.lower())
        signals: list[Signal] = []
        for category, terms in self.TERMS.items():
            hits = tuple(term for term in terms if term in lowered)
            if hits:
                confidence = min(0.92, 0.5 + 0.08 * len(hits))
                signals.append(Signal(
                    name=f"{category}_marker",
                    category=category,
                    strength=min(1.0, 0.3 + 0.12 * len(hits)),
                    confidence=confidence,
                    explanation=f"Observed terms: {', '.join(hits)}. Marker only; human review required.",
                ))
        return tuple(signals)

