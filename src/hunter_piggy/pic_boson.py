"""Adapter between Ian Tasker's PIC framework and HunterPiggy trajectories.

PIC attribution: Political–Institutional Contingency framework, Ian Tasker.
Boson mappings and computational adapter: Anna Kai / FreeIntelligence.Institute.
Used with the framework author's permission.
"""

from __future__ import annotations

from .models import PICLever, Signal


class PICBosonAdapter:
    MAP = {
        "structure": ("PIC-S", "Structural Design", "Structural Boson"),
        "culture": ("PIC-C", "Cultural Norms", "Resonance Boson"),
        "procedure": ("PIC-P", "Procedural Action", "Procedure Boson"),
        "fiscal": ("PIC-F", "Fiscal Prioritisation", "Resource Boson"),
        "jurisdiction": ("PIC-J", "Jurisdictional Boundary-Setting", "Responsibility Boson"),
        "temporal": ("PIC-T", "Temporal Constraint", "Temporal / Anti-Loop Boson"),
    }

    def transform(self, signals: tuple[Signal, ...]) -> tuple[PICLever, ...]:
        levers: list[PICLever] = []
        for signal in signals:
            mapping = self.MAP.get(signal.category)
            if mapping is None:
                continue
            code, name, boson = mapping
            levers.append(PICLever(
                code=code,
                name=name,
                boson=boson,
                value=round(signal.strength * signal.confidence, 4),
                confidence=signal.confidence,
                evidence=(signal.explanation,),
            ))
        return tuple(levers)

