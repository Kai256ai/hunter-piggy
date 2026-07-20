"""Shared, serializable data structures."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Signal:
    name: str
    category: str
    strength: float
    confidence: float
    explanation: str


@dataclass(frozen=True)
class PICLever:
    code: str
    name: str
    boson: str
    value: float
    confidence: float
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class Trajectory:
    name: str
    steps: tuple[float, ...]
    probability: float
    turning_points: tuple[int, ...] = ()


@dataclass(frozen=True)
class AnalysisResult:
    question: str
    dominant_trajectory: str
    growth: Trajectory
    shadow: Trajectory
    key_levers: tuple[str, ...]
    counter_hypotheses: tuple[str, ...]
    anti_loop_detected: bool
    confidence: float
    audit: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

