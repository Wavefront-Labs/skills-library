---
id: computing-software.systems-network-administration.nagios-core.network-reachability-parents
name: network-reachability-parents
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, network-reachability, parents, down-vs-unreachable, parent-child-hosts, unreachable-notifications, topology]
level: practitioner
status: docs-checked
description: "Model network topology in Nagios Core with parents so outages show root-cause hosts DOWN and hosts behind them UNREACHABLE; suppress UNREACHABLE notices."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/networkreachability.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DOWN vs UNREACHABLE

- **DOWN:** the path to the host is not blocked, so the host itself failed.
- **UNREACHABLE:** an upstream host blocks the path; the host's real state is unknown.

## Parent/child setup
Set `parents` on each host along the path from the Nagios host: every switch, router or server hop. The Nagios host itself has no parent.

Example chain: Nagios -> Switch1 -> Router1 -> Switch2 -> Wkstn1; Router1 -> Router2 -> remote site.

## How it is determined
When a host changes state, reachability logic checks the parents and children in parallel to map the network.

Worked example: Web and Router1 fail. Both are DOWN; everything beneath Router1 is UNREACHABLE.

## Notifications
Contacts are notified for both DOWN and UNREACHABLE by default. To suppress UNREACHABLE alerts, drop `u` from the host's `notification_options` and/or the contact's `host_notification_options`.

## Performance
Avoid `max_check_attempts 1` on hosts with parents (serial parent checks). Details: `computing-software.systems-network-administration.nagios-core.host-checks`.

## Checked

2026-11-04. Confirmed against the Network Reachability page (DOWN versus UNREACHABLE, parents along the path, Nagios host has no parent, parallel parent and child checks, Web and Router1 example, dropping u from notification_options and host_notification_options) and the Host Checks page (max_check_attempts 1 serial parent checks).

Method: documentation only; no commands were run.
