---
id: computing-software.systems-network-administration.nagios-core.host-service-dependencies
name: host-service-dependencies
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, dependencies, servicedependency, hostdependency, execution-failure-criteria, notification-failure-criteria, inherits-parent, dependency-period, soft-state-dependencies]
level: advanced
status: docs-checked
description: "Define Nagios Core host and service dependencies: execution versus notification criteria, option letters, evaluation logic, inherits_parent and when to use parents instead."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/dependencies.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectdefinitions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependencies

One `servicedependency` / `hostdependency` object per relationship: master (depended-on) object, dependent object, failure criteria.

```
define servicedependency {
    host_name                      WWW1
    service_description            Apache Web Server
    dependent_host_name            WWW1
    dependent_service_description  Main Web Site
    execution_failure_criteria     n
    notification_failure_criteria  w,u,c
}
define hostdependency {
    host_name                      WWW1
    dependent_host_name            DBASE1
    notification_failure_criteria  d,u
}
```

Letters: service `o,w,u,c,p,n`; host `o,d,u,p,n` (p pending, n none = never fails).

## Evaluation
Take the master's current HARD state (current state if `soft_state_dependencies=1`), compare to the criteria; a match fails the dependency and stops. All must pass.

- **Execution dependencies** restrict ACTIVE checks only; a failing one defers the check and reschedules it.
- **Notification dependencies** suppress notifications until they pass.

## Options
`dependency_period` (default always). `inherits_parent 1` also tests the master's own dependencies, multi-level. Dependencies are not inherited otherwise. Omit `dependent_host_name` for same-host.

## Prefer parents
For ordinary topology use `parents` (`computing-software.systems-network-administration.nagios-core.network-reachability-parents`).

## Checked

2026-11-04. Confirmed against the Dependencies page and the Object Definitions page: servicedependency and hostdependency fields, the WWW1/DBASE1 examples, failure criteria letters, HARD-state evaluation and soft_state_dependencies, execution versus notification behaviour, dependency_period default, inherits_parent and the parents tip.

Method: documentation only; no commands were run.
