---
id: computing-software.ai-ml-engineering.llm-application-engineering.tevv-plan-and-trustworthiness-metrics
name: tevv-plan-and-trustworthiness-metrics
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, ai-risk-management, tevv, nist-ai-rmf, measure-function, trustworthiness-metrics, red-teaming]
level: practitioner
status: docs-checked
description: "Write a TEVV plan per the NIST AI RMF Measure function: metrics for validity, safety, security, fairness and privacy, thresholds, and ongoing measurement."
sources:
  - https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
  - https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook/Measure
  - https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TEVV plan and trustworthiness metrics (NIST AI RMF Measure)

**Goal:** a written plan for test, evaluation, verification and validation (TEVV) that turns each mapped risk into metrics, thresholds and evidence - before and after launch.

## Trustworthiness characteristics -> example measurements
| Characteristic (AI RMF) | LLM-app measurement examples |
|---|---|
| Valid and reliable | task accuracy on golden set, faithfulness/groundedness rate, pass^k reliability for agents, performance on recent traffic |
| Safe | harmful-output rate on safety eval set, unsafe-action rate for agents, escalation correctness |
| Secure and resilient | prompt-injection attack success rate (direct + indirect), data exfiltration tests, behaviour under provider outage |
| Accountable and transparent | logging coverage, documentation/model card completeness, user disclosure present |
| Explainable and interpretable | citation coverage, rationale availability where decisions are made |
| Privacy-enhanced | PII leakage rate in outputs/logs, memorisation probes, retention compliance |
| Fair, harmful bias managed | performance and refusal-rate gaps across groups/languages/dialects |

## Plan contents
1. Risks in scope (from the impact assessment) and the metric(s) for each.
2. Test sets: golden set, adversarial/red-team sets, slice sets (languages, user groups); provenance and refresh cadence.
3. Methods: automated graders (code checks, validated LLM judges), human evaluation protocol (raters, instructions, agreement targets), red teaming (internal and external).
4. **Thresholds and decision rules** for launch and for each release (e.g. a maximum injection success rate on a versioned suite; a maximum gap between any slice and overall).
5. Independence: who evaluates (not only the builders), and how results are reviewed.
6. Post-deployment measurement: production sampling, user feedback, incident signals, drift checks; frequency.
7. Known measurement limits (what the tests cannot show) - required by the RMF's emphasis on documenting uncertainty.

## Practice notes
- Measure the *system* (prompts, retrieval, tools, guardrails, model) not just the model; a model benchmark says little about your application's risks.
- Version test sets and results; every release has a TEVV report linked to the release.
- Re-run on model or prompt changes; regressions in safety metrics block release like functional regressions.

## Verify
- [ ] Every top risk has a metric, a test set and a threshold.
- [ ] Launch decision references the TEVV report.
- [ ] Post-launch measurement scheduled and owned.

## Checked
2026-11-01. Confirmed in NIST AI 100-1 and the AI RMF Playbook Measure page: the seven trustworthiness characteristics, MEASURE 1.1 (metrics start with the most significant risks; unmeasured risks documented), 2.1 (test sets, metrics and TEVV tools documented), 2.2 (human-subject evaluations), 3.1 (regular tracking of existing and emergent risks), 4.1 (measurement tied to deployment context). Removed: the numeric example thresholds. Measurement examples per characteristic are suggested practice, not NIST content.
Method: documentation only; no commands were run.
