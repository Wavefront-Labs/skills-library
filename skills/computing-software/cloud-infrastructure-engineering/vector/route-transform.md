---
id: computing-software.cloud-infrastructure-engineering.vector.route-transform
name: route-transform
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [route, transform, conditions, unmatched, reroute-unmatched, fanout, vector]
level: practitioner
status: docs-checked
description: "Split a stream into named outputs with route and handle events that match nothing."
sources:
  - https://vector.dev/docs/reference/configuration/transforms/route/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`route` splits one stream into several sub-streams, each defined by a condition. An event can match more than one route and is then sent to every matching output. (For first-match-wins, see exclusive-route-transform.)

```yaml
transforms:
  my-routes:
    type: route
    inputs: [some_source]
    route:
      foo-exists: 'exists(.foo)'
      foo-doesnt-exist: '!exists(.foo)'
  remap-route-1:
    type: remap
    inputs: [my-routes.foo-exists]
    source: ".route = \"route 1\""
```

Each route is addressed as `<transform_name>.<route_id>` in other components' `inputs`. Conditions use the same syntaxes as `filter` (VRL, Datadog Search, is_log and so on).

Reserved route IDs: `_unmatched` and `_default` cannot be used. With `reroute_unmatched: true` (the default), events matching no route go to the `<transform_name>._unmatched` output; set it to false to silently discard them.

The transform is stable, stateless, and handles logs, metrics and traces.

Test it with `insert_at: my-routes` and `extract_from: remap-route-1` in a unit test, as in the docs example.

Verify with the unit test above, plus an event that matches no route to confirm it reaches the `_unmatched` output.

## Checked

2026-11-03. Read transforms/route. Confirmed: multi-match routing, the `<transform>.<route_id>` input form, reserved `_unmatched` and `_default`, `reroute_unmatched` default true, stable and stateless, and the docs example with `foo-exists`. Removed: the generic typical-uses list and the `vector top` verification, neither on the page.

Method: documentation only; no commands were run.
