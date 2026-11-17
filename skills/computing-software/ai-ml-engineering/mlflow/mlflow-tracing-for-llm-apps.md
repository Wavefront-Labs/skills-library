---
id: computing-software.ai-ml-engineering.mlflow.mlflow-tracing-for-llm-apps
name: mlflow-tracing-for-llm-apps
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-genai, mlflow-tracing, mlflow-trace, llm-observability, autolog, spans]
level: practitioner
status: docs-checked
description: "Trace LLM applications with MLflow Tracing: provider/framework autolog, @mlflow.trace and manual spans, attaching metadata and feedback, searching traces and production setup."
sources:
  - https://mlflow.org/docs/latest/genai/tracing/
  - https://mlflow.org/docs/latest/genai/tracing/prod-tracing/
  - https://mlflow.org/docs/latest/genai/tracing/search-traces/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MLflow Tracing for LLM apps

**Goal:** see every LLM call, retrieval and tool step of a request as a trace with inputs, outputs, latency and token usage.

## Automatic instrumentation
```python
import mlflow
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("support-bot")
mlflow.openai.autolog()          # also: mlflow.anthropic.autolog(), mlflow.langchain.autolog(), mlflow.llama_index.autolog(), ...
```
Each SDK/framework call becomes a span with request, response, model and token counts.

## Your own steps
```python
@mlflow.trace(span_type="RETRIEVER")
def retrieve(query: str) -> list[str]: ...

@mlflow.trace
def answer(question: str) -> str:
    docs = retrieve(question)
    with mlflow.start_span(name="rerank") as span:
        span.set_inputs({"n": len(docs)})
        top = rerank(question, docs)
        span.set_outputs({"kept": len(top)})
    return generate(question, top)
```
Nested calls build the tree automatically. Add tags and metadata with `mlflow.update_current_trace(tags={...}, metadata={...}, session_id=..., user=...)` so you can filter later (tags are mutable, metadata is fixed once logged; `session_id` and `user` fill the `mlflow.trace.session` and `mlflow.trace.user` metadata keys). Filter fields are `tag.<key>` and `metadata.<key>`.

## Querying
```python
traces = mlflow.search_traces(locations=[exp_id], filter_string="tag.app_version = '1.4.0'", max_results=500)
```
Returns a DataFrame (request, response, spans, timing) - use it to build eval datasets from real traffic or to investigate regressions. Human or user feedback can be attached to traces (`mlflow.log_feedback`) and later used to select cases.

## Production
- Use the lightweight `mlflow-tracing` package in services to avoid the full MLflow dependency.
- Traces can export to an OpenTelemetry collector by setting `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` before the first trace.
- Sampling: `MLFLOW_TRACE_SAMPLING_RATIO` (default `1.0`) controls the fraction of traces exported.
- Redact PII with span processors (post-processing hooks that update each span in place) before traces are stored.

## Verify
- [ ] A request produces one trace with nested LLM/retrieval/tool spans.
- [ ] Traces filterable by `tag.app_version` and by the session metadata key.
- [ ] Sensitive fields redacted in stored traces.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `search_traces(locations=..., filter_string=..., max_results=...)` and `update_current_trace(tags, metadata, session_id, user)`: mlflow/tracing/fluent.py. Filter fields `tag.<key>` and `metadata.<key>` (the old `tags.` prefix was wrong): docs/genai/tracing/search-traces.mdx.
- `MLFLOW_TRACE_SAMPLING_RATIO` default 1.0 and `mlflow-tracing` package: prod-tracing.mdx and lightweight-sdk.mdx; `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`: opentelemetry/export.mdx; span processors for masking: observe-with-traces/masking.mdx.
- Removed as unconfirmed: always-trace-errors sampling and payload-capture disabling per span.

Method: documentation only; no commands were run.
