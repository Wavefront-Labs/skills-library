---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-parameterization-context-data-defaults
name: argo-events-trigger-parameterization-context-data-defaults
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, parameters, contextkey, datakey, default-value, userawdata, dest]
level: practitioner
status: docs-checked
description: "Inject event context or data into trigger resources with parameters, including defaults and the useRawData type behavior."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/tutorials/02-parameterization.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger parameterization context data defaults

A trigger `parameters` entry has a `src` (where to read) and a `dest` (the path in the trigger resource to replace, such as `spec.arguments.parameters.0.value`).

Event structure the Sensor sees for a webhook: `context` (type, specversion, source, id, time, datacontenttype, subject) and `data` with `header` (request headers) and `body` (request payload).

- `contextKey: type` extracts a context field (for webhook, `webhook`).
- `dataKey: body.message` extracts event data; the workflow prints "this is my first webhook".
- If both keys are set, `dataKey` takes precedence.
- Default value: add `value` to the parameter; if the key is missing in the event (say `dataKey` points at an unknown key) the default is used (`wow! a default value.`).
- Type: when `useRawData` is unset or false the parameter resolves to a string; with `useRawData: true` a number, boolean, JSON or string value may be passed through.

```yaml
parameters:
  - src:
      dependencyName: test-dep
      dataKey: body.message
      value: wow! a default value.
    dest: spec.arguments.parameters.0.value
```

You can add as many parameters as needed.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/tutorials/02-parameterization.md. Confirmed: event structure, contextKey, dataKey, precedence, default value, useRawData behaviour. Removed or changed: the claim that parameters apply in order. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
