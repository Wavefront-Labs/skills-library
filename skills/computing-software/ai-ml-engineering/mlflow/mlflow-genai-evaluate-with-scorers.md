---
id: computing-software.ai-ml-engineering.mlflow.mlflow-genai-evaluate-with-scorers
name: mlflow-genai-evaluate-with-scorers
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-genai, mlflow-evaluate, llm-judges, scorers, genai-evaluation, eval-dataset]
level: practitioner
status: docs-checked
description: "Evaluate GenAI apps with mlflow.genai.evaluate: eval data with inputs and expectations, built-in LLM-judge scorers, Guidelines, custom code scorers, and comparing versions."
sources:
  - https://mlflow.org/docs/latest/genai/eval-monitor/
  - https://mlflow.org/docs/latest/genai/eval-monitor/quickstart/
  - https://mlflow.org/docs/latest/genai/eval-monitor/scorers/
  - https://mlflow.org/docs/latest/genai/eval-monitor/scorers/custom/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mlflow.genai.evaluate with scorers

**Goal:** score an LLM app version on a dataset with LLM judges and code checks, and compare versions in the MLflow UI. (MLflow 3 GenAI API; MLflow 2's `mlflow.evaluate(model_type="question-answering")` is the older path.)

## Data
```python
eval_data = [
    {"inputs": {"question": "How do I reset my password?"},
     "expectations": {"expected_facts": ["Settings > Security", "reset link valid 30 minutes"]}},
    {"inputs": {"question": "Can I get a refund after 60 days?"},
     "expectations": {"expected_response": "No - refunds within 30 days only."}},
]
```
The `data` argument can also be a pandas or Spark DataFrame, an MLflow evaluation dataset, or traces from `mlflow.search_traces()` (evaluate existing outputs without re-running the app).

## Run
```python
import mlflow
from mlflow.genai.scorers import Correctness, RelevanceToQuery, Safety, Guidelines, scorer

@scorer
def short_enough(outputs) -> bool:
    return len(outputs.split()) <= 120

results = mlflow.genai.evaluate(
    data=eval_data,
    predict_fn=lambda question: my_app.answer(question),     # kwargs match the keys of "inputs"
    scorers=[Correctness(), RelevanceToQuery(), Safety(),
             Guidelines(name="tone", guidelines="Polite, no blame on the user, no internal jargon."),
             short_enough],
)
```
- Each row is run through `predict_fn` with the `inputs` keys as keyword arguments, and results show in the run's evaluation view.
- Built-in LLM judges need an LLM: the default judge model in the docs is OpenAI `gpt-4o-mini`; pass `model="<provider>:/<model>"` (for example `Correctness(model="anthropic:/<model-name>")`) to change it, and keep it fixed across comparisons.
- Custom scorers receive any of `inputs`, `outputs`, `expectations`, `trace` and return bool/number/`Feedback`.

## Comparing versions
Run evaluate once per app version (log the version as a param/tag); compare runs in the UI's evaluation view, row by row, to see which questions regressed.

## Judge hygiene
Validate built-in and Guidelines judges against a sample of human-labelled rows before trusting them; adjust guideline wording where they disagree. Prefer code scorers for anything checkable (format, length, citations present).

## Verify
- [ ] Eval dataset versioned; app version recorded on each evaluation run.
- [ ] Judge agreement with humans measured.
- [ ] Regressions inspected per row, not only in aggregates.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `mlflow.genai.evaluate(data, predict_fn, scorers)`, list-of-dicts / pandas / Spark DataFrame data, `inputs` keys matching `predict_fn` parameter names, `expectations` keys `expected_facts` / `expected_response`: docs/genai/eval-monitor/quickstart.mdx and running-evaluation/eval-examples.mdx.
- Default LLM-judge model `gpt-4o-mini` and the `model="provider:/model"` form: quickstart.mdx.
- Built-in scorer names and `scorer` decorator import path: mlflow/genai/scorers/__init__.py; custom scorer arguments and return types: scorers/custom/index.mdx.
- Removed as unconfirmed: the assessments-attached-to-traces and aggregate-metrics-on-run statements, and the 50-row judge-validation figure. The legacy `mlflow.evaluate` path is documented on the legacy LLM evaluation page.

Method: documentation only; no commands were run.
