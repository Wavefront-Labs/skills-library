---
id: computing-software.systems-network-administration.network-design.change-correlation-in-troubleshooting
name: change-correlation-in-troubleshooting
category: computing-software
field: systems-network-administration
product: network-design
tags: [troubleshooting-methodology, change-correlation, what-changed, config-diff, change-log, root-cause]
level: practitioner
status: docs-checked
description: "Ask what changed first when something breaks: correlate fault start time with config diffs, change tickets, upgrades, provider and DNS changes, and cert expiry."
sources:
  - https://www.comptia.org/certifications/network
  - https://sre.google/sre-book/effective-troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Change correlation

Most outages follow a change. Establish the exact fault start time, then list every change around
it before forming theories.

## 1. Pin the start time
Monitoring graphs (first failed probe, traffic drop), first user ticket, first syslog error. Note
the time zone; align device clocks (NTP) before comparing logs.

## 2. Gather changes in the window (the fault start and the period before it)
| Source | How |
|---|---|
| Device configs | backup tool diff (for example Oxidized, which backs up device configs and can commit them to git) |
| Change tickets | change calendar entries touching the affected path |
| Automation | CI/CD pipeline runs, Ansible/Terraform applies (who, what, when) |
| Software | upgrades, reloads (device uptime), auto-updates on firewalls/SD-WAN |
| Providers | carrier maintenance notifications, cloud provider status pages |
| DNS | zone serial changes, record edits, registrar changes |
| Certificates | expiry dates of anything in the path (load balancers, IdP, VPN) |
| Security | new firewall rules, IPS signature updates, EDR policy pushes |
| Environment | power work, cabling work, facilities events |

## 3. Correlate, then test
- Did the symptom start within minutes of a change on the path? Strong candidate.
- Can you reverse it safely? A rollback is often the fastest test (and fix).
- No change found: widen the window (time bombs: certificate expiry, lease expiry, licence
  expiry, counter wraps) or consider external causes.

## Make it easy next time
- Every config change logged centrally (syslog of config commands, regular config backups with
  diffs emailed or posted to chat).
- Change records with exact timestamps of implementation, not just the planned window.
- Annotations of changes on monitoring dashboards.

## Verify
- [ ] The incident timeline lists the fault start and all changes in the window, with the
  identified change confirmed by rollback or reproduction.

## Checked

- Date: 2026-10-28
- Confirmed: Google SRE book, effective troubleshooting: recent changes are a productive place to start, and correlating changes in behaviour with other events helps; Oxidized README: config backup tool with a git output module.
- Removed: IOS archive commands, show version, hourly backup interval, Grafana annotation detail.
Method: documentation only; no commands were run.
