"""Deterministic causal trajectory simulation inspired by Cairo v2.0."""

from __future__ import annotations

import math
import random

from .models import AnalysisResult, PICLever, Trajectory


class CairoResonanceTrajectoryEngine:
    """Simulate growth/shadow paths without classifying people.

    The engine analyses system levers. A fixed seed makes demonstrations and
    tests reproducible; uncertainty is represented through bounded sampling.
    """

    def __init__(self, *, iterations: int = 240, steps: int = 10, seed: int = 1448):
        if iterations < 1 or steps < 2:
            raise ValueError("iterations must be positive and steps must be at least 2")
        self.iterations = iterations
        self.steps = steps
        self.seed = seed
        self._history: list[tuple[float, float]] = []

    @staticmethod
    def _turning_points(values: list[float]) -> tuple[int, ...]:
        return tuple(i for i in range(1, len(values) - 1)
                     if (values[i] - values[i - 1]) * (values[i + 1] - values[i]) < 0)

    def analyze(self, question: str, levers: tuple[PICLever, ...]) -> AnalysisResult:
        if not levers:
            neutral = Trajectory("neutral", tuple(0.5 for _ in range(self.steps + 1)), 0.5)
            return AnalysisResult(question, "undetermined", neutral, neutral, (),
                                  ("No PIC lever was detected.",), False, 0.5,
                                  ("No inference made from absent signals.",))

        rng = random.Random(self.seed)
        growth_runs: list[list[float]] = []
        shadow_runs: list[list[float]] = []
        temporal = next((x.value for x in levers if x.code == "PIC-T"), 0.0)
        resource = next((x.value for x in levers if x.code == "PIC-F"), 0.0)
        responsibility = next((x.value for x in levers if x.code == "PIC-J"), 0.0)
        base = sum(x.value for x in levers) / len(levers)

        for _ in range(self.iterations):
            growth, shadow = 0.5, 0.5
            g_steps, s_steps = [growth], [shadow]
            for step in range(1, self.steps + 1):
                noise = rng.uniform(-0.035, 0.035)
                compounding = temporal * (step / self.steps)
                shadow_force = base + 0.30 * resource + 0.35 * responsibility + 0.45 * compounding
                # Missing/weak pressure is not automatically evidence of a
                # protective mechanism. Keep the baseline conservative and
                # expose protective evidence explicitly in later adapters.
                protective_force = 0.28 + 0.22 * max(0.0, 1.0 - base)
                shadow = min(1.0, max(0.0, shadow + math.tanh(shadow_force - protective_force + noise) * 0.12))
                growth = min(1.0, max(0.0, growth + math.tanh(protective_force - shadow_force - noise) * 0.12))
                g_steps.append(growth)
                s_steps.append(shadow)
            growth_runs.append(g_steps)
            shadow_runs.append(s_steps)

        growth_avg = [sum(run[i] for run in growth_runs) / self.iterations for i in range(self.steps + 1)]
        shadow_avg = [sum(run[i] for run in shadow_runs) / self.iterations for i in range(self.steps + 1)]
        total = growth_avg[-1] + shadow_avg[-1] or 1.0
        growth_p, shadow_p = growth_avg[-1] / total, shadow_avg[-1] / total
        snapshot = (round(growth_p, 4), round(shadow_p, 4))
        self._history.append(snapshot)
        anti_loop = len(self._history) >= 3 and len(set(self._history[-3:])) == 1
        ranked = tuple(x.code for x in sorted(levers, key=lambda x: x.value, reverse=True))
        confidence = sum(x.confidence for x in levers) / len(levers)

        return AnalysisResult(
            question=question,
            dominant_trajectory="shadow" if shadow_p > growth_p else "growth",
            growth=Trajectory("growth", tuple(round(x, 4) for x in growth_avg), round(growth_p, 4), self._turning_points(growth_avg)),
            shadow=Trajectory("shadow", tuple(round(x, 4) for x in shadow_avg), round(shadow_p, 4), self._turning_points(shadow_avg)),
            key_levers=ranked,
            counter_hypotheses=(
                "The apparent sequence may reflect reverse causality.",
                "A missing institutional variable may explain the outcome.",
                "The observed markers may depend on measurement or document framing.",
                "An intervention test is required before treating a lever as causal.",
            ),
            anti_loop_detected=anti_loop,
            confidence=round(confidence, 4),
            audit=(
                "Analysed submitted text only.",
                "Markers were mapped to PIC levers; they were not treated as proof.",
                "Simulation is deterministic for the configured seed.",
                "Human review is required before action.",
            ),
        )
