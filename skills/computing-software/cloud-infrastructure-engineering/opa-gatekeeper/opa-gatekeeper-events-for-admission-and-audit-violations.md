---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-events-for-admission-and-audit-violations
name: opa-gatekeeper-events-for-admission-and-audit-violations
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, events, emit-admission-events, emit-audit-events, violations, kubernetes-events]
level: advanced
status: docs-checked
description: "Emit Kubernetes Events for Gatekeeper admission and audit violations (alpha flags) and understand event types, namespaces and aggregation limits."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/customize-startup.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper events for admission and audit violations

Alpha flags, all off by default:
- `--emit-admission-events`: emit every admission violation as a Kubernetes event.
- `--emit-audit-events`: emit every audit violation as an event.
- `--admission-events-involved-namespace` and `--audit-events-involved-namespace`: when `true`, events are created in the namespace of the violating object (or the Gatekeeper namespace for cluster-scoped objects); when `false`, always in the Gatekeeper namespace.

Event reasons:

| Event | Meaning |
|---|---|
| `FailedAdmission` | webhook denied the request |
| `WarningAdmission` | constraint has `enforcementAction: warn` |
| `DryrunViolation` | constraint has `enforcementAction: dryrun` |
| `AuditViolation` | violation found during audit |

Aggregation warning: if the same constraint and violating resource pair is emitted more than 10 times in a 10-minute rolling window, the Kubernetes event recorder aggregates them (shown as "combined from similar events"). Gatekeeper may burst 25 events about an object but limits refill to one new event every 5 minutes, which controls the long tail for resources that always violate.

## Checked

2026-11-04. Confirmed against customize-startup.md (Emit admission and audit events). Removed or corrected: nothing.

Method: documentation only; no commands were run.
