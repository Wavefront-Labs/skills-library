---
id: computing-software.ai-ml-engineering.langchain.langsmith-trace-sampling-otel-and-retention
name: langsmith-trace-sampling-otel-and-retention
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langsmith, langsmith-sampling, opentelemetry, data-retention, tracing-cost]
level: practitioner
status: docs-checked
description: "Control LangSmith trace volume and lifetime: sampling rate, OpenTelemetry export, input/output masking, and base vs extended retention with auto-upgrades."
sources:
  - https://docs.langchain.com/langsmith/sample-traces
  - https://docs.langchain.com/langsmith/trace-with-opentelemetry
  - https://docs.langchain.com/langsmith/administration-overview
  - https://docs.langchain.com/langsmith/mask-inputs-outputs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LangSmith trace sampling, OpenTelemetry export and retention

**Goal:** production tracing stays affordable and compliant: the right fraction of traffic is traced, sensitive fields are masked, and traces live only as long as needed.

## Sampling
- By default all traces are logged. Set `LANGSMITH_TRACING_SAMPLING_RATE` to a float between 0 (none) and 1 (all); `0.75` logs 75 percent.
- For finer control, create `Client` instances with different sampling rates and use `tracing_context(client=...)` to choose which one applies to a block of code (including a client that does not trace).

## Masking
```python
from langsmith import Client
client = Client(hide_inputs=lambda inputs: redact(inputs), hide_outputs=lambda outputs: redact(outputs))
```
`LANGSMITH_HIDE_INPUTS=true` (and `LANGSMITH_HIDE_OUTPUTS=true`) hide inputs and outputs entirely. Pass a custom client to a traced function with `langsmith_extra={"client": client}`. Function-level processors take precedence over client-level `hide_inputs` / `hide_outputs`.

## OpenTelemetry
- The OTLP base URL is your LangSmith API URL (`LANGSMITH_ENDPOINT`) plus `/otel`, for example `https://api.smith.langchain.com/otel` (US) or `https://eu.api.smith.langchain.com/otel` (EU). Exporters add the `/v1/traces` signal path themselves; including it in `OTEL_EXPORTER_OTLP_ENDPOINT` causes a 404.
- Set `OTEL_EXPORTER_OTLP_HEADERS="x-api-key=<key>"`. In project-based workspaces (including self-hosted) add `Langsmith-Project=<project>`; agent-based workspaces use the `Langsmith-Agent-Id` and `Langsmith-Agent-Environment` headers instead. Send both agent headers or neither, and never alongside `Langsmith-Project`, or LangSmith returns 400.
- To make the LangSmith SDK emit OpenTelemetry spans (for fan-out through an OpenTelemetry Collector), install `langsmith[otel]` and set `LANGSMITH_OTEL_ENABLED=true`.
- Spans using `gen_ai.*` attributes (for example `gen_ai.request.model`, `gen_ai.usage.prompt_tokens`) are shown as traces in LangSmith.

## Retention tiers
| | Base | Extended |
| - | - | - |
| Retention period | 14 days | 180 days |

- Extended retention is longer-lived and costs more; the docs state SaaS maximum retention becomes 180 days from 14 September 2026, with enterprise customers able to customise the extended period per workspace up to that maximum.
- After retention ends, traces are inaccessible in the UI and API and user data (inputs and outputs) is deleted within a day; some metadata may be kept for analytics and billing.
- Auto-upgrade from base to extended happens for: feedback sent via API or SDK with `extend_trace_retention=true`; online evaluators scoring the trace (can be opted out per evaluator when the project default is base); and automation rules with retention extension enabled (matching one run upgrades the whole trace, and thread rules upgrade every trace in the thread). Manually adding runs to an annotation queue does not upgrade by default.
- Retention extension is on by default for new online evaluators and automation rules. Tier changes apply to new traces only, and project-level default retention should be planned before sending traces.

## Verify
- [ ] Observed trace count is roughly the sampling rate times request count.
- [ ] A sample trace shows masked fields as redacted, not raw.
- [ ] Retention tier and extension settings match the data-retention policy.

## Checked
Method: docs-checked 2026-11-09 against sample-traces (full), trace-with-opentelemetry (grepped endpoints, headers, env vars and gen_ai attributes), administration-overview (retention section, lines 296-357) and mask-inputs-outputs (grepped). Corrected extended retention from about 400 days to 180 days; dropped error-sampling advice, online-evaluator scaling, per-project defaults and self-hosted TTL notes not confirmed.
