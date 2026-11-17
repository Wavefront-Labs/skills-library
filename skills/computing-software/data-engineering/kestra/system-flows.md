---
id: computing-software.data-engineering.kestra.system-flows
name: system-flows
category: computing-software
field: data-engineering
product: kestra
tags: [system-flows, system-namespace, maintenance, purge, blueprints]
level: practitioner
status: docs-checked
description: "Use Kestra system flows in the system namespace for recurring maintenance such as purges, Git sync and failure alerts, and how to rename the namespace."
sources:
  - https://kestra.io/docs/concepts/system-flows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
System flows live in the `system` namespace and automate platform maintenance on a schedule, kept apart from user-facing executions.

Typical uses: alert notifications, support tickets when critical workflows fail, purging logs and old executions or storage files, syncing from or pushing to Git, and promoting flows from dev to QA and staging.

Any valid flow added to the `system` namespace becomes a system flow, not only blueprints. The Blueprints tab inside that namespace provides ready-to-use templates you can customize.

To use a different namespace name, set this in your Plugins and Execution configuration:

```yaml
kestra:
  systemFlows:
    namespace: system
```

System flows appear pinned at the top of the Namespaces list. Their executions show on the Dashboard, Flows and Executions pages; the Scope filter shows user executions, system executions or both.

The `system` namespace is open by default. Using namespace-level RBAC in the Enterprise Edition, you can restrict it to admins while assigning `company.*` namespaces to your general user base.

## Checked

2026-11-04. Confirmed against "Automate Platform Maintenance with System Flows" (concepts/system-flows): system namespace, typical uses, any valid flow becomes a system flow, systemFlows.namespace setting, pinned display, Scope filter, open by default and Enterprise RBAC. Removed: the claim that the Blueprints tab offers purge, Git sync and failure alert templates specifically, and that RBAC is unavailable in the default setup (the page does not state either).
Method: documentation only; no commands were run.
