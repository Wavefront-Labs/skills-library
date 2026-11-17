---
id: computing-software.database-administration.patroni.patroni-candidate-eligibility-checks
name: patroni-candidate-eligibility-checks
category: computing-software
field: database-administration
product: patroni
tags: [patroni, failover, candidate, nofailover, leader-race]
level: advanced
status: docs-checked
description: "The checks a member must pass to take part in a leader race or be a switchover or failover candidate."
sources:
  - https://patroni.readthedocs.io/en/latest/rest_api.html
  - https://patroni.readthedocs.io/en/latest/dcs_failsafe_mode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: explain why a node is not promoted.

A member must:
- be reachable via the Patroni API;
- not have the `nofailover` tag set to true;
- have a fully functional watchdog, if the configuration requires it;
- for a switchover in a healthy cluster or an automatic failover, not exceed `maximum_lag_on_failover`;
- for those same cases, not have a timeline lower than the cluster timeline when `check_timeline` is true;
- in synchronous mode, for a switchover (with or without a candidate), be listed in the `/sync` key members. This check is omitted for failover.
- when DCS failsafe mode is in use, be present in the `/failsafe` key to take part in the leader race.

In a leaderless cluster, a manual failover bypasses the sync, lag and timeline checks: the candidate may promote even if it is not in the `/sync` members, its lag exceeds the limit, or its timeline is older than the last known one.

## Checked

2026-11-08. Confirmed against the Patroni REST API page (healthy standby checks and the leaderless-failover warning) and the DCS failsafe mode page (`/failsafe` key membership). Removed `failover_priority` claims and two 4.1.1 release notes, which neither page covers.

Method: documentation only; no commands were run.
