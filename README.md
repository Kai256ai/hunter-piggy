# HunterPiggy

**Detect the signal. Reconstruct the mechanism. Do not issue a verdict.**

HunterPiggy is an explainable detection and signal-to-trajectory engine. Its
core identifies correlated markers of scams, manipulation, suspicious links,
obfuscation, sensitive contexts, and structural anomalies. Its optional
PIC–Boson layer then reconstructs how administrative and institutional
mechanisms may interact and become durable over time. It analyses signals and
systems, not people.

## Why it exists

Scam filters often match one suspicious word and stop at classification.
Institutional audits often inspect the final outcome while losing the sequence
that produced it. HunterPiggy asks two connected questions:

> Which signals are present, how do they correlate, and what sequence of
> mechanisms could have produced the outcome?

Every result preserves uncertainty, offers counter-hypotheses, and requires
human review. A marker is an entry point for investigation, not evidence of
wrongdoing.

## Build Week contribution

### Before OpenAI Build Week

HunterPiggy existed inside the broader Python Zero / Kai256 research system as
a transparent scam, manipulation, and anomaly signal router. It detected URL,
linguistic, structural, context, and reputation markers; applied correlation
boosts; prioritised review; and explicitly avoided automated accusations. It
did not yet reconstruct institutional trajectories.

### Built during OpenAI Build Week (13–21 July 2026)

- **19 July:** Cairo Resonance Trajectory Engine v2 was introduced as a causal
  graph and trajectory concept.
- The prototype was extracted from the monolithic Python Zero system into this
  independently installable repository.
- The trajectory implementation was repaired so time steps use evolving state
  rather than repeated final-state values.
- Seeded bounded simulation was added for reproducible demos and tests.
- Ian Tasker's Political–Institutional Contingency (PIC) framework was mapped
  through a new **PIC–Boson Adapter**, with the author's permission.
- An end-to-end pipeline, neutral institutional demo, audit trail,
  counter-hypotheses, and automated tests were added.

## Architecture

1. `ThreatSignalRouter` detects scam, manipulation, link, obfuscation,
   sensitive-context, and structural anomaly markers.
2. The threat layer correlates markers and produces an explainable review
   priority without declaring that fraud or wrongdoing occurred.
3. `SignalRouter` separately detects institutional mechanism markers.
4. `PICBosonAdapter` maps them to six PIC institutional levers and paired
   computational bosons.
5. `CairoResonanceTrajectoryEngine` simulates growth and shadow trajectories.
6. `HunterPiggyPipeline` returns signals, mappings, probabilities, key levers,
   counter-hypotheses, limitations, and an audit trail.

## Core detection capabilities

- manipulative and scam-style language;
- shortened, verification-style, and configured reputation-list URLs;
- obfuscated contact details;
- urgency formatting;
- high-entropy or encoded-looking structures as weak contextual signals;
- child-safety and other sensitive contexts as weak priority markers;
- cross-category correlation boosts;
- confidence-aware review priority;
- explicit limitations and mandatory human review.

HunterPiggy never treats a single keyword, URL, entropy score, or sensitive
topic as proof. Correlation changes review priority, not legal or moral status.

| PIC lever | Computational mapping |
|---|---|
| PIC–S — Structural Design | Structural Boson |
| PIC–C — Cultural Norms | Resonance Boson |
| PIC–P — Procedural Action | Procedure Boson |
| PIC–F — Fiscal Prioritisation | Resource Boson |
| PIC–J — Jurisdictional Boundary-Setting | Responsibility Boson |
| PIC–T — Temporal Constraint | Temporal / Anti-Loop Boson |

PIC identifies *where* institutional contingency acts. The computational layer
models *how* interacting effects may compound, weaken, or stabilise over time.

## Install and run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
hunter-piggy-demo
python -m unittest discover -s tests
```

Or run without installation:

```bash
PYTHONPATH=src python -m hunter_piggy.demo
```

## Minimal API

```python
from hunter_piggy import HunterPiggyPipeline

result = HunterPiggyPipeline().analyze(
    "Urgent! Verify your account now: http://bit.ly/verify-account"
)
print(result.threat_assessment.to_dict())
```

## Collaboration with Codex and GPT-5.6

Anna Kai made the research, product, safety, architecture, and framework-integration
decisions. During Build Week, Codex and GPT-5.6 helped:

- audit the 19 July prototype and identify duplicated source, invalid data-model
  ordering, non-evolving trajectory output, and non-reproducible simulation;
- extract a coherent standalone package from Python Zero / Kai256;
- translate the approved PIC-to-boson research mapping into a testable adapter;
- implement the end-to-end pipeline and deterministic test suite;
- distinguish pre-existing work from the Build Week contribution.

The core product decision remained human-led: HunterPiggy must expose mechanisms
and uncertainty without classifying people or automating consequential decisions.

## Safety and limitations

- HunterPiggy analyses only text deliberately submitted to it.
- Signals are markers, not evidence or accusations.
- The current routers are transparent baselines, not trained classifiers.
- The included domain reputation list is demo data, not a live OSINT feed.
- Simulated trajectories are hypotheses, not predictions of fact.
- False positives and false negatives are expected.
- Human review is required before any meaningful action.

## Attribution

- Product and computational architecture: **Anna Kai / FreeIntelligence.Institute**
- Political–Institutional Contingency (PIC) framework: **Ian Tasker**, used with
  permission. PIC specifies Structural, Cultural, Procedural, Fiscal,
  Jurisdictional, and Temporal levers.
- Cairo Resonance Trajectory Engine concept: developed inside the wider
  Python Zero / Kai256 collaboration and extracted during Build Week.

## License

Apache License 2.0. The PIC framework attribution above must be preserved when
describing the PIC-derived mapping.
