---
id: computing-software.ai-ml-engineering.llm-application-engineering.llm-model-selection-by-evals
name: llm-model-selection-by-evals
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, model-selection, llm-model-selection, pareto-frontier, cost-quality-latency, model-versioning]
level: practitioner
status: docs-checked
description: "Choose an LLM for a feature with evidence: task evals across models and settings, cost per successful task, latency percentiles, Pareto trade-offs and version pinning."
sources:
  - https://platform.claude.com/docs/en/about-claude/models/choosing-a-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Picking a model by quality, cost and latency evals

**Goal:** select the model (and settings) per feature from measurements on your task, not from public leaderboards.

## What the Claude docs say
- Criteria to settle first: capabilities, speed, cost, and effort. Several Claude models support an effort parameter that trades intelligence for latency and cost within one model, and the docs say tuning effort is often a better lever than switching models. Defaults differ by model (for example `high` on Sonnet 5.5, `medium` on Opus 5.5 and Haiku 5.5): start at the default and adjust from your evals.
- Two starting strategies: efficiency-first (begin with Haiku 5.5, test, upgrade only for specific capability gaps; suits prototyping, tight latency, cost-sensitive and high-volume tasks) or capability-first (begin with Opus 5.5, optimise prompts, then lower effort or downgrade models as the workflow matures).
- To decide whether to change models: build benchmark tests specific to your use case ("having a good evaluation set is the most important step"), test with your actual prompts and data, compare accuracy, response quality and edge-case handling, and weigh performance against cost.
- Multi-model strategies (an executor that escalates hard decisions to an advisor, or an orchestrator delegating bulk work to cheaper workers) are covered on the docs' "Optimizing for cost and intelligence" page.

## Procedure (practitioner synthesis)
1. **Eval set ready** (golden cases + graders). Public benchmarks only shortlist candidates.
2. **Candidates:** 3-5 models across sizes, plus settings that change behaviour and cost (effort/reasoning level, temperature, max output). Use the prompt variant best for each model; one shared prompt biases toward the model it was written for.
3. **Run** each candidate on the full eval set (several samples for nondeterministic tasks).
4. **Measure per candidate:** quality (overall and per slice); cost per request and **cost per successful task** including retries and agent loops; latency p50/p95 under realistic concurrency; failure modes (format errors, refusals, tool misuse).
5. **Plot the Pareto frontier** (quality vs cost, quality vs latency); discard dominated options and pick the operating point against the feature's requirements (for example "p95 < 2 s, quality >= 92%").
6. Consider routing (cheap model for easy cases) if no single model fits.

## Operational choices (practitioner advice)
- Pin exact model IDs in config; floating aliases can change behaviour without a deploy.
- Track provider deprecation schedules; re-run the eval suite on new releases and before forced migrations.
- Check non-functional constraints: data residency, retention terms, availability on your cloud, rate limits, context window, modality support.

## Pitfalls
- Choosing on vibes from a handful of chats.
- Comparing at different max-token or effort settings without noting it.
- Ignoring variance: two models within noise are a tie; choose on cost and latency.

## Verify
- [ ] Results table (quality, cost/task, latency) for all candidates on the same eval version.
- [ ] Chosen model ID pinned in config with the eval run linked.
- [ ] Re-evaluation scheduled for new model releases.

## Checked
Method: docs-checked 2026-11-09 against the Claude Choosing the right model page (platform.claude.com, read in full). Dropped: the OpenAI model-selection and Stanford HELM sources (not read). The procedure, pitfalls and operational sections are practitioner synthesis, not source-backed.
