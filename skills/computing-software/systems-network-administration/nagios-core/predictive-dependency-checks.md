---
id: computing-software.systems-network-administration.nagios-core.predictive-dependency-checks
name: predictive-dependency-checks
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, predictive-dependency-checks, enable-predictive-host-dependency-checks, enable-predictive-service-dependency-checks, on-demand-checks]
level: advanced
status: docs-checked
description: "Predictive host and service dependency checks in Nagios Core: when they run, the two enabling directives (default 1), and their low overhead via cached checks."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/dependencychecks.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configmain.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Predictive dependency checks

When a host changes state, Nagios checks its immediate parents and children in parallel (reachability logic). With predictive checks enabled it also checks the hosts the changed host depends on, for notification or execution dependencies, at the same time. Services work the same way.

## Enable
- `enable_predictive_host_dependency_checks` (default 1)
- `enable_predictive_service_dependency_checks` (default 1)

## Cost
The docs say overhead is rather small and recommend enabling, since accurate dependency status usually outweighs it. They are on-demand checks, so cached check rules apply and a recent result can be reused (`computing-software.systems-network-administration.nagios-core.cached-checks`).

Service predictive checks only matter if you define service dependencies (`computing-software.systems-network-administration.nagios-core.host-service-dependencies`).

## Checked

2026-11-04. Confirmed against the Predictive Dependency Checks page (parallel checks of parents, children and depended-on hosts, low overhead recommendation, on-demand and cached-check rules, service version similar) and the main configuration page (both enable_predictive_*_dependency_checks options default to 1).

Method: documentation only; no commands were run.
