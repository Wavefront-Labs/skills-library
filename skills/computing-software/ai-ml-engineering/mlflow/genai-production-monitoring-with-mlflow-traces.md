---
id: computing-software.ai-ml-engineering.mlflow.genai-production-monitoring-with-mlflow-traces
name: genai-production-monitoring-with-mlflow-traces
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-production-monitoring, mlflow-tracing, genai-monitoring, scorers, observability]
level: practitioner
status: docs-checked
description: "Monitor GenAI apps in production with MLflow: lightweight tracing SDK, async trace logging, scheduled scorers with sampling, trace search, and feeding failures back to evals."
sources:
  - https://mlflow.org/docs/latest/genai/tracing/prod-tracing/
  - https://mlflow.org/docs/latest/genai/eval-monitor/automatic-evaluations/
  - https://mlflow.org/docs/latest/genai/tracing/search-traces/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Production monitoring of GenAI traces

**Goal:** production LLM traffic is traced cheaply, quality is scored continuously on a sample, and bad traces become evaluation cases.

## Production tracing
- Install the lightweight `mlflow-tracing` package in the serving image instead of full `mlflow` (smaller, fewer dependencies).
- Point at the tracking server: `MLFLOW_TRACKING_URI`, `MLFLOW_EXPERIMENT_ID` (one experiment per app and environment).
- Async logging keeps tracing off the request path: `MLFLOW_ENABLE_ASYNC_TRACE_LOGGING` is on by default for OSS MLflow and Databricks non-notebook workloads (off in Databricks notebooks). For high QPS tune `MLFLOW_ASYNC_TRACE_LOGGING_MAX_WORKERS` and `MLFLOW_ASYNC_TRACE_LOGGING_MAX_QUEUE_SIZE`; when the queue is full new traces are discarded. `MLFLOW_TRACE_SAMPLING_RATIO` (default `1.0`) samples traces.
- Attach context to every trace: `mlflow.update_current_trace(tags={"user_tier": "pro", "route": "support"}, metadata={"app_version": GIT_SHA}, session_id=session_id, user=user_hash)`. Tags are mutable; metadata cannot be changed once the trace is logged, so put immutable facts such as the app version there. `session_id` and `user` populate the `mlflow.trace.session` and `mlflow.trace.user` metadata keys.
- Redact PII before it is logged with span processors (post-processing hooks applied to each span); traces are stored with inputs and outputs.

## Continuous scoring
Automatic evaluation runs LLM judges on a sample of new traces as they are logged (it needs a running MLflow server and an AI Gateway endpoint for the judge model; a judge evaluates traces at most one hour old when it is created or enabled):
```python
from mlflow.genai.scorers import Safety, Guidelines, ScorerSamplingConfig
safety = Safety().register(name="safety")
safety.start(sampling_config=ScorerSamplingConfig(sample_rate=1.0))
tone = Guidelines(name="tone", guidelines="Polite, no blame").register(name="tone")
tone.start(sampling_config=ScorerSamplingConfig(sample_rate=0.1))
```
Code-based scorers or ad hoc scoring: schedule a job that pulls recent traces and scores them offline:
```python
traces = mlflow.search_traces(locations=[EXP], filter_string="trace.timestamp_ms > {}".format(since), max_results=2000)
mlflow.genai.evaluate(data=traces, scorers=[Safety(), tone_scorer])
```

## Operational queries
- Errors: `filter_string="trace.status = 'ERROR'"`.
- Slow: `trace.execution_time_ms > 1000`, then group by route tag.
- Feedback: user thumbs logged with `mlflow.log_feedback(trace_id=..., name="user_rating", value=False, source=AssessmentSource(source_type="HUMAN", source_id=user_hash))`.
Track scorer pass rates, error rate, latency and tokens per request over time (the trace dashboard and token-usage views are in the MLflow UI); alert on drops.

## Close the loop
Weekly: pull failed or low-rated traces, label them, and add them to the evaluation dataset (`mlflow.genai.datasets`), so the next release is tested on real failures.

## Verify
- [ ] Response latency is unchanged with tracing on (async logging).
- [ ] Scorer results appear on sampled production traces.
- [ ] Failed traces from last week exist as rows in the eval dataset.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- Async logging default and env vars `MLFLOW_ENABLE_ASYNC_TRACE_LOGGING`, `MLFLOW_ASYNC_TRACE_LOGGING_MAX_WORKERS`, `MLFLOW_ASYNC_TRACE_LOGGING_MAX_QUEUE_SIZE`, `MLFLOW_TRACE_SAMPLING_RATIO` (default 1.0), and `mlflow-tracing` package: docs/genai/tracing/prod-tracing.mdx and lightweight-sdk.mdx.
- `update_current_trace(tags, metadata, session_id, user)` and tag-versus-metadata semantics: mlflow/tracing/fluent.py; `mlflow.trace.session` / `mlflow.trace.user` keys: track-environments-context docs.
- `ScorerSamplingConfig(sample_rate=...)`, `.register(name=...)`, `.start(...)`, one-hour window and the AI Gateway prerequisite: automatic-evaluations/index.mdx.
- Trace filter fields `trace.status`, `trace.execution_time_ms`, `trace.timestamp_ms`: search-traces.mdx; `search_traces(locations=...)` parameter: fluent.py.
- Removed as unconfirmed: the claim that scheduled scorers are Databricks-only (the current docs describe server-side automatic evaluation for OSS MLflow).

Method: documentation only; no commands were run.
