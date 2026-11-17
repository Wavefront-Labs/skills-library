---
id: computing-software.cloud-infrastructure-engineering.saltstack.states-extend
name: states-extend
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, states, extend, include, watch-in, require-in]
level: practitioner
status: docs-checked
description: "Modify states from an included Salt SLS with extend: append vs replace rules, single top-level declaration, and the watch_in alternative."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/states/extend.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# extend

`extend` changes states defined in another SLS, for example overriding an argument or adding a state for a service to watch.

Rules:
- The target SLS must be pulled in with `include`.
- Requisites (`watch`, `require`) are appended to; every other argument is replaced.
- `extend` is a top-level declaration. A second `extend` in the same SLS overwrites the first, so put all changes in one block (it can modify many IDs).

Alternative (since 0.9.8): `watch_in` or `require_in` on the new state adds it to another state's requisites, which is often cleaner than extending the other service.

## Checked

2026-11-04: read the Salt extend page in full. Confirmed the four rules (include first, requisites appended and everything else overwritten, one top-level extend, many IDs allowed) and the watch_in alternative added in 0.9.8. Nothing removed.

Method: documentation only; no commands were run.

