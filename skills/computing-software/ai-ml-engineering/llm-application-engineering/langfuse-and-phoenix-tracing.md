---
id: computing-software.ai-ml-engineering.llm-application-engineering.langfuse-and-phoenix-tracing
name: langfuse-and-phoenix-tracing
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, llm-observability, langfuse, arize-phoenix, llm-tracing, trace-scores, prompt-management]
level: practitioner
status: draft
description: "Use Langfuse or Arize Phoenix for LLM observability: instrumenting apps, sessions and users, scores and feedback, datasets and experiments, and self-hosting."
sources:
  - https://langfuse.com/docs
  - https://langfuse.com/docs/observability/sdk/python/overview
  - https://arize.com/docs/phoenix
  - https://github.com/Arize-ai/phoenix
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Langfuse and Phoenix tracing

**Goal:** an LLM-specific observability tool where you can inspect traces, score them, build datasets from them, and run experiments - open-source and self-hostable.

## Langfuse
```python
from langfuse import observe, get_client
langfuse = get_client()        # LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY / LANGFUSE_HOST env vars

@observe()
def retrieve(q): ...

@observe()
def answer(q, user_id, session_id):
    langfuse.update_current_trace(user_id=user_id, session_id=session_id, tags=["v1.4"])
    docs = retrieve(q)
    return generate(q, docs)          # LLM call instrumented via integration (OpenAI drop-in, LangChain callback, OTel)
```
- Traces group into **sessions** (conversations) and **users**.
- **Scores:** attach numeric/categorical/boolean scores to traces or observations from user feedback, LLM-as-judge evaluators (configurable in the UI), or your own code (`langfuse.create_score(trace_id=..., name="helpful", value=1)`).
- **Datasets and experiments:** add traces to datasets, run app versions over them and compare scores.
- **Prompt management:** versioned prompts with labels (`production`), linked to traces.
- Built on OpenTelemetry in recent SDK versions; check the SDK major version - APIs changed between v2 and v3.

## Arize Phoenix
```python
from phoenix.otel import register
tracer_provider = register(project_name="support-bot", auto_instrument=True)  # OpenInference instrumentors
```
- Runs locally (`phoenix serve` or in a notebook) or self-hosted; OTLP ingest with OpenInference semantic conventions.
- Evals library for LLM-judge evaluations (relevance, hallucination, toxicity) over traces; datasets and experiments; embedding/cluster views for retrieval analysis.

## Choosing and running
Both: open-source with managed cloud options. Decide on data residency (self-host when traces contain sensitive data), retention, and access control. Sample traces at high volume; always keep errors and flagged traces.

## Verify
- [ ] Traces show nested retrieval/LLM/tool steps with user and session IDs.
- [ ] User feedback and automated evaluator scores attached to traces.
- [ ] Datasets built from production traces feed the eval suite.
