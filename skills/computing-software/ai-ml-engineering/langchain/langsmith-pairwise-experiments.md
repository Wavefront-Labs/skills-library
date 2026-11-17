---
id: computing-software.ai-ml-engineering.langchain.langsmith-pairwise-experiments
name: langsmith-pairwise-experiments
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langsmith-pairwise, langsmith, pairwise-evaluation, evaluate-comparative, llm-as-judge]
level: practitioner
status: docs-checked
description: "Compare two existing LangSmith experiments head-to-head: pairwise evaluator function, randomize_order, score output formats, viewing results."
sources:
  - https://docs.langchain.com/langsmith/evaluate-pairwise
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Pairwise experiments in LangSmith

**Why pairwise:** a judge (human or LLM) is often asked "which of these two outputs is better" instead of scoring each one in isolation. LangSmith supports this by evaluating **existing** experiments against each other.

## 1. Run both candidates on the same dataset
```python
from langsmith import evaluate
exp_a = evaluate(app_v1, data="support-golden-v3", experiment_prefix="prompt-v1")
exp_b = evaluate(app_v2, data="support-golden-v3", experiment_prefix="prompt-v2")
```
Requires `langsmith>=0.2.0` (Python) or `langsmith>=0.2.9` (JS).

## 2. Pairwise evaluator and run
Pass two existing experiments (names or UUIDs) as the target of `evaluate()`; `evaluate_comparative()` also exists and accepts more than two experiments.
```python
from langsmith import evaluate

def ranked_preference(inputs: dict, outputs: list[dict]) -> list:
    a = outputs[0].get("answer", "N/A")
    b = outputs[1].get("answer", "N/A")
    pref = judge(inputs["question"], a, b)   # your LLM judge returns 1, 2 or 0 (tie)
    if pref == 1: return [1, 0]
    if pref == 2: return [0, 1]
    return [0, 0]

evaluate(
    (exp_a.experiment_name, exp_b.experiment_name),
    evaluators=[ranked_preference],
    randomize_order=True,
    max_concurrency=4,
)
```

### Evaluator arguments
Any subset of: `inputs` (dict), `outputs` (two-item list of dicts, one per experiment), `reference_outputs`, `runs` (two-item list of full Run objects), `example` (the full dataset Example).

### Evaluator return types
- `dict` with `key` (feedback key), `scores` (mapping of run ID to score) and optional `comment` (commonly the judge's reasoning). Python and JS.
- Python only: a two-item list of int/float/bool scores in the same order as `runs` / `outputs`; the function name becomes the feedback key.

Choose a feedback key distinct from standard feedback on the run; the docs recommend prefixing with `pairwise_` or `ranked_`.

### Optional `evaluate()` arguments
`randomize_order` (default False) randomizes output order per evaluation to reduce positional bias; the docs say position bias should mainly be handled through prompt engineering, with this as an extra mitigation. Also `experiment_prefix`, `description`, `max_concurrency` (default 5), `client`, `metadata`, and `load_nested` (default False: only root traces are passed to the evaluator).

## Judge prompt essentials
The documented example prompt asks the judge to compare both responses, give a short explanation, avoid position bias, ignore response length and assistant names, and output 1 (A better), 2 (B better) or 0 (tie), using structured output.

## Viewing results
Open the dataset's "Pairwise Experiments" tab, select an experiment to reach the Comparison View, and use the thumbs up/down buttons in the table header to filter to runs where the first or second experiment was better.

## Checked
Method: docs-checked 2026-11-09 against https://docs.langchain.com/langsmith/evaluate-pairwise (full page). Dropped the manual order-flip code, tie score of 0.5, named judge model, significance-test and calibration advice, and the unread concepts and compare-results sources.
