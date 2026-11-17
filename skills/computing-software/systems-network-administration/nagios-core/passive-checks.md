---
id: computing-software.systems-network-administration.nagios-core.passive-checks
name: passive-checks
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, passive-checks, accept-passive-service-checks, passive-checks-enabled, command-file, nsca, nrdp, firewall-hosts]
level: practitioner
status: docs-checked
description: "Passive checks in Nagios Core: when to use them, the flow from external app through the command file to the reaper, and the global and per-object enable switches."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/passivechecks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passive checks

External applications run the check and submit the result.

## Use for
- Asynchronous events (SNMP traps, security alerts).
- Hosts behind firewalls Nagios cannot poll.
- Distributed or redundant setups.

## Flow
1. External app checks the host/service.
2. It writes the result to the external command file.
3. Nagios queues it when it reads the file.
4. The check result reaper processes the queue; passive results get the same handling as active (notifications, logging).

## Enable
- Global: `accept_passive_service_checks`, `accept_passive_host_checks` (1/0).
- Per object: `passive_checks_enabled`.

## Remote submission
Local apps can write the command file directly. Remote hosts need an addon: NSCA (daemon on the Nagios host, `send_nsca` client on remote) or NRDP.

## Rules
- The host/service must already exist at last (re)start, or the result is ignored.
- Passive host results are HARD unless `passive_host_checks_are_soft=1`.
- Commands format: `computing-software.systems-network-administration.nagios-core.passive-check-submission`.
- Staleness detection: `computing-software.systems-network-administration.nagios-core.freshness-checking`.

## Checked

2026-11-04. Confirmed against the Passive Checks page (uses, four-step flow with the reaper, enabling, remote submission with NSCA or NRDP, hosts and services must exist before the last restart, passive host checks HARD unless passive_host_checks_are_soft) and the main configuration page (accept_passive_host_checks, passive_host_checks_are_soft default 0).

Method: documentation only; no commands were run.
