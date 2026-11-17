---
id: computing-software.digital-forensics-incident-response.incident-response-process.running-a-compromise-assessment
name: running-a-compromise-assessment
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [compromise-assessment, ir-preparation, threat-hunting, dfir, velociraptor]
level: advanced
status: draft
description: "Plan and run a proactive compromise assessment: scope, data collection, hunt packages, triage of findings and the report that answers 'are we breached?'"
sources: ["https://docs.velociraptor.app/docs/hunting/", "https://attack.mitre.org/", "https://csrc.nist.gov/pubs/sp/800/61/r3/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a compromise assessment

**Goal:** answer, with evidence, whether an environment shows signs of current or past
compromise, e.g. before an acquisition, after a peer breach, or as an IR readiness exercise.

## Scope and rules
- Define assets (all endpoints? DCs + crown jewels?), time window (90 days of logs typically),
  and what counts as a finding requiring escalation to IR (pre-agreed).
- Agree data handling and that any live intrusion converts to an incident under the IR plan.

## Collection
- Endpoint: deploy Velociraptor/EDR; collect autoruns, services, scheduled tasks, WMI
  subscriptions, prefetch/amcache, running processes with signatures, network connections.
- Identity: AD object dump (users, groups, ACLs, GPOs, trusts) with tooling such as
  PingCastle/ADRecon/BloodHound collection in read-only mode.
- Logs: DC security logs (4624/4625/4768/4769/4720/4728), VPN, proxy/DNS, cloud audit logs.
- Network: 1-2 weeks of Zeek/NetFlow at egress if available.

## Analysis passes
1. **Known bad:** IOC and YARA sweeps from current threat intel.
2. **Stacking:** least-frequent autoruns, services, binaries in user-writable paths, unsigned
   DLLs, parent-child process pairs across the fleet.
3. **Identity hygiene:** accounts with SPNs and weak encryption, unconstrained delegation,
   AdminSDHolder changes, recently created privileged accounts, stale krbtgt password age.
4. **Network:** beaconing (RITA), rare destinations, DNS to newly registered domains.
5. **Cloud:** new OAuth apps, federation changes, access keys older than policy, unusual sign-in locations.

## Reporting
- Findings classified: confirmed malicious, suspicious-unresolved, hygiene risk.
- State coverage honestly: % hosts collected, log gaps, time window.
- "No evidence of compromise found" is scoped to what was examined; never "not compromised".

## Gotchas
- Assessments without log retention cannot see past intrusions; report the limit.
- Pen-test tooling found mid-assessment: confirm with the red team before escalating.

## Verify
Every suspicious item is either resolved with evidence or escalated, and the coverage table is in the report.
