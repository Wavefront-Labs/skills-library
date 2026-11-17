---
id: computing-software.networking-hardware-and-wireless.envoy.priority-levels-and-overprovisioning
name: priority-levels-and-overprovisioning
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, priority, overprovisioning-factor, locality-lb-endpoints, failover, priority-load]
level: practitioner
status: docs-checked
description: "Distribute traffic across Envoy priority levels using health score times the 1.4 overprovisioning factor, and read the resulting priority load table."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/load_balancing/priority.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# priority levels and overprovisioning
Envoy normally sends traffic only to the highest priority level (P=0). Priority is set per EDS `LocalityLbEndpoints`. As P=0 endpoints become unhealthy, traffic spills to lower priorities.

The system is overprovisioned by an `overprovisioning_factor`, default 1.4. A level's health score is (percent healthy) x factor, capped at 100. P=0 receives its health score percent of traffic and the rest flows down.
- 80 percent healthy: 80 x 1.4 = 112, capped at 100, so P=0 still takes everything. It keeps all traffic until fewer than ~71.4 percent are healthy.
- 50 percent healthy: 50 x 1.4 = 70, so P=0 gets 70 percent and P=1 gets 30 percent (if P=1 is 100 percent healthy).

```yaml
load_assignment:
  endpoints:
  - priority: 0
    lb_endpoints: [ ... ]
  - priority: 1
    lb_endpoints: [ ... ]
  policy:
    overprovisioning_factor: 140
```
The `overprovisioning_factor` field is a percentage; the default 140 means 1.4, so a level is not considered unhealthy until its healthy fraction drops below about 72 percent.

The integer percentages per level are the "priority load". Gotcha: the docs' examples assume P=1 is 100 percent healthy; the page also gives tables for the case where P=1 is not.

## Checked
2026-11-03. Confirmed against priority.rst and the ClusterLoadAssignment reference (overprovisioning_factor is a percentage, default 140). Removed or corrected: the 'confirm against your version' note, the panic-mode claim, the factor tuning advice and the /clusters verify step; fixed the YAML nesting of policy.
Method: documentation only; no commands were run.
