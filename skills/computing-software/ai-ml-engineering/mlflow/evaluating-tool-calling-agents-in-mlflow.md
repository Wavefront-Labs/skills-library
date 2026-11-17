---
id: computing-software.ai-ml-engineering.mlflow.evaluating-tool-calling-agents-in-mlflow
name: evaluating-tool-calling-agents-in-mlflow
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-agent-evaluation, genai-evaluation, tool-calling, trace-scorers, agents]
level: practitioner
status: docs-checked
description: "Evaluate tool-calling agents with mlflow.genai.evaluate: traced predict functions, expectations, trace-aware scorers on tool spans, judges, and comparing agent versions."
sources:
  - https://mlflow.org/docs/latest/genai/eval-monitor/
  - https://mlflow.org/docs/latest/genai/eval-monitor/scorers/custom/
  - https://mlflow.org/docs/latest/genai/eval-monitor/scorers/llm-judge/predefined/
  - https://mlflow.org/docs/latest/genai/eval-monitor/scorers/llm-judge/tool-call/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Evaluating tool-calling agents in MLflow

**Goal:** agent changes (prompt, model, tools) are compared on the same dataset with scores for final answers and for the tool-use path, not just output text.

## Dataset with expectations
```python
data = [
  {"inputs": {"question": "Cancel order 1182"},
   "expectations": {"expected_tools": ["lookup_order", "cancel_order"],
                    "expected_facts": ["order 1182 is cancelled", "refund in 5-7 days"]}},
  ...
]
```
Store reusable sets as MLflow evaluation datasets (`mlflow.genai.datasets`) so versions are tracked alongside runs.

## Traced predict function
```python
import mlflow
mlflow.langchain.autolog()          # or anthropic/openai autolog, or @mlflow.trace on your loop
def predict_fn(question: str) -> str:
    return agent.invoke({"messages": [{"role": "user", "content": question}]})["messages"][-1].content
```
`mlflow.genai.evaluate` calls `predict_fn(**inputs)` per row and captures a trace, so scorers can inspect every tool span.

## Trace-aware custom scorer
```python
from mlflow.genai.scorers import scorer
from mlflow.entities import SpanType, Feedback

@scorer
def tool_path(trace, expectations) -> Feedback:
    called = [s.name for s in trace.search_spans(span_type=SpanType.TOOL)]
    missing = [t for t in expectations["expected_tools"] if t not in called]
    return Feedback(value=not missing, rationale=f"called={called} missing={missing}")

@scorer
def tool_calls_count(trace) -> int:
    return len(trace.search_spans(span_type=SpanType.TOOL))
```
Add built-in judges for answer quality: `Correctness()` (uses `expected_facts` or `expected_response`), `RelevanceToQuery()`, `Safety()`, `Guidelines(name="policy", guidelines="Never cancel without confirming the order id")`. MLflow also ships tool-call judges, `ToolCallCorrectness` and `ToolCallEfficiency` (plus `ConversationalToolCallEfficiency`), in `mlflow.genai.scorers`; prefer deterministic span checks where the expected path is known.

## Run and compare
```python
from mlflow.genai.scorers import Correctness, Safety
with mlflow.start_run(run_name="agent-v8"):
    mlflow.genai.evaluate(data=data, predict_fn=predict_fn,
                          scorers=[tool_path, tool_calls_count, Correctness(), Safety()])
```
Compare runs in the Evaluation UI per row. Look at: task success, wrong-tool rate, average tool calls and tokens per task (efficiency regressions are common after prompt changes), and safety failures.

## Gotchas
- Agents are non-deterministic: run each case 3+ times for small datasets or report variance.
- Tools with side effects must point at sandboxes or mocks during eval.
- Judge models need their own calibration against human labels before you trust thresholds.

## Verify
- [ ] Every row has a trace with tool spans in the evaluation results.
- [ ] Release gate thresholds exist for task success and wrong-tool rate.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `mlflow.genai.evaluate(data, predict_fn, scorers)` with list-of-dict rows whose `inputs` keys match `predict_fn` parameter names: docs/genai/eval-monitor/quickstart.mdx.
- `@scorer` trace-aware pattern with `trace.search_spans(span_type=SpanType.TOOL)` and `Feedback` return: scorers/custom docs; `SpanType.TOOL` in mlflow/entities/span.py.
- Built-in `Correctness`, `RelevanceToQuery`, `Safety`, `Guidelines`, `ToolCallCorrectness`, `ToolCallEfficiency`, `ConversationalToolCallEfficiency`: mlflow/genai/scorers/__init__.py.
- Behavioural advice (reruns, sandboxes, judge calibration) is process guidance, not a product claim, and was left as is.

Method: documentation only; no commands were run.
