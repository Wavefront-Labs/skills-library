---
id: computing-software.networking-hardware-and-wireless.check-point.policy-layers-and-inline-layers
name: policy-layers-and-inline-layers
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, policy-layers, inline-layer, ordered-layers]
level: practitioner
status: draft
description: "Design Check Point access control with ordered layers and inline layers, with Accept and Drop semantics and per-layer blades."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
  - https://www.checkpoint.com/training/certification/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Policy layers and inline layers

- A policy package holds one or more **ordered layers** (Access Control > Policy > Layers). A packet must be accepted by *every* ordered layer to pass; a drop in any layer drops it. Typical: layer 1 Network (firewall), layer 2 Application Control & URL Filtering, layer 3 Content Awareness.
- **Inline layer**: a sub-rulebase attached to a parent rule. When the parent rule matches, the traffic is evaluated in the inline layer; if no rule in it matches, the **implicit cleanup action** of the inline layer applies (Drop by default). Always put an explicit `Cleanup` rule with the intended action.
- Each layer enables its own blades (Firewall, Applications & URL Filtering, Content Awareness, Mobile Access). Enabling Applications on a layer makes the rulebase evaluate application objects, which needs the traffic to pass through full-path inspection (no SecureXL acceleration for those flows).
- Sharing: a layer can be shared among policy packages (Layer Editor > Multiple policies and rules can use this layer), so changes affect all.
```
mgmt_cli -r true add access-layer name "Net-Layer" applications-and-url-filtering false firewall true
mgmt_cli -r true add access-rule layer "Network" position top name "Web inline" source Any destination WebSrv service Any action "Inner Layer" inline-layer "Web-Inline"
mgmt_cli -r true publish
```
- Gotcha: the Drop at the end of an ordered layer only applies if the layer's *Implicit cleanup action* is Drop; an Accept implicit cleanup effectively disables the safety net. Check Layer Editor > Advanced.
- Rule position matters; top-down first match within a layer.

Verify: Install the policy, then in **Logs & Monitor > Logs** filter on a test source; the log field `Layer Name` and `Rule` show which layer made the decision (with `Policy Rule UID`). Use a drop log to find the layer.
