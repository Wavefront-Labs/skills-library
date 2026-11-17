---
id: computing-software.devops-ci-cd.argo-events.argo-events-eventsource-multiple-events-and-names
name: argo-events-eventsource-multiple-events-and-names
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, eventsource, eventname, eventsourcename, dependencies, mixed-types]
level: practitioner
status: docs-checked
description: "Define several events in one EventSource and reference them from Sensor dependencies using eventSourceName and eventName correctly."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/multiple-events.md", "https://github.com/argoproj/argo-events/blob/master/docs/eventsources/naming.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events eventsource multiple events and names

One EventSource can configure many events, of one type or mixed types (since v0.17.0).

```yaml
apiVersion: argoproj.io/v1alpha1
kind: EventSource
metadata:
  name: webhook-example      # eventSourceName
spec:
  webhook:
    example:                  # eventName
      port: "12000"
      endpoint: /example
      method: POST
    example-foo:              # eventName
      port: "13000"
      endpoint: /example2
      method: POST
```

A Sensor dependency refers to it as:

```yaml
dependencies:
  - name: test-dep
    eventSourceName: webhook-example
    eventName: example
```

`eventSourceName` is the `metadata.name` of the EventSource; `eventName` is the map key under the type. Rules for mixing types such as `webhook` and `sns` in one object: active-active types cannot be mixed with active-passive types, and every `eventName` must be unique within the EventSource, even across different types, because `eventSourceName` plus `eventName` form the dependency attributes the Sensor matches on.

For the second event, the same EventSource gives `eventSourceName: webhook-example` with `eventName: example-foo`. Multiple events in one EventSource are supported from v0.17.0.

## Checked

2026-11-04. Confirmed against the EventSource With Multiple Events page (v0.17.0 and after, single and mixed types, the two mixing rules and the reason) and the EventSource Names page (the `webhook-example` example, `eventSourceName` is the object `name`, `eventName` is the map key). Removed repeated and meta sentences; the example sets `metadata.name: webhook-example` as on the Names page.
Method: documentation only; no commands were run.
