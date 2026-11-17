---
id: computing-software.ai-ml-engineering.langchain.langsmith-traceable-tracing
name: langsmith-traceable-tracing
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langsmith, tracing, traceable, wrap-openai, observability, run-metadata]
level: practitioner
status: docs-checked
description: "Instrument Python code for LangSmith with @traceable and SDK wrappers, add tags and metadata, sample, redact inputs and flush before exit."
sources:
  - https://docs.langchain.com/langsmith/annotate-code
  - https://docs.langchain.com/langsmith/add-metadata-tags
  - https://docs.langchain.com/langsmith/mask-inputs-outputs
  - https://docs.langchain.com/langsmith/sample-traces
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LangSmith tracing with @traceable

## Enable
```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=...
```
`LANGSMITH_TRACING` controls the `@traceable` decorator and the `trace` context manager. To override at runtime without changing environment variables, use `tracing_context(enabled=True/False)` in Python. `RunTree` objects are not affected by these controls and always send data when posted.

## Non-LangChain code
```python
import langsmith as ls
from langsmith.wrappers import wrap_openai

client = wrap_openai(openai.Client())      # wrapped client calls are traced automatically

@ls.traceable(run_type="tool", name="Retrieve Context")
def search(q: str): ...

@ls.traceable(run_type="llm", name="Call", tags=["rag"], metadata={"prompt_version": "v7"})
def call(messages):
    rt = ls.get_current_run_tree()           # set metadata and tags dynamically
    rt.metadata["some-key"] = "some-val"
    rt.tags.extend(["another-tag"])
    ...

call(messages, langsmith_extra={"tags": ["t2"], "metadata": {"user": "u1"}})   # at invocation time

with ls.tracing_context(metadata={"default-key": "default-value"}):   # defaults for runs in scope;
    call(messages)                                                      # does not create a span itself
```
- Functions called from another traced function nest automatically as child runs.
- `run_type="llm"` lets LangSmith render token counts and latency correctly; `run_type="tool"` is shown in the docs for tool functions, and `"chain"` for pipeline steps.
- `ls.trace(name=..., run_type=..., inputs=..., tags=..., metadata=...)` as a context manager creates a new span; set outputs with `rt.end(outputs=...)`.
- Pass `run_id` inside `langsmith_extra` to choose the run ID of a `@traceable` call.
- `wrap_openai(client, tracing_extra={"metadata": ..., "tags": ...})` sets defaults on a wrapped client; `langsmith_extra` can be passed per call.

## Production concerns
- **Sampling:** `LANGSMITH_TRACING_SAMPLING_RATE` takes a float from 0 (no traces) to 1 (all, the default); for example `0.75` logs 75 percent. Per-client rates are possible by creating `Client` instances with their own sampling and passing them to `tracing_context(client=...)`.
- **Redaction:** `LANGSMITH_HIDE_INPUTS=true` (and `LANGSMITH_HIDE_OUTPUTS`), or `Client(hide_inputs=fn, hide_outputs=fn)` and pass the client with `langsmith_extra={"client": c}`. An anonymizer (`create_anonymizer`) takes precedence over `hide_inputs` / `hide_outputs` when both apply, but is skipped when the hide environment variables are true.
- **Flushing:** tracing runs in a background thread, so the process may exit before all traces post. Call `client.flush()` before exit (for example in a `finally` block). Runs sit in an in-memory buffer that only flushes automatically when a size limit or timeout is reached.

## Verify
- [ ] A request shows one root run with nested child runs, token counts and metadata.
- [ ] Redacted fields appear masked in the UI.
- [ ] Batch job traces are present after process exit (flush works).

## Checked
Method: docs-checked 2026-11-09 against annotate-code (grepped for env vars, run_type, wrappers, flush section), add-metadata-tags (first 100 lines), mask-inputs-outputs (grepped hide_inputs, anonymizer, flush) and sample-traces (full). Dropped EU endpoint, the full run_type list, contextvars/thread advice, wrap_anthropic, wait_for_all_tracers, the project variable and the never-raise claim, which the pages read do not confirm.
