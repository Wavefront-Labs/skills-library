---
id: computing-software.data-engineering.kestra.flow-variables
name: flow-variables
category: computing-software
field: data-engineering
product: kestra
tags: [variables, vars, render, setvariables, unsetvariables, pebble]
level: practitioner
status: docs-checked
description: "Define and use Kestra flow variables with vars, render() for expression values, SetVariables and UnsetVariables at runtime, and raw escaping."
sources:
  - https://kestra.io/docs/workflow-components/variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Declare under `variables`, reference as `{{ vars.name }}`.

```yaml
variables:
  myvar: hello
  numeric_variable: 42

tasks:
  - id: log
    type: io.kestra.plugin.core.log.Log
    message: "{{ vars.myvar }} world {{ vars.numeric_variable }}"
```

A variable that contains an expression is a literal string unless wrapped in `render()`. Rendering is no longer recursive.

```yaml
variables:
  time: "{{ now() }}"
# message: "{{ render(vars.time) }}"
```

Runtime changes:

- `io.kestra.plugin.core.execution.SetVariables` updates values; later tasks see them.
- `io.kestra.plugin.core.execution.UnsetVariables` takes a list of names and supports dot notation such as `nested.child`.

To print an expression literally, wrap it in `{% raw %}` and `{% endraw %}`.

Ordering: inputs resolve before execution. Variables can use inputs, but inputs generally cannot use variables. Triggers can reference inputs only if the inputs define `defaults`.

Use Secrets for sensitive values and the KV Store for values that must persist across executions.

## Checked

2026-11-04. Confirmed against the Kestra variables page: variables key and vars reference, render() for expression-valued variables, non-recursive rendering, SetVariables and UnsetVariables with dot notation, raw and endraw escaping, input and trigger resolution order, Secrets and KV Store pointers. Nothing removed.

Method: documentation only; no commands were run.
