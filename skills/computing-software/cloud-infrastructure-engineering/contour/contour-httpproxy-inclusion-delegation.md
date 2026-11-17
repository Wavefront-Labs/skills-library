---
id: computing-software.cloud-infrastructure-engineering.contour.contour-httpproxy-inclusion-delegation
name: contour-httpproxy-inclusion-delegation
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [inclusion, delegation, includes, root-httpproxy, multi-team, orphaned, conditions-concatenation]
level: practitioner
status: docs-checked
description: "HTTPProxy inclusion: root vs child proxies, includes with conditions, cross-namespace delegation, condition concatenation rules, orphaned children."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/inclusion-delegation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy inclusion and delegation

A root HTTPProxy has `spec.virtualhost`; included proxies must not. Roots cannot include other roots. Contour merges the inclusion tree into one object before rendering Envoy config; includes may cross namespaces (watch-namespaces must list them all).

```yaml
spec:
  virtualhost:
    fqdn: ns-root.bar.com
  includes:
  - name: blog
    namespace: marketing        # optional, defaults to same namespace
    conditions:
    - prefix: /blog
  routes:
  - services: [{name: s1, port: 80}]
```

Condition merging (recursive through the tree):
- `prefix` conditions concatenate from the root: `/api` then `/v1` becomes `/api/v1`.
- `exact` and `regex` are not allowed in include conditions, but a child route's `exact`/`regex` is appended to the inherited prefix (`/static` + `exact: /main.js` gives `exact: /static/main.js`).
- Repeated identical exact `header` conditions on the same key make the proxy `Invalid`.
- Multiple prefixes cannot be on a single route's conditions.

Other rules:
- Includes are a YAML list; `name` is required, `namespace` and `conditions` optional.
- Orphaned HTTPProxies (not included by any root) are ignored.

## Checked

2026-11-08. Read the Contour main-branch config page inclusion-delegation.md in full. Confirmed: root versus included proxies, roots cannot include roots, merged inclusion tree, cross-namespace includes and the `--watch-namespaces` requirement, the required and optional include fields, the concatenation rules for prefix, exact and regex conditions, the invalid repeated header rule, and orphaned proxies. Removed three unsourced claims (a route that both delegates and lists services is invalid, cycles are invalid, a missing include yields 502) and the closing advice about `--root-namespaces`.

Method: documentation only; no commands were run.
