"""End-to-end HunterPiggy pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .models import AnalysisResult, PICLever, Signal
from .pic_boson import PICBosonAdapter
from .signal_router import SignalRouter
from .trajectory import CairoResonanceTrajectoryEngine
from .threat_router import ThreatAssessment, ThreatSignalRouter


@dataclass(frozen=True)
class PipelineResult:
    threat_assessment: ThreatAssessment
    signals: tuple[Signal, ...]
    pic_levers: tuple[PICLever, ...]
    trajectory: AnalysisResult

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class HunterPiggyPipeline:
    def __init__(self) -> None:
        self.router = SignalRouter()
        self.threat_router = ThreatSignalRouter()
        self.adapter = PICBosonAdapter()
        self.engine = CairoResonanceTrajectoryEngine()

    def analyze(self, text: str, question: str = "Which mechanisms shape this institutional outcome?") -> PipelineResult:
        threat_assessment = self.threat_router.analyze(text)
        signals = self.router.analyze(text)
        levers = self.adapter.transform(signals)
        trajectory = self.engine.analyze(question, levers)
        return PipelineResult(threat_assessment, signals, levers, trajectory)
