---
id: computing-software.ai-ml-engineering.mlflow.custom-code-scorers
name: custom-code-scorers
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, custom-scorer, scorer-decorator, mlflow-evaluate, genai-evaluation, code-based-evaluation]
level: practitioner
status: docs-checked
description: "Write code-based scorers for mlflow.genai.evaluate with @scorer: inputs/outputs/expectations/trace arguments, Feedback returns with rationale, span-level checks and return types."
sources:
  - https://mlflow.org/docs/latest/genai/eval-monitor/scorers/custom/
  - https://mlflow.org/docs/latest/genai/eval-monitor/
  - https://mlflow.org/docs/latest/genai/eval-monitor/scorers/llm-judge/predefined/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom code-based scorers (@scorer)

**Use for:** deterministic checks that do not need an LLM judge: format validity, required facts, latency budgets, tool-call correctness, citation presence.

## Basic scorers
```python
from mlflow.genai.scorers import scorer, Correctness
from mlflow.entities import Feedback
import json

@scorer
def valid_json(outputs) -> bool:
    try: json.loads(outputs); return True
    except Exception: return False

@scorer
def mentions_expected_facts(outputs, expectations) -> Feedback:
    facts = expectations["expected_facts"]
    missing = [f for f in facts if f.lower() not in outputs.lower()]
    return Feedback(value=1 - len(missing) / len(facts),
                    rationale=f"missing: {missing}" if missing else "all facts present")
```
Scorer functions declare which of `inputs`, `outputs`, `expectations`, `trace` they need (all optional); MLflow passes them by name. Valid return types are `"yes"`/`"no"`, `bool`, `int`/`float`, `Feedback`, or a list of `Feedback` objects.

## Trace-aware scorers
```python
from mlflow.entities import SpanType
@scorer
def retrieval_under_budget(trace) -> Feedback:
    spans = trace.search_spans(span_type=SpanType.RETRIEVER)
    ms = sum((s.end_time_ns - s.start_time_ns) / 1e6 for s in spans)
    return Feedback(value=ms < 300, rationale=f"retrieval took {ms:.0f} ms")

@scorer
def called_refund_tool(trace) -> bool:
    return any(s.name == "issue_refund" for s in trace.search_spans(span_type=SpanType.TOOL))
```

## Run
```python
import mlflow
results = mlflow.genai.evaluate(
    data=eval_dataset,                  # rows with inputs and expectations
    predict_fn=my_app,                  # called with **inputs; traced automatically
    scorers=[valid_json, mentions_expected_facts, retrieval_under_budget, Correctness()])
```
Mix with built-in LLM judges (`Correctness`, `RelevanceToQuery`, `Guidelines`, `RetrievalGroundedness`, all importable from `mlflow.genai.scorers`). `Correctness` needs `expected_facts` or `expected_response` in the row's expectations.

## Tips
- Return `Feedback` with rationale for anything non-obvious; it shows in the UI per row.
- A scorer can return a list of Feedback objects for multiple metrics.
- Keep scorers pure and fast. Automatic evaluation on live traces supports LLM judges; code-based `@scorer` functions only run there on a self-hosted server whose administrator enabled job containers (experimental).

## Verify
- [ ] Each scorer unit-tested on hand-made pass/fail outputs before running at scale.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- Scorer arguments (`inputs`, `outputs`, `expectations`, `trace`, all optional) and the five valid return types: docs/genai/eval-monitor/scorers/custom/index.mdx.
- `trace.search_spans(span_type=SpanType.CHAT_MODEL)` pattern, list-of-Feedback return and `Feedback(value=..., rationale=...)`: custom/code-examples.mdx.
- `SpanType` constants (TOOL, RETRIEVER, RERANKER, CHAIN, CHAT_MODEL, ...): mlflow/entities/span.py; built-in scorer names: mlflow/genai/scorers/__init__.py.
- Code-scorer limitation in automatic evaluation: docs/genai/eval-monitor/automatic-evaluations/index.mdx.
- `Correctness` expects `expected_facts`: llm-judge/predefined.mdx.

Method: documentation only; no commands were run.
