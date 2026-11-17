---
id: computing-software.cloud-infrastructure-engineering.vector.exclusive-route-transform
name: exclusive-route-transform
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [exclusive-route, transform, routing, first-match-wins, unmatched, vector]
level: practitioner
status: docs-checked
description: "Route each event to exactly one output with ordered conditions using exclusive_route."
sources:
  - https://vector.dev/docs/reference/configuration/transforms/exclusive_route/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`exclusive_route` sends each event to a single output. Routes are an ordered array evaluated first to last, and only the first matching route receives the event (first-match-wins).

```yaml
transforms:
  transform0:
    type: exclusive_route
    inputs: [source0]
    routes:
      - name: a
        condition:
          type: vrl
          source: .level == 1
      - name: b
        condition:
          type: vrl
          source: .level == 1 || .level == 2
```

Details from the reference:

- Each route `name` is also the output port, referenced downstream as `transform0.a`. Names must be unique.
- `_unmatched` is reserved and is created implicitly for events matching no route.
- The second condition above is redundant for level 1 because route `a` has precedence; the docs' own example notes this.
- Condition syntaxes are the same as for `filter`.
- It is a beta, stateless transform that handles logs, metrics and traces.

Compare with `route`, where one event may go to several outputs. Choose `exclusive_route` for mutually exclusive handling, such as sending an event to one tenant's sink only, and keep more specific conditions first because order is the tiebreaker.

Unit test it with `insert_at: transform0` inputs (see config-unit-tests-with-vector-test), and verify each event arrives on exactly one output.

## Checked

2026-11-03. Read transforms/exclusive_route. Confirmed: first-match-wins ordered routes, unique route names, `_unmatched` reserved and implicit, the `<transform>.<name>` output form, the redundant-condition note in the example, and that it is stateless with logs, metrics and traces inputs. Added: beta status from the page header. Removed: the `extract_from: transform0.a` unit-test form and the `vector top` verification, neither shown on the page.

Method: documentation only; no commands were run.
