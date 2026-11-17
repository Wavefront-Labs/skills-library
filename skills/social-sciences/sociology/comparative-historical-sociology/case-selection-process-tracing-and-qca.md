---
id: social-sciences.sociology.comparative-historical-sociology.case-selection-process-tracing-and-qca
name: case-selection-process-tracing-and-qca
category: social-sciences
field: sociology
product: comparative-historical-sociology
tags: [comparative-historical-sociology, comparative-historical-analysis, historical-sociology, sociology, case-study, case-selection, most-similar-systems, most-different-systems, mills-methods, process-tracing, hoop-test, smoking-gun, straw-in-the-wind, doubly-decisive, archival-research, primary-sources, historiography, critical-junctures, path-dependence, qca, qualitative-comparative-analysis, csqca, fsqca, calibration, truth-table, consistency, coverage, qca-r-package, ragin]
level: advanced
status: draft
description: "Run comparative-historical analysis: select cases on purpose, work archival sources critically, apply process-tracing tests and crisp/fuzzy-set QCA with calibration."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Case selection, process tracing and QCA

**Goal:** explain large historical outcomes (revolutions, welfare states, state
formation) from a small number of cases, with case choices and causal claims that
survive the "you picked convenient cases" critique.

## 1. Case selection — deliberate, stated, defended
- **Most-similar systems:** cases alike on many background factors, different on the
  outcome → look for the factor that differs (Mill's method of difference).
- **Most-different systems:** cases differing widely but sharing the outcome → look for
  the common factor (method of agreement).
- **Typical, deviant, extreme, crucial cases** (Gerring; Seawright & Gerring) serve
  different purposes — deviant cases are good for finding missing variables.
- Don't select only on the dependent variable (all revolutions) if you want to claim
  causes — include negative cases where the outcome was possible but didn't happen
  (Mahoney & Goertz "possibility principle").
- Mill's methods are fragile with few cases and multiple causes; treat them as
  heuristics, then test within cases.

## 2. Sources
- **Primary archival sources:** government records, organisational files, letters,
  newspapers. Ask who produced it, for whom, what it omits, and what survived and why
  (archives are themselves selective).
- **Secondary historiography:** most comparative-historical work relies on historians'
  accounts — be explicit about which historiographical school you rely on and check for
  contested interpretations (Lustick's warning about selection bias in secondary sources).
- Keep a source log: claim → source → page → reliability notes.

## 3. Process tracing
Lay out the hypothesised causal chain, then look for evidence at each link. Evidence
tests (Van Evera; Bennett & Checkel):
| Test | Passing | Failing |
|---|---|---|
| Straw in the wind | Slightly supports | Slightly weakens |
| Hoop | Necessary to stay in contention, doesn't confirm | Eliminates hypothesis |
| Smoking gun | Strongly confirms | Doesn't eliminate |
| Doubly decisive | Confirms and eliminates rivals | Eliminates |
Test rival explanations with the same rigour. Attend to timing and sequence: **critical
junctures** and **path dependence** claims require showing that alternatives were
genuinely open at the juncture and that later reinforcement locked the path in.

## 4. Qualitative Comparative Analysis (QCA)
For roughly 10–50 cases, set-theoretic comparison of configurations:
1. **Calibrate** conditions into sets: crisp (0/1) or fuzzy (0–1) with three anchors —
   full membership, crossover (0.5), full non-membership — justified substantively.
2. **Test necessary conditions** first (consistency typically ≥ 0.9).
3. **Build the truth table:** each row a configuration; set a frequency threshold and a
   consistency threshold (commonly ≥ 0.75–0.8, with PRI checked).
4. **Minimise** (Boolean) to solutions: conservative, parsimonious, intermediate
   (using directional expectations for logical remainders).
5. Report consistency and coverage of each path; interpret paths through case knowledge.
R: `QCA` and `SetMethods` packages; also fs/QCA software.

## 5. Writing it up
Present a case-by-case narrative for each causal link with dated events, followed by
the cross-case comparison. Tables of conditions per case help readers check you.

## Gotchas
- QCA solutions are sensitive to calibration and thresholds — run robustness checks.
- Limited diversity (many unobserved configurations) makes parsimonious solutions rest
  on counterfactual assumptions; state them.
- Uncertain: threshold values above are conventions from methods texts, not fixed rules.

## Verify
- [ ] Case selection logic stated, including negative cases.
- [ ] Sources logged with provenance and historiographical position.
- [ ] Each mechanism link has named evidence tests; rivals tested too.
- [ ] QCA calibration anchors justified; robustness to thresholds shown.
- [ ] Cross-case table lets readers verify claims.
