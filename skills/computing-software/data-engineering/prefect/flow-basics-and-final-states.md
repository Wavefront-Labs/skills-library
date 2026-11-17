---
id: computing-software.data-engineering.prefect.flow-basics-and-final-states
name: flow-basics-and-final-states
category: computing-software
field: data-engineering
product: prefect
tags: [flows, flow-run, final-state, parameters, nested-flows]
level: intro
status: docs-checked
description: "Write a Prefect flow, understand how its return value or exception sets the final state, parameter size limits and nested flow behaviour."
sources:
  - https://docs.prefect.io/v3/concepts/flows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define a flow and predict the state its run ends in.

A flow is a Python function decorated with `@flow` (for example `@flow(log_prints=True)`); calling it creates a flow run. Sync and async functions, methods and generators are supported.

Parameters are the function arguments. Prefect coerces them using type hints (any Pydantic model works) and validates before the run: an invalid parameter takes a deployment run from `Pending` straight to `Failed`. When the API overrides defaults, pass parameters by keyword. The size limit is 512 KB; set `PREFECT_SERVER_API_MAX_PARAMETER_SIZE` (bytes) to change it, `0` disables the limit. Inspect with `my_flow.parameters.model_json_schema()`.

Lifecycle: a run can be interrupted (cancellation or deletion, host infrastructure failure, network problems) but should eventually reach a terminal state; one that never does is a zombie.

Final state rules:
- exception in the flow function: `FAILED`
- returned manual state (`Completed`, `Failed` from `prefect.states`): that state
- returned iterable of states: `FAILED` if any is failed
- anything else: `COMPLETED`

Custom names: `Completed(message="...", name="Skipped")`. Call a task with `return_state=True` to avoid raising and test `state.is_failed()`.

Generators: returning one consumes it fully into a list (can block); yielding avoids this.

Nested flows block the parent unless run asynchronously. A nested flow cannot be cancelled without its parent; deploy it separately and start it with `run_deployment` for independent cancellation.

## Checked

2026-11-08. Supported function types, parameter validation and 512 KB limit, final state rules, custom named state, generator behaviour and nested-flow cancellation confirmed against the flows page. Replaced the unconfirmed state list with the page's zombie-run wording.

Method: documentation only; no commands were run.
