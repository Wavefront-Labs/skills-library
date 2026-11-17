---
id: engineering-technology.systems-engineering.systems-architecture.sysml-functional-architecture-and-trade-studies
name: sysml-functional-architecture-and-trade-studies
category: engineering-technology
field: systems-engineering
product: systems-architecture
tags: [systems-architecture, mbse, sysml, sysml-v1, sysml-v2, functional-decomposition, functional-architecture, ffbd, allocation, allocation-matrix, cameo, catia-magic, capella, arcadia, trade-study, pugh-matrix, weighted-decision-matrix, sensitivity-analysis, swing-weighting, ahp, analysis-of-alternatives, block-definition-diagram, internal-block-diagram, logical-architecture]
level: advanced
status: draft
description: "Build a functional architecture in SysML (v1.6/v2) or Capella, allocate functions to physical elements, and pick a concept with a Pugh screen plus a weighted trade study and sensitivity check."
sources: ["OMG Systems Modeling Language (SysML) v1.6 / v1.7 specification", "OMG SysML v2 specification", "Friedenthal, Moore, Steiner — A Practical Guide to SysML", "Roques — Systems Architecture Modeling with the Arcadia Method (Capella)", "NASA Systems Engineering Handbook SP-2016-6105 Rev 2", "INCOSE Systems Engineering Handbook, 5th ed."]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SysML functional architecture and trade studies — from functions to a defended concept

**Goal:** decompose what the system must do, allocate it to candidate physical architectures, and select one with a trade study whose result survives a challenge to its weights.

## 1. Functional decomposition
1. Start from the context: system boundary, external actors, and operational scenarios (use cases / Capella *Operational Analysis*).
2. Name each function **verb + noun** ("Convert DC power", "Estimate attitude"), solution-free.
3. Decompose level by level; 3–7 children per parent keeps reviews tractable. Stop when a function can be allocated to a single element.
4. For each scenario draw the flow (SysML **activity diagram** or classic FFBD) with object flows for items exchanged (power, data, fluid, force).
5. Check completeness: every system requirement traces to at least one function (SysML `«refine»`/`«satisfy»`), every leaf function to a requirement.

## 2. SysML views you actually need
SysML v1.x has nine diagram kinds: requirement, use case, package, block definition (**bdd**), internal block (**ibd**), activity, sequence, state machine, parametric. Practical minimum: bdd (structure hierarchy), ibd (connections via ports/flows), activity (functions), state machine (modes), requirement or a requirement table, parametric for budgets.

**SysML v2** (adopted by OMG, 2025 — check final status) replaces UML profiling with its own metamodel, a textual notation and a standard API:
```
part def PowerSubsystem { port busOut : PowerPort; }
action def ConvertDCPower { in vIn : Voltage; out vOut : Voltage; }
allocate ConvertDCPower to PowerSubsystem;
```
Tooling: Cameo Systems Modeler / CATIA Magic (v1, v2 support emerging), Capella (Arcadia: Operational → System → Logical → Physical → EPBS; not SysML-notated but similar concepts), Enterprise Architect, SysON / open v2 pilot implementations.

## 3. Allocation
- Allocate leaf functions to logical then physical components (SysML `«allocate»`; Capella functional allocation). Render an **allocation matrix** (functions × components).
- Rule: each leaf function allocated to exactly one component; a function split across two components means decompose further.
- Function-to-function flows that cross component boundaries *are* your interfaces — export them to the N2 work in engineering-technology.systems-engineering.interface-management.n2-diagrams-and-icd-authoring.

## 4. Trade study
**Screen with a Pugh matrix:** pick a datum concept; score each alternative per criterion as + / S / − versus datum; drop clearly dominated options, hybridise strong ones. No weights at this stage.

**Weighted decision matrix for the 2–4 survivors:**
1. Criteria: independent, measurable, derived from requirements and MOEs (mass, cost, TRL, power, risk). Requirements that are pass/fail are *gates*, not criteria.
2. Weights sum to 1.0; derive by swing weighting or AHP (accept AHP consistency ratio < 0.10).
3. Score with defined utility scales (e.g. 1/3/9, or a linear utility between threshold and objective values), not gut feel.
4. Utility U_a = Σ w_k · s_ak.

**Sensitivity:** for each criterion k, vary w_k while rescaling the other weights proportionally. With R_a the weighted mean of alternative a over the other criteria, U_a(w_k) = w_k·s_ak + (1 − w_k)·R_a. The crossover weight where A and B tie:

w* = (R_B − R_A) / [(s_Ak − R_A) − (s_Bk − R_B)]

If w* lies within a plausible range of the current weight (say ±0.10), the decision is weight-sensitive: report it. Complement with a Monte Carlo over weights and score uncertainty and quote the probability each option ranks first.

## Gotchas
- Correlated criteria (mass and cost both driven by size) double-count — merge or decorrelate.
- Scoring the incumbent design as datum biases toward it; rotate the datum once.
- A model is not an architecture: diagrams without a governing model (one element, many views) drift. Use the repository, not pictures.
- SysML v1 → v2 migration is not lossless; pilot on one subsystem before committing a programme.
- Decomposing by physical part ("Battery function") is a physical tree in disguise.

## Verify
- [ ] Every leaf function is verb–noun, traced to a requirement, and allocated to exactly one component.
- [ ] Every cross-component flow appears as an interface in the N2/ICD set.
- [ ] Trade criteria are independent, weights sum to 1.0 with documented derivation, and scoring scales are written down.
- [ ] Crossover weights are computed for every criterion and the winner is robust or the sensitivity is stated.
- [ ] Rationale for the selected concept is recorded in the model or decision record.
