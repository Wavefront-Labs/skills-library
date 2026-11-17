---
id: computing-software.ai-ml-engineering.llm-application-engineering.defining-success-criteria-for-llm-apps
name: defining-success-criteria-for-llm-apps
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, success-criteria, llm-evaluation, metrics, acceptance-criteria, eval-design]
level: practitioner
status: docs-checked
description: "Define measurable success criteria for an LLM feature before building: specific, measurable, achievable, relevant targets for quality, safety, latency, cost."
sources:
  - https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Defining measurable success criteria

**Bad:** "The bot should give good answers." **Good:** "On the 400-question support eval, at least 90% of answers are rated correct by the rubric judge (calibrated against human labels), fewer than 1% contain policy violations, p95 latency under 4 s, cost under $0.01 per conversation."

## Properties (Claude docs: specific, measurable, achievable, relevant)
- **Specific:** name what you want (not "good performance" but "accurate sentiment classification").
- **Measurable:** quantitative metrics or well-defined qualitative scales (Likert scales, expert rubrics). Even hazy topics can be quantified, e.g. "less than 0.1% of outputs out of 10,000 trials flagged for toxicity by the content filter".
- **Achievable:** base targets on industry benchmarks, prior experiments, research or expert knowledge, and not beyond current frontier model capability.
- **Relevant:** aligned with the application's purpose and user needs (citation accuracy matters more for a medical app than a casual chatbot).

Docs' worked example: an F1 of at least 0.85 on a held-out test set of 10,000 diverse Twitter posts, a 5% improvement over the current baseline. Most use cases need multidimensional criteria, e.g. F1 at least 0.85, 99.5% non-toxic outputs, 90% of errors causing inconvenience rather than egregious error, and 95% response time under 200 ms.

## Dimensions to cover
Common criteria listed by the docs: task fidelity (including edge case handling), consistency (similar inputs give semantically similar answers), relevance and coherence, tone and style, privacy preservation, context utilisation, latency, and price.

| Dimension | Example metric |
|---|---|
| Task quality | accuracy, F1, rubric score, A/B comparison against a baseline or earlier version |
| Consistency | cosine similarity of answers to paraphrased questions |
| Safety / policy | share of outputs flagged by a content filter |
| Edge cases | percentage handled without errors |
| Tone / format | style rubric, Likert rating |
| Latency | response time percentile |
| Cost | tokens and dollars per task |
| Privacy | rate of leaking details the model was told not to share |

## Process
1. Write criteria with stakeholders before prompt work starts (practitioner advice).
2. Collect or create eval cases that mirror the real task distribution, including edge cases: irrelevant or missing input, overly long input, poor or harmful user input, ambiguous cases even humans would not agree on.
3. Measure the baseline (current system or simple prompt).
4. Set targets and a launch bar; distinguish must-pass (safety) from trade-off metrics (practitioner advice).
5. Automate grading where possible (multiple choice, string match, code-graded, LLM-graded); the docs prefer more questions with slightly lower-signal automated grading over fewer hand-graded ones.
6. Revisit after launch with production data (practitioner advice).

## Verify
- [ ] Criteria document has each metric, its measurement method, the dataset, baseline and target.

## Checked
Method: docs-checked 2026-11-09 against the Claude Define success criteria and build evaluations page (platform.claude.com; success-criteria and eval-design sections read, the page serves both cited URLs). Dropped: the OpenAI evals source (unreadable), the faithfulness and jailbreak-success-rate rows, and the p50/p95 time-to-first-token wording. The opening bad/good example is illustrative.
