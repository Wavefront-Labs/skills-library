---
id: computing-software.cybersecurity-defensive.endpoint-security.endpoint-isolation-and-forensic-triage
name: endpoint-isolation-and-forensic-triage
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [edr, endpoint-isolation, forensic-triage, memory-acquisition, volatile-evidence, network-containment, process-tree, persistence-mechanisms, crowdstrike, defender-for-endpoint, sentinelone, live-response]
level: advanced
status: draft
description: "Isolate a suspect endpoint via EDR and run first-response forensic triage without destroying volatile evidence: order of operations, live-response collection, and persistence checks."
sources: ["SANS FOR508 - Advanced Incident Response and Threat Hunting (public course outline)", "NIST SP 800-61 Rev. 3", "Vendor EDR live-response documentation (CrowdStrike/Defender for Endpoint/SentinelOne, general public docs)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Endpoint isolation and forensic triage — contain without destroying the evidence

**Goal:** pull a compromised endpoint out of the fight (network isolation via EDR)
while preserving the volatile evidence that explains how the attacker got in and
what they touched — the two goals are in tension and the order you do things in
determines whether you get both.

## 1. Decide isolation timing against investigation state, not reflex
EDR network isolation (host can still talk to the EDR console, nothing else)
stops lateral movement and C2 instantly — but it also tips off an attacker with
active hands-on-keyboard access, who may react by wiping logs, deploying
ransomware, or going fully dormant elsewhere. For a single confirmed-compromised,
low-value host with no sign of lateral movement, isolate immediately. For a
suspected multi-host intrusion still being scoped, coordinate isolation timing
with the IC so you contain host-by-host without alerting the attacker before
you've found the other footholds (see incident-response-coordination). Isolating
is not optional once ransomware behaviour (mass file encryption, shadow-copy
deletion) is observed — contain immediately regardless of scoping state.

## 2. Volatile evidence dies in isolation order
Collect in order of volatility, through the EDR's live-response/real-time-response
shell where possible (keeps the host otherwise undisturbed):
1. **Running processes and network connections** (`netstat`-equivalent via EDR,
   process tree with command lines) — gone on reboot.
2. **Memory** — a full memory capture if the EDR supports it or a separate tool
   can be pushed; LSASS/process memory holds credentials and injected code a disk
   image won't show. Capture *before* isolation-induced reboots or AV/EDR
   remediation actions (some "clean" actions kill and delete the malicious
   process, destroying exactly the artefact you need).
3. **Key volatile logs and artefacts**: Windows Security/Sysmon event logs
   (export, don't rely on live querying surviving a reboot), scheduled tasks,
   autoruns/persistence locations, recent prefetch/shimcache/amcache on Windows.
4. **Disk image** (or targeted file collection if full imaging isn't feasible) —
   least volatile, can wait, but still do it before any "clean and rebuild."
Never let a well-meaning admin reboot, run a disk cleanup tool, or let AV
auto-remediate a flagged host before this list is captured — each of those
destroys specific evidence classes.

## 3. Check persistence before declaring the host clean
Attackers rarely rely on one foothold. Check, at minimum: scheduled
tasks/cron, run keys/startup folders, services, WMI event subscriptions (Windows),
new/modified local accounts, SSH authorized_keys (Linux), browser extensions, and
any EDR-flagged "suspicious autoruns" list. A host "cleaned" of the original
malware but still carrying one of these is not clean.

## 4. Build the process tree, not just the single alert
Pull parent→child chain around the triggering event: what spawned the suspicious
process, what it spawned, what network connections each made, and the timestamps.
This tells you initial access vector vs. later-stage tooling, which changes the
remediation (closing a phishing-opened macro is different from closing an exposed
RDP port).

## Gotchas
- EDR "kill process" or "quarantine file" actions taken before memory capture
  remove the live artefact — sequence containment actions deliberately, or use
  isolation (network-only) instead of kill/quarantine until triage is captured.
- A reboot to "apply isolation" (some agents require it) clears memory and some
  logs — know your specific EDR's isolation mechanism before invoking it under
  pressure.
- Cloud/VM snapshots taken *after* remediation scripts ran are not equivalent to a
  pre-remediation forensic image.
- Chain of custody matters even for an internal-only incident if legal action or
  insurance claims are plausible later — label and timestamp every collected
  artefact.

## Verify
- [ ] Isolation timing was a decision tied to investigation/scoping state, not a
      reflex, and ransomware behaviour triggered immediate isolation regardless.
- [ ] Volatile evidence (processes, network, memory) was captured before any
      kill/quarantine/reboot action on the host.
- [ ] Persistence mechanisms were checked across all common classes, not just the
      one the alert named.
- [ ] A process tree with timestamps exists showing initial access and
      subsequent activity.
- [ ] Collected artefacts are labelled with collector, timestamp, and storage location.

Related: computing-software.cybersecurity-defensive.security-operations.incident-response-coordination,
computing-software.cybersecurity-defensive.endpoint-security.edr-deployment-and-tuning,
computing-software.cybersecurity-defensive.security-operations.threat-hunting-methodology
