---
id: computing-software.data-engineering.prefect.interactive-workflows
name: interactive-workflows
category: computing-software
field: data-engineering
product: prefect
tags: [pause, suspend, resume, run-input, wait-for-input]
level: advanced
status: docs-checked
description: "Build interactive Prefect flows with pause_flow_run, suspend_flow_run, resume_flow_run, wait_for_input types, RunInput models and send_input or receive_input."
sources:
  - https://docs.prefect.io/v3/advanced/interactive
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ask a human for input mid-run.

`pause_flow_run` and `suspend_flow_run` accept `wait_for_input`:
- a built-in type such as `int`, `str` or `List[int]`; Prefect generates a Pydantic model with one field named `value`
- a `pydantic.BaseModel` subclass, upgraded to a `RunInput` automatically
- a `prefect.input.RunInput` subclass, to override how inputs are stored

```python
user = pause_flow_run(wait_for_input=str)
```

Resume programmatically; with a built-in type the input is a dict keyed by `value`:

```python
resume_flow_run(flow_run_id, run_input={"value": "Alice"})
```

Use a `RunInput` or `BaseModel` to rename the field, add help text or set defaults shown in the Resume form. `with_initial_data(...)` sets defaults such as `name="anonymous"` and a Markdown `description` shown above the form.

Validators (such as a Pydantic `model_validator`) run after the flow resumes. A failed check raises `pydantic.ValidationError` and fails the run unless caught; the guide loops and calls `pause_flow_run` again on error.

Without pausing, use `send_input` and `receive_input(str, timeout=None)`. No timeout waits indefinitely; `timeout=30` raises `TimeoutError`. `with_metadata=True` exposes `.value`, `.metadata.key` and `.respond()`. Sender and receiver must use the same type.

The page documents no default for the `pause_flow_run` timeout.

## Checked

2026-11-09. Confirmed: Interactive workflows page (docs.prefect.io/v3/advanced/interactive): wait_for_input types, value field, resume_flow_run run_input, with_initial_data and description, validators and ValidationError loop, send_input and receive_input, timeout, with_metadata, matching types. Nothing removed.

Method: documentation only; no commands were run.
