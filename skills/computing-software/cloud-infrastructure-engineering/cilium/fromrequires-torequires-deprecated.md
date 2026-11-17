---
id: computing-software.cloud-infrastructure-engineering.cilium.fromrequires-torequires-deprecated
name: fromrequires-torequires-deprecated
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, fromrequires, torequires, deprecated, label-requirements, env-prod]
level: advanced
status: docs-checked
description: "Understand Cilium fromRequires and toRequires: base label requirements that grant nothing alone, apply to all rules sharing a selector, and are removed in 1.19."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer3/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# fromRequires and toRequires

Warning from the page: deprecated as of Cilium 1.17.x and removed as of 1.19. Plan migration off them.

Purpose: base label requirements for any connectivity, for separation of concern. Example: any endpoint with `env=prod` is reachable only if the source also carries `env=prod`.

Behaviour:
- `fromRequires` grants no access by itself; combine with `fromEndpoints` (same for `toRequires` with `toEndpoints`). With the docs example, an `env=prod` endpoint becomes reachable from endpoints having both `env=prod` and `role=frontend`.
- They apply to all rules sharing the same endpoint selector and limit ALL ingress and egress traffic for that selector. Other rules (`fromEndpoints`, `fromPorts`, `toEntities`, `toServices` and so on) do not narrow their scope; the requirement stays in effect no matter what else allows.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/layer3/. 

Method: documentation only; no commands were run.
