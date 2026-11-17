---
id: computing-software.ai-ml-engineering.llm-application-engineering.sampling-production-traffic-for-online-evaluation
name: sampling-production-traffic-for-online-evaluation
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, production-eval-sampling, online-evaluation, llm-as-judge, annotation-queues, observability]
level: practitioner
status: draft
description: "Evaluate LLM quality on live traffic: random and targeted trace sampling, reference-free judges, async scoring, human annotation queues, statistics and privacy controls."
sources:
  - https://docs.smith.langchain.com/observability/how_to_guides/online_evaluations
  - https://langfuse.com/docs/scores/model-based-evals
  - https://docs.claude.com/en/docs/test-and-evaluate/develop-tests
  - https://mlflow.org/docs/latest/genai/eval-monitor/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sampling production traffic for online evaluation

**Goal:** a continuous, statistically meaningful read on production quality, catching regressions offline evals missed.

## What to sample
- **Random sample** (e.g. 2-5% of traces) for unbiased quality estimates.
- **Targeted samples** (100% or high rate): negative user feedback, errors and retries, refusals, `max_tokens` truncations, long conversations, new features or prompt versions, high-value customers.
- **Stratify** by route, language, tenant tier so small segments get enough samples.
Keep sampling rules in config with the rationale; record which rule selected each trace (needed to weight results).

## What to score (no reference answer available)
- Faithfulness / groundedness: is every claim supported by the retrieved context in the trace?
- Relevance to the question; instruction and format compliance.
- Safety: toxicity, PII leakage, policy violations.
- Task-specific checks with code (valid JSON, correct tool sequence, citation present).
LLM judges run asynchronously after the response, never in the request path. Use a cheaper judge model where calibration allows, and validate judge agreement with human labels (target agreement close to human-human agreement) before trusting trends.

## Human review
Route a subset (low judge scores, disagreements, random 0.5%) to annotation queues (LangSmith, Langfuse, Phoenix, MLflow review apps). Human labels calibrate judges and become new offline eval cases.

## Statistics
Report rates with confidence intervals; with 400 samples a 10% failure rate has roughly a +/-3 point 95% interval. Compare prompt or model versions only with enough samples per arm. Weight targeted samples separately - do not mix them into the random-sample rate.

## Privacy and cost
- Respect consent and data agreements; redact PII before sending traces to judge models; restrict who can read traces.
- Budget judge spend (samples/day x tokens x price); cap per day.

## Close the loop
Weekly triage of failures -> categorise -> fix -> add cases to the offline regression set.

## Verify
- [ ] Sampling rates and rules documented; selection rule stored per trace.
- [ ] Judge agreement with humans measured.
- [ ] Dashboards show online scores with intervals by route and version.
