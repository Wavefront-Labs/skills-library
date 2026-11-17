---
id: computing-software.ai-ml-engineering.llm-application-engineering.opentelemetry-genai-spans
name: opentelemetry-genai-spans
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, llm-observability, opentelemetry-genai, otel-semantic-conventions, llm-tracing, openinference, openllmetry]
level: practitioner
status: draft
description: "Instrument LLM calls with OpenTelemetry GenAI semantic conventions: span names, gen_ai.* attributes, token usage, opt-in content capture and instrumentation libraries."
sources:
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/
  - https://github.com/traceloop/openllmetry
  - https://github.com/Arize-ai/openinference
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenTelemetry GenAI spans

**Goal:** LLM calls, tool executions and agent steps appear in the same distributed traces as the rest of your services, using vendor-neutral attribute names.

## Conventions (GenAI semantic conventions - still marked in development, check the current spec)
- Span name: `{gen_ai.operation.name} {gen_ai.request.model}`, e.g. `chat claude-sonnet-5-5`; span kind CLIENT for remote model calls.
- Key attributes: `gen_ai.operation.name` (`chat`, `embeddings`, `execute_tool`, `invoke_agent`, ...), `gen_ai.provider.name` (older versions: `gen_ai.system`), `gen_ai.request.model`, `gen_ai.response.model`, `gen_ai.request.max_tokens`, `gen_ai.request.temperature`, `gen_ai.response.finish_reasons`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.response.id`.
- Tool spans: `execute_tool {gen_ai.tool.name}`.
- Metrics: `gen_ai.client.token.usage` and `gen_ai.client.operation.duration` histograms.
- Prompt/response **content is opt-in** (sensitive); instrumentations gate it behind a setting such as `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`.

## Instrument
Auto-instrumentation packages exist for major SDKs and frameworks (OpenTelemetry contrib GenAI instrumentations, OpenLLMetry by Traceloop, OpenInference by Arize). Manual:
```python
from opentelemetry import trace
tracer = trace.get_tracer("support-bot")
with tracer.start_as_current_span(f"chat {MODEL}", kind=trace.SpanKind.CLIENT) as span:
    span.set_attribute("gen_ai.operation.name", "chat")
    span.set_attribute("gen_ai.provider.name", "anthropic")
    span.set_attribute("gen_ai.request.model", MODEL)
    resp = client.messages.create(model=MODEL, max_tokens=1024, messages=msgs)
    span.set_attribute("gen_ai.response.model", resp.model)
    span.set_attribute("gen_ai.usage.input_tokens", resp.usage.input_tokens)
    span.set_attribute("gen_ai.usage.output_tokens", resp.usage.output_tokens)
    span.set_attribute("gen_ai.response.finish_reasons", [resp.stop_reason])
```
Add your own attributes for app context (`app.prompt.version`, `app.feature`, `app.tenant`).

## Backends
Any OTLP backend (Jaeger, Tempo, Honeycomb, Datadog, Grafana) shows the spans; LLM-focused tools (Langfuse, Phoenix, MLflow Tracing) ingest OTLP and add LLM-specific views.

## Gotchas
- Content capture can put PII and secrets into your tracing backend; redact or keep it off in production, sample if on.
- Streaming calls: end the span when the stream finishes, and record usage from the final event.
- Keep attribute names aligned with the spec version your backend understands; the conventions are still evolving.

## Verify
- [ ] A user request's trace shows HTTP -> retrieval -> LLM -> tool spans with gen_ai.* attributes.
- [ ] Token usage metrics populated per model.
- [ ] Content capture policy decided and enforced.
