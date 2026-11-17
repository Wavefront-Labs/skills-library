---
id: computing-software.digital-forensics-incident-response.incident-response-process.planning-a-coordinated-remediation-event
name: planning-a-coordinated-remediation-event
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [remediation-event, coordinated-remediation, eradication, active-directory, incident-response, dfir]
level: advanced
status: draft
description: "Plan and run a coordinated remediation event to evict an intruder in one window: preconditions, action list, sequencing, rehearsal and post-event watch."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.mandiant.com/resources/reports"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Planning a coordinated remediation event

**Goal:** remove every attacker foothold at the same time so they cannot use one remaining
backdoor to re-enter and adapt (the FOR508 "enterprise remediation" approach).

## Preconditions
- Scope is believed complete: all compromised hosts, accounts, persistence, C2, tools and
  the initial access vector identified, sweeps clean elsewhere.
- Monitoring in place to see re-entry (EDR on all hosts, identity and egress logging).
- Business approval for the window (outages, password resets, VPN downtime).

## Action list (typical AD intrusion)
1. Block C2 domains/IPs and known exfil channels.
2. Isolate/rebuild compromised hosts.
3. Disable attacker-created accounts; reset compromised users and **all privileged accounts**;
   rotate service account passwords.
4. **KRBTGT double reset** if domain admin was obtained.
5. Remove persistence (services, tasks, WMI, Run keys, web shells, GPO changes).
6. Close the initial access vector (patch VPN, disable exposed RDP, enforce MFA).
7. Rotate secrets: API keys, cloud keys, certificates, backup/hypervisor/network device
   credentials.
8. Revoke cloud sessions and OAuth grants.

## Sequencing and execution
- Order by dependency: block egress first, then accounts and persistence, then initial access.
- Runbook with owner, exact command, verification, and rollback for each step.
- Dry run in a test environment for scripts (mass resets, GPO changes).
- Execute on a bridge with the IC calling each step; scribe records times.

## After the event
- 72 h heightened watch for re-entry: new logons with reset accounts, new persistence,
  beacons from previously unknown hosts.
- If re-entry happens, treat it as missed scope; do not repeat the same plan blindly.

## Verify
Every action has a verification result recorded. Follow-up sweeps for all IOCs return clean
and no new attacker activity appears in the watch period.
