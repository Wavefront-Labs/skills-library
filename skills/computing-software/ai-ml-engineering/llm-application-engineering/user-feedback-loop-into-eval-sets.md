---
id: computing-software.ai-ml-engineering.llm-application-engineering.user-feedback-loop-into-eval-sets
name: user-feedback-loop-into-eval-sets
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, llm-observability, user-feedback-loop, thumbs-feedback, implicit-feedback, eval-set, data-flywheel]
level: practitioner
status: docs-checked
description: "Turn user feedback into improvements: explicit and implicit signals linked to trace IDs, triage queues, converting failures into eval cases, and avoiding feedback bias."
sources:
  - https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk
  - https://docs.smith.langchain.com/evaluation/how_to_guides/attach_user_feedback
  - https://pair.withgoogle.com/chapter/feedback-controls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collecting user feedback into eval sets

**Goal:** a loop where real failures users experience become test cases that every future version must pass.

## Capture signals linked to traces
- **Explicit:** thumbs up/down with optional reason categories ("wrong", "outdated", "unsafe", "not what I asked") and free text. Keep it one click; reasons on the down-vote only.
- **Implicit:** regenerate clicks, copying the answer, editing a generated draft (edit distance), abandoning the session, follow-up "that's wrong" messages, escalation to a human agent, task completion events.
- Send each signal with the **trace/request ID** so you can open exactly what the model saw (prompt version, retrieved docs, tool results).

## Triage
- Queue negative feedback (and a random sample of positive) for review; label root cause: retrieval miss, wrong doc, model reasoning, prompt instruction gap, missing tool, out-of-scope, user error.
- Aggregate by cause and route to owners; the counts tell you where to invest (often retrieval, not the model).

## Into the eval set
For each confirmed failure:
1. Create a test case: input (with needed context fixtures, e.g. doc snapshot), expected behaviour (reference answer, rubric, or must/must-not checks).
2. Tag it (cause, feature, date) and add it to the regression suite.
3. Fix, and confirm the case passes without regressing others.
Scrub or synthesise PII before adding production data to eval sets, and respect consent/retention policies.

## Bias in feedback
- Few users leave explicit feedback, skewed toward strong reactions; don't treat thumbs-up rate as quality.
- Use random sampling + grading of production traffic for unbiased quality estimates; feedback is for finding failures, not measuring the rate.
- Watch for changes in UI (button placement) that shift feedback rates without any quality change.

## Verify
- [ ] Feedback events carry trace IDs and reach a reviewable queue.
- [ ] Confirmed failures are added as regression cases within a set SLA.
- [ ] Quality KPI comes from sampled grading, not raw feedback rates.

## Checked
2026-11-01. Confirmed the pattern of attaching user feedback to traces/runs as scores against Langfuse scores-via-SDK and LangSmith attach-user-feedback pages, and feedback-control design against Google PAIR's feedback controls chapter. Removed the 'few percent' figure. The triage and eval-set steps are process guidance.
Method: documentation only; no commands were run.
