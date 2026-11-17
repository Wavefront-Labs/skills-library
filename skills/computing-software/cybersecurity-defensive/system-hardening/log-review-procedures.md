---
id: computing-software.cybersecurity-defensive.system-hardening.log-review-procedures
name: log-review-procedures
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [log-review, log-management, pci-dss, daily-log-review, siem, audit-evidence]
level: practitioner
status: draft
description: "Set up log review procedures that meet PCI DSS and audit needs: what to review daily vs periodically, automating with SIEM alerts and reports, sign-off evidence, and escalation."
sources: ["https://csrc.nist.gov/pubs/sp/800/92/final", "https://www.pcisecuritystandards.org/document_library/", "https://www.cisecurity.org/controls/audit-log-management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log review procedures

Collecting logs is CIS Control 8.2; reviewing them is 8.11 ("conduct audit log reviews"). PCI DSS 10.4.1
requires daily review of security events and logs of CDE and security-critical components (automated
mechanisms allowed and expected, 10.4.1.1), and periodic review of other components per risk analysis (10.4.2).

## Define what is reviewed and how often
| Frequency | Content | Method |
|---|---|---|
| Real time | High-severity detections (malware, privilege escalation, critical config changes) | SIEM alerts to SOC queue |
| Daily | Security event summary for in-scope systems: auth failures, admin activity, new accounts and group changes, firewall/IDS denies trends, FIM alerts, log source health | SIEM dashboard/report reviewed and acknowledged |
| Weekly | Privileged account activity, VPN anomalies, change correlation | Report with sign-off |
| Monthly/quarterly | Rare-event review, rule tuning, coverage gaps | Engineering review |

## Make reviews meaningful
- Reviews start from questions with expected answers ("all domain admin logons came from PAWs?"), not scrolling
  raw logs.
- Each report has a defined "normal" and thresholds that require investigation.
- **Log source health** is part of daily review: sources silent for more than N hours are incidents for the
  logging team (PCI DSS 10.7 requires detecting failures of critical security control systems including
  logging).

## Evidence
- Ticket or SIEM case per daily review with reviewer, timestamp, findings, and actions; or SIEM report
  acknowledgement workflow.
- Exceptions escalated per incident response process with ticket links.
- Auditors sample days: gaps (weekends, holidays) are findings, so assign coverage.

## Automate
- SIEM correlation rules and scheduled searches generate the daily summary; analysts review exceptions only.
- SOAR enriches alerts (asset owner, user details) and opens tickets.
- Retain review records as long as logs (PCI: 12 months with 3 months immediately available).

## Gotchas
- "Reviewed" checkboxes without findings recorded for months look like rubber-stamping.
- Reviews that depend on one person fail during absences; rota and runbooks.
- Tuning: if a daily report always has hundreds of items, it is not being reviewed; fix the report.

## Verify
For a random sample of days, evidence shows completed reviews with any anomalies ticketed; log source health
alerts fired and were resolved during the period.
