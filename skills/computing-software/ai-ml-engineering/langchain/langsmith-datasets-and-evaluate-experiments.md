---
id: computing-software.ai-ml-engineering.langchain.langsmith-datasets-and-evaluate-experiments
name: langsmith-datasets-and-evaluate-experiments
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langsmith, langsmith-datasets, langsmith-evaluation, evaluate, llm-evaluation, experiments, llm-as-judge]
level: practitioner
status: docs-checked
description: "Run offline evals in LangSmith: create datasets and examples in code, write code and openevals LLM-judge evaluators, run evaluate() experiments with metadata."
sources:
  - https://docs.langchain.com/langsmith/manage-datasets-programmatically
  - https://docs.langchain.com/langsmith/evaluation-quickstart
  - https://docs.langchain.com/langsmith/evaluate-llm-application
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LangSmith datasets and evaluate() experiments

## Dataset
```python
from langsmith import Client
client = Client()
dataset = client.create_dataset("support-qa", description="Golden support questions v1")
client.create_examples(dataset_id=dataset.id, examples=[
    {"inputs": {"question": "How do I reset 2FA?"},
     "outputs": {"answer": "Settings > Security > Reset"},
     "metadata": {"category": "auth"}},
])
```
- `create_examples` creates many examples in one request; `create_example` makes a single one. Other documented routes: create from traces, from a CSV file, and from a pandas DataFrame (Python only).
- `client.update_example(example_id=..., inputs=..., outputs=..., metadata=..., split="train")` updates one example; a bulk update accepts splits as arrays or standalone strings.

## Target and evaluators
```python
def target(inputs: dict) -> dict:
    return {"answer": my_app(inputs["question"])}

def correct(inputs: dict, outputs: dict, reference_outputs: dict) -> bool:
    return outputs["answer"] == reference_outputs["answer"]

from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT

def correctness_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
    evaluator = create_llm_as_judge(prompt=CORRECTNESS_PROMPT, model="openai:gpt-5.5", feedback_key="correctness")
    return evaluator(inputs=inputs, outputs=outputs, reference_outputs=reference_outputs)

results = client.evaluate(
    target,
    data="support-qa",                       # dataset name or UUID, or an iterator of examples
    evaluators=[correct, correctness_evaluator],
    experiment_prefix="prompt-v8",           # optional
    description="Testing prompt v8.",        # optional
    max_concurrency=4,                       # optional
    metadata={"models": [...], "prompts": [...], "tools": [...]},   # fills model/prompt/tool columns in the UI
)
```
- The target takes the example's `inputs` dict and returns an output dict. Requires `langsmith>=0.3.13` (Python).
- Evaluators are functions taking `inputs`, `outputs` and, when present, `reference_outputs`; the evaluate guide returns a bool.
- `CORRECTNESS_PROMPT` from `openevals.prompts` is an f-string with variables `inputs`, `outputs` and `reference_outputs`. Install with `pip install -U langsmith openevals openai`.
- Evaluators defined in the LangSmith UI (Evaluators tab) are triggered automatically for each new experiment.
- For larger jobs the docs recommend `aevaluate()` (same interface) and setting `max_concurrency`, which parallelizes by splitting the dataset across threads. `evaluate` can also be imported directly from `langsmith`.

## Checked
Method: docs-checked 2026-11-09 against manage-datasets-programmatically (headings and dataset/update sections), evaluation-quickstart (judge section lines 296-345 and grepped), evaluate-llm-application (evaluator and run sections lines 165-265). Dropped dataset version tagging with as_of, summary_evaluators, num_repetitions, the pairwise one-liner and the gotchas, which these pages did not confirm; the openevals README source was dropped unread.
