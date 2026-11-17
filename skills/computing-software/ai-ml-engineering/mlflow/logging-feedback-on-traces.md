---
id: computing-software.ai-ml-engineering.mlflow.logging-feedback-on-traces
name: logging-feedback-on-traces
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, log-feedback, trace-assessments, human-feedback, expectations, genai-evaluation]
level: practitioner
status: docs-checked
description: "Attach human and automated feedback to MLflow traces: log_feedback, log_expectation for ground truth, assessment sources and turning feedback into eval datasets."
sources:
  - https://mlflow.org/docs/latest/genai/tracing/collect-user-feedback/
  - https://mlflow.org/docs/latest/genai/assessments/feedback/
  - https://mlflow.org/docs/latest/genai/tracing/search-traces/
  - https://mlflow.org/docs/latest/genai/datasets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Logging feedback and expectations on traces

**Assessments** in MLflow 3: **feedback** (a judgment about quality: thumbs, score, rationale) and **expectations** (ground truth: correct answer, expected facts). Both attach to a trace.

## Get the trace id to your frontend
```python
@mlflow.trace
def answer(q):
    ...
result = answer(q)
trace_id = mlflow.get_last_active_trace_id()       # return this to the client with the response
```

## Log user feedback
```python
from mlflow.entities import AssessmentSource, AssessmentSourceType
mlflow.log_feedback(
    trace_id=trace_id, name="user_satisfaction", value=True,       # float / int / str / bool / list / dict
    rationale="Answer solved my issue",
    source=AssessmentSource(source_type=AssessmentSourceType.HUMAN, source_id="user_8812"))
```
Automated judges use `source_type=LLM_JUDGE` and deterministic checks use `CODE` (the default when no source is given); the legacy `AI_JUDGE` value is deprecated. This keeps human and machine assessments distinguishable.

## Log expectations (ground truth)
```python
mlflow.log_expectation(trace_id=trace_id, name="expected_response",
                       value="Refunds are available within 30 days of purchase.",
                       source=AssessmentSource(source_type=AssessmentSourceType.HUMAN, source_id="sme_jane"))
```
Domain experts can also label traces in the MLflow UI through review queues (experimental, added in MLflow 3.14.0).

## Close the loop
- Query traces by assessment with the `feedback.<name>` and `expectation.<name>` filter fields, for example `mlflow.search_traces(filter_string="feedback.rating = 'positive'")` (the documented comparators are `=`, `!=`, `LIKE`, `ILIKE`, `RLIKE`; the docs show string values, so log string labels such as `"positive"`/`"negative"` if you want to filter).
- Add them to an evaluation dataset (`mlflow.genai.datasets`) with expectations, then run `mlflow.genai.evaluate` on each new app version.
- Track feedback rate and satisfaction over time per app version tag.

## Gotchas
- Feedback endpoints must authenticate and verify the user owns the trace, or users can spam others' traces.
- Store trace ids, not full conversations, in your app DB; MLflow is the source of truth for traces.

## Verify
- [ ] A trace in the UI shows the user's feedback and an expert's expectation with their sources.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `log_feedback` and `log_expectation` keyword-only signatures (`trace_id`, `name`, `value`, `source`, `rationale`, `span_id`) and the allowed feedback value types: mlflow/tracing/assessment.py.
- `AssessmentSourceType` HUMAN / LLM_JUDGE / CODE (default CODE), `AI_JUDGE` deprecated: mlflow/entities/assessment_source.py and assessment.py.
- `mlflow.get_last_active_trace_id()` (not thread-safe by default; `thread_local=True` available): mlflow/tracing/fluent.py.
- Trace filter fields `feedback.<name>` and `expectation.<name>`: docs/genai/tracing/search-traces.mdx. Review queues: docs/genai/assessments/review-queues.mdx.
- Removed as unconfirmed: filtering on a boolean feedback value.

Method: documentation only; no commands were run.
