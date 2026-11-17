---
id: computing-software.digital-forensics-incident-response.incident-response-process.post-incident-heightened-monitoring
name: post-incident-heightened-monitoring
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [post-incident-monitoring, incident-recovery, threat-hunting, re-entry-detection, dfir]
level: practitioner
status: draft
description: "Run heightened post-incident monitoring to detect attacker re-entry: incident-specific detections, watchlists, hunt cadence and when to stand down."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-incident heightened monitoring

**Goal:** catch the attacker coming back. Re-compromise after eviction is common, through
missed persistence, stolen credentials not rotated, or the same unpatched entry point.

## Build incident-specific detections
- Every IOC from the case (hashes, domains, IPs, named pipes, service names, user agents) as
  SIEM/EDR detections with high priority.
- Behavioural rules for the TTPs seen: the exact lateral movement method, the LOLBins used,
  the persistence types, the exfil tool (rclone, MEGA, WinSCP).
- Watchlists: reset accounts, previously compromised hosts, the attacker's source ASNs/VPN
  providers, service accounts used.

## Specific re-entry signals
- Logon attempts with old passwords of reset accounts (4625 / sign-in failures with correct
  user but old credential pattern).
- New MFA method registrations, new OAuth app consents, new inbox rules.
- New accounts, group membership changes, GPO edits.
- Beacons to newly registered domains from previously affected subnets.
- VPN logins from new devices for previously compromised users.

## Cadence
- Daily review of incident detections and watchlists for 2 weeks, then weekly to 90 days.
- Scheduled hunts at day 7, 30 and 90 using the incident's hunt queries.
- Re-sweep for IOCs across hosts that were offline during the incident.

## Stand-down criteria
No relevant hits for the agreed period, all remediation actions verified, detections
converted to permanent rules where valuable. Document the decision.

## Verify
Test each incident detection by safely simulating the behaviour (Atomic Red Team test or
replaying a log sample) and confirming the alert fires and reaches a human.
