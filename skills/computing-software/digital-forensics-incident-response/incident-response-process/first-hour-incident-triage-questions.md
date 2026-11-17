---
id: computing-software.digital-forensics-incident-response.incident-response-process.first-hour-incident-triage-questions
name: first-hour-incident-triage-questions
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [first-hour-triage, incident-triage, initial-scoping, dfir, incident-declaration]
level: practitioner
status: draft
description: "The first-hour triage interview and data requests: what happened, what changed, which systems and accounts, what logs exist, and what not to touch."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.rfc-editor.org/rfc/rfc3227"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# First-hour incident triage questions

**Goal:** in the first call, collect enough facts to set severity, preserve evidence and assign
work, without letting well-meaning staff destroy evidence.

## Ask the reporter / system owner
1. What did you see, when (with time zone), and how did you notice?
2. What has been done since? (reboots, AV scans, deleted files, password resets, reimages)
3. Which hosts, accounts, applications, data are involved? Business function and criticality?
4. Is it ongoing? Encryption spreading, data leaving, accounts being created?
5. Who else knows? (vendors, customers, social media, attacker contact)
6. Any recent changes: new software, admin activity, vendor access, pen test scheduled?

## Immediately request
- Hostnames/IPs, asset owner, OS, whether EDR is present.
- Log sources and retention for: EDR, DC security logs, VPN, firewall/proxy/DNS, M365/cloud audit.
- Network diagram of the affected segment; backup status of affected systems.

## Immediately instruct
- Do not power off, reboot, reimage, or run cleanup tools on affected systems.
- Do not log in to suspect hosts with privileged domain accounts (credential exposure).
- Do not email about the incident if email may be compromised; use the agreed bridge.
- Extend log retention / disable log rotation where possible.

## Output of the first hour
- Initial severity and incident commander named.
- Preservation actions dispatched (memory capture, triage collection, log export).
- First version of scope (known hosts/accounts), hypotheses, and next-2-hour action list.

## Gotchas
- Reporter times are often wrong by hours or in local time; confirm from logs.
- "We already cleaned it" means the AV quarantine folder and the AV logs are now key evidence.

## Verify
Severity, IC, preservation actions and a written scope exist within 60 minutes of the call.
