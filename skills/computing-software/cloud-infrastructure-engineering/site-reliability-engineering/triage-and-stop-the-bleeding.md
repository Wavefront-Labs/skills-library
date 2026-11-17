---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.triage-and-stop-the-bleeding
name: triage-and-stop-the-bleeding
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [triage-and-mitigation, stop-the-bleeding, troubleshooting, mitigation, incident-response, generic-mitigations]
level: practitioner
status: docs-checked
description: "Triage a production problem and mitigate before diagnosing: divert, drop or disable to keep the system working, while preserving logs and evidence for later root-cause analysis."
sources: ["https://sre.google/sre-book/effective-troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triage and stop the bleeding

SRE Book "Effective Troubleshooting", Triage: "Your first response in a major outage may be to start troubleshooting and
try to find a root cause as quickly as possible. Ignore that instinct!" Instead, make the system work as well as it can
under the circumstances.

## Emergency options the Book names
- Divert traffic from a broken cluster to others that are still working.
- Drop traffic wholesale to prevent a cascading failure.
- Disable subsystems to lighten the load.
- If a bug may cause unrecoverable data corruption, freezing the system to prevent further damage may be better than
  letting it continue.
Stopping the bleeding is the first priority: you do not help users if the system dies while you are root-causing.

## Preserve evidence
Rapid triage does not preclude steps to preserve evidence of what is going wrong, such as logs, for later root-cause
analysis. The Book's analogy is the novice pilot's first responsibility in an emergency: fly the airplane.

## Gotchas
- The Book calls this realisation unsettling and counterintuitive for new SREs, particularly those from product
  development backgrounds; coach new on-callers on it.
- Mitigations such as diverting traffic move load onto other clusters; check they can absorb it.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Effective Troubleshooting" (Triage section). Removed: the
five-minute triage list, the mitigation table with kubectl and pprof commands, the rollback and flag claims, the
order-of-safety claim and the verify list; this page does not state them. The O'Reilly and Workbook sources were dropped
(not read this batch).
Method: documentation only; no commands were run.
