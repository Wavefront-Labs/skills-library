---
id: computing-software.ai-ml-engineering.mlflow.manual-tracing-mlflow-trace-decorator
name: manual-tracing-mlflow-trace-decorator
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-trace-decorator, mlflow-tracing, spans, start-span, genai-observability, opentelemetry]
level: practitioner
status: docs-checked
description: "Instrument GenAI code with MLflow manual tracing: @mlflow.trace, mlflow.start_span, span types and attributes, combining with autolog, async/streaming and trace tags."
sources:
  - https://mlflow.org/docs/latest/genai/tracing/app-instrumentation/manual-tracing/
  - https://mlflow.org/docs/latest/genai/tracing/search-traces/
  - https://mlflow.org/docs/latest/genai/tracing/opentelemetry/export/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manual tracing with @mlflow.trace and spans

**Use when:** autologging (OpenAI, Anthropic, LangChain...) does not cover your custom logic (retrieval, reranking, business rules), or you want named spans per pipeline stage.

## Decorator
```python
import mlflow
from mlflow.entities import SpanType
mlflow.set_experiment("support-bot")
mlflow.anthropic.autolog()                         # LLM calls become child spans automatically

@mlflow.trace(span_type=SpanType.RETRIEVER)
def retrieve(query: str, k: int = 5) -> list[str]:
    return vector_search(query, k)

@mlflow.trace(name="answer_question", span_type=SpanType.CHAIN, attributes={"version": "v3"})
def answer(query: str) -> str:
    docs = retrieve(query)
    return call_claude(query, docs)
```
Inputs (function args) and outputs (return value) are recorded automatically; nested decorated calls become child spans.

## Context manager for blocks
```python
with mlflow.start_span(name="rerank", span_type=SpanType.RERANKER) as span:
    span.set_inputs({"n_candidates": len(docs)})
    ranked = reranker(query, docs)
    span.set_outputs({"top_ids": [d.id for d in ranked[:3]]})
    span.set_attribute("model", "bge-reranker-v2")
```

## Trace-level metadata
`mlflow.update_current_trace(tags={"route": "support"}, metadata={"app_version": "1.4.2"}, session_id=sid, user=uid)` inside a traced function. Tags are mutable and metadata is fixed once the trace is logged; `session_id` and `user` fill the `mlflow.trace.session` and `mlflow.trace.user` metadata keys. Search with `tag.<key>` and `metadata.<key>`: `mlflow.search_traces(filter_string="tag.route = 'support'")`, ``filter_string="metadata.`mlflow.trace.session` = 'abc'"``.

## Async and generators
The decorator supports async functions (since MLflow 2.16.0) and generators and async generators (since 2.20.2). By default all yielded elements are captured as a list in the span output; pass `output_reducer` to aggregate them into one value.

## Production
- Lightweight `mlflow-tracing` package for production apps; send traces to a tracking server, or to an OpenTelemetry collector by setting `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` before the first trace starts.
- Sampling (`MLFLOW_TRACE_SAMPLING_RATIO`, or `sampling_ratio_override` on the decorator) and async logging (`MLFLOW_ENABLE_ASYNC_TRACE_LOGGING`) keep overhead low.
- Avoid recording secrets/PII in inputs; redact before return or use span processors.

## Verify
- [ ] The trace UI shows the expected tree (chain -> retriever -> reranker -> LLM) with inputs/outputs.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `@mlflow.trace(name, span_type, attributes, output_reducer, sampling_ratio_override, ...)` and `mlflow.start_span(name, span_type, attributes, ...)`: mlflow/tracing/fluent.py; `SpanType` constants: mlflow/entities/span.py.
- Async (>= 2.16.0), generator and async generator (>= 2.20.2) support and `output_reducer` behaviour: docs/genai/tracing/app-instrumentation/manual-tracing.mdx.
- `update_current_trace(tags, metadata, session_id, user)`: fluent.py. Filter fields `tag.<key>`, `metadata.<key>`: search-traces.mdx (the earlier `tags.` prefix was wrong).
- Export to OpenTelemetry collectors uses `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`, set before any trace: docs/genai/tracing/opentelemetry/export.mdx; `mlflow-tracing` package: lightweight-sdk.mdx; `MLFLOW_TRACE_SAMPLING_RATIO`: prod-tracing.mdx.

Method: documentation only; no commands were run.
