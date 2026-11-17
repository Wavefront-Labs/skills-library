---
id: computing-software.ai-ml-engineering.llm-application-engineering.llm-classification-with-fixed-labels-and-logprobs
name: llm-classification-with-fixed-labels-and-logprobs
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, structured-output, llm-classification, logprobs, zero-shot-classification, label-calibration, routing]
level: practitioner
status: draft
description: "Classify text with LLMs reliably: enum-constrained labels, label definitions and examples, confidence from logprobs or self-consistency, calibration and when a small model wins."
sources:
  - https://platform.openai.com/docs/api-reference/chat/create#chat-create-logprobs
  - https://docs.claude.com/en/docs/about-claude/use-case-guides/ticket-routing
  - https://docs.claude.com/en/docs/build-with-claude/structured-outputs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LLM classification with fixed labels and logprobs

**Goal:** route tickets, tag content or detect intents with an LLM, getting valid labels and a usable confidence score.

## Constrain the label
- Use structured outputs with an enum: `{"label": {"enum": ["billing", "bug", "feature_request", "other"]}}`. No free-text labels to normalise.
- Always include an `other`/`unclear` class; without it, ambiguous inputs get forced into the nearest label.
- Multi-label: an array of enum values with "may be empty" stated.

## Prompt
- Define each label in one or two sentences with boundary rules ("billing: charges, refunds, invoices; NOT login problems even if the user mentions payment").
- 1-3 short examples per label, including near-misses between confusable labels.
- Optional `reasoning` field before `label` for hard taxonomies; skip it for latency-critical routing.

## Confidence
- **Token logprobs** (where the API exposes them, e.g. OpenAI `logprobs=True, top_logprobs=5`): probability mass on the first token of each label. Make labels start with distinct tokens (or use single-letter codes) so the first token identifies the label.
- **Self-consistency:** sample N times at temperature > 0 and use the agreement rate. Costs N calls.
- **Verbalised confidence** ("rate 1-5") is poorly calibrated; use it only after checking against labelled data.
- Whatever the source, calibrate on a labelled set: plot accuracy vs confidence and choose the threshold for auto-routing vs human review.

## When not to use a large LLM
At high volume with stable labels, label 1-5k examples with the LLM (plus human spot checks) and train a small classifier (fine-tuned encoder or logistic regression on embeddings). It's cheaper, faster and often as accurate; keep the LLM for the low-confidence tail.

## Evaluate
Confusion matrix and per-class precision/recall on a labelled set drawn from production traffic, re-run on every prompt or model change.

## Verify
- [ ] 100% valid labels; `other` rate monitored.
- [ ] Confidence threshold chosen from a calibration plot.
- [ ] Cost per 1k classifications compared with a distilled small model.
