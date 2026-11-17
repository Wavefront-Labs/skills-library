---
id: computing-software.cybersecurity-defensive.security-operations.insider-threat-alert-triage
name: insider-threat-alert-triage
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [insider-threat-triage, insider-threat, alert-triage, data-exfiltration, ueba, dlp, soc]
level: advanced
status: draft
description: "Triage insider threat alerts (data exfiltration, unusual access, departing employee activity) with proportionality, HR/legal coordination and evidence preservation."
sources: ["https://www.cisa.gov/topics/physical-security/insider-threat-mitigation", "https://insights.sei.cmu.edu/library/common-sense-guide-to-mitigating-insider-threats-seventh-edition/", "https://www.cisa.gov/resources-tools/resources/insider-threat-mitigation-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Insider threat alert triage

Insider alerts involve a named employee. Errors harm people and expose the company legally; the
process is stricter than for external threats.

## Before you dig
- Confirm the case type is covered by your insider programme's authorised monitoring policy and
  that you are permitted to investigate (many programmes require HR/legal sign-off before
  examining content).
- Keep the circle small: need-to-know only; do not discuss in general SOC channels.

## Triage questions
1. **Signal**: what triggered (DLP volume, bulk download from SharePoint, USB copy, email to
   personal domain, access to unusual repositories, UEBA anomaly)?
2. **Context**: role and normal duties; is the activity plausible for the job? Peer comparison.
3. **Risk indicators**: resignation or notice period (HR feed), performance issues, access
   outside hours, use of personal cloud storage, attempts to evade controls (renaming files,
   encryption, disabling agents).
4. **Data**: what data, classification, volume, destination. Metadata first (file names, sizes,
   destinations) before reading content.
5. **Benign explanations**: project handover, sanctioned backup, manager-requested export.

## Outcome paths
- Benign: document the reason, close, consider policy tuning.
- Policy violation, low risk: refer to manager/HR per process.
- Suspected malicious: escalate to insider risk team, legal and HR; preserve evidence (mailbox
  hold, endpoint image, cloud audit export) before any confrontation or access removal.

## Tools
Microsoft Purview Insider Risk Management, DLP incident queues, UEBA risk scores, proxy and CASB logs,
M365 audit (`FileDownloaded`, `FileSyncDownloadedFull`).

## Gotchas
- Do not alert the subject (no access revocation before evidence preservation unless risk is
  immediate).
- Pseudonymised review where the platform supports it reduces bias until escalation.
- Jurisdictional privacy law (e.g. GDPR, works councils) can limit monitoring; follow the policy.

## Verify
Case file shows authorisation, evidence collected with chain of custody, benign explanations
considered, and the decision path with approvers.
