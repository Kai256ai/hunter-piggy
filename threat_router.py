"""Explainable scam, manipulation, and anomaly signal router."""

from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any
from urllib.parse import urlparse


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT_REVIEW = "URGENT_REVIEW"


@dataclass(frozen=True)
class ThreatSignal:
    name: str
    category: str
    weight: int
    confidence: float
    explanation: str
    source: str = "transparent_heuristic"


@dataclass(frozen=True)
class Correlation:
    reason: str
    bonus: int
    signals: tuple[str, ...]


@dataclass(frozen=True)
class ThreatAssessment:
    risk_score: int
    risk_level: RiskLevel
    confidence: float
    signals: tuple[ThreatSignal, ...]
    correlations: tuple[Correlation, ...]
    entropy: float
    human_review_recommended: bool
    limitations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["risk_level"] = self.risk_level.value
        return data


class ThreatSignalRouter:
    """Detect markers of scam/manipulation without issuing a verdict."""

    SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "cutt.ly", "ow.ly", "is.gd"}
    PHRASES = {
        "urgent", "act now", "last chance", "account suspended", "verify your identity",
        "you won", "claim your prize", "click here", "payment required",
        "pilne", "natychmiast", "ostatnia szansa", "zablokowane konto",
        "potwierdź tożsamość", "wygrałeś", "odbierz nagrodę", "kliknij tutaj",
        "zweryfikuj dane", "dopłata", "przesyłka zatrzymana",
    }
    SENSITIVE = {"child", "children", "safety", "abuse", "harm", "threat",
                 "dziecko", "dzieci", "bezpieczeństwo", "przemoc", "groźba"}
    FLAGGED_DOMAINS = {"phishing-site.com", "fake-login.xyz", "scam-bank.co"}

    @staticmethod
    def _urls(text: str) -> tuple[str, ...]:
        return tuple(re.findall(r"https?://[^\s<>\]\)\"']+", text, flags=re.I))

    @staticmethod
    def _domain(url: str) -> str:
        return (urlparse(url).netloc or "").lower().split(":")[0]

    @staticmethod
    def _entropy(text: str) -> float:
        if not text:
            return 0.0
        counts: dict[str, int] = {}
        for char in text:
            if char.isprintable():
                counts[char] = counts.get(char, 0) + 1
        total = sum(counts.values())
        return -sum((n / total) * math.log2(n / total) for n in counts.values()) if total else 0.0

    def analyze(self, text: str) -> ThreatAssessment:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Input must be non-empty text")
        if len(text) > 20_000:
            raise ValueError("Input exceeds 20,000 characters")

        lowered = re.sub(r"\s+", " ", text.lower())
        urls = self._urls(text)
        signals: list[ThreatSignal] = []

        shorteners = sorted({self._domain(url) for url in urls} & self.SHORTENERS)
        if shorteners:
            signals.append(ThreatSignal("url_shortener", "technical", 18, 0.76,
                                        f"Known shortener: {shorteners[0]}."))

        if any(any(token in url.lower() for token in ("login", "verify", "confirm", "reset", "secure")) for url in urls):
            signals.append(ThreatSignal("credential_url_pattern", "technical", 20, 0.70,
                                        "URL contains credential or verification wording."))

        phrases = sorted(phrase for phrase in self.PHRASES if phrase in lowered)
        if phrases:
            signals.append(ThreatSignal("manipulative_language", "linguistic", 28,
                                        min(0.90, 0.62 + 0.06 * len(phrases)),
                                        f"Observed pressure/scam phrases: {', '.join(phrases[:5])}."))

        sensitive = sorted(term for term in self.SENSITIVE if term in lowered)
        if sensitive:
            signals.append(ThreatSignal("sensitive_context", "context", 8, 0.55,
                                        "Sensitive context detected; weak signal alone."))

        flagged = sorted({self._domain(url) for url in urls} & self.FLAGGED_DOMAINS)
        if flagged:
            signals.append(ThreatSignal("flagged_domain", "reputation", 42, 0.88,
                                        f"Domain occurs in configured demo reputation data: {flagged[0]}.",
                                        "demo_reputation_list"))

        if re.search(r"\b[\w.%+-]+\s*(?:\[at\]|\(at\)|\sat\s)\s*[\w.-]+\s*(?:\[dot\]|\(dot\)|\sdot\s)\s*[a-z]{2,}\b", lowered):
            signals.append(ThreatSignal("email_obfuscation", "technical", 12, 0.72,
                                        "Observed an obfuscated email pattern."))

        entropy = self._entropy(text)
        if entropy > 4.8 and len(text) > 80:
            signals.append(ThreatSignal("high_entropy_structure", "structural", 14, 0.62,
                                        f"High character entropy ({entropy:.2f}); weak signal alone."))

        if re.search(r"!{3,}|\?{3,}", text):
            signals.append(ThreatSignal("urgency_formatting", "linguistic", 10, 0.60,
                                        "Excessive urgency punctuation observed."))

        names = {signal.name for signal in signals}
        correlations: list[Correlation] = []
        if {"manipulative_language", "url_shortener"}.issubset(names):
            correlations.append(Correlation("Pressure language appears with a shortened URL.", 14,
                                            ("manipulative_language", "url_shortener")))
        if {"manipulative_language", "credential_url_pattern"}.issubset(names):
            correlations.append(Correlation("Pressure language appears with verification-style URL wording.", 18,
                                            ("manipulative_language", "credential_url_pattern")))
        if {"flagged_domain", "manipulative_language"}.issubset(names):
            correlations.append(Correlation("Configured flagged domain appears with pressure language.", 22,
                                            ("flagged_domain", "manipulative_language")))

        raw = sum(signal.weight * signal.confidence for signal in signals) + sum(x.bonus for x in correlations)
        score = min(100, round(raw))
        confidence = (sum(x.confidence for x in signals) / len(signals)) if signals else 0.5
        confidence = round(min(0.95, confidence + min(0.12, 0.02 * len(signals))), 3)
        if score >= 82 and confidence >= 0.70:
            level = RiskLevel.URGENT_REVIEW
        elif score >= 62 and confidence >= 0.62:
            level = RiskLevel.HIGH
        elif score >= 32 and confidence >= 0.55:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        return ThreatAssessment(
            risk_score=score,
            risk_level=level,
            confidence=confidence,
            signals=tuple(signals),
            correlations=tuple(correlations),
            entropy=round(entropy, 3),
            human_review_recommended=level != RiskLevel.LOW,
            limitations=(
                "Markers are not proof of fraud, manipulation, or wrongdoing.",
                "The reputation list is demo data, not a live external feed.",
                "False positives and false negatives are expected.",
                "Human review is required before consequential action.",
            ),
        )
