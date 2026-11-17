---
id: computing-software.digital-forensics-incident-response.log-analysis.cloud-identity-and-saas-log-forensics
name: cloud-identity-and-saas-log-forensics
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [cloud-forensics, azure-ad, entra-id, sign-in-logs, cloudtrail, m365, unified-audit-log, oauth-consent-grant, business-email-compromise, impossible-travel, conditional-access, mfa-fatigue, app-registration, token-theft, dfir, saas-forensics]
level: advanced
status: draft
description: "Investigate account compromise and data access in cloud identity logs: Azure AD/Entra sign-in logs, AWS CloudTrail, M365 Unified Audit Log, and malicious OAuth app grants."
sources: ["https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-in-log-activity-details", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud identity and SaaS log forensics

**Goal:** investigate compromise in environments with no filesystem to image at
all — the evidence is entirely provider-side logs, and knowing which log answers
which question (and which doesn't exist at the retention tier you have) is the whole
skill. Complements
computing-software.digital-forensics-incident-response.log-analysis.windows-event-log-threat-hunting
(host logs) and feeds
computing-software.digital-forensics-incident-response.evidence-handling.cloud-and-legal-process-evidence-handling
when a provider log has already rolled off and needs legal process to recover.

## 1. Azure AD / Entra ID sign-in logs
- **Interactive vs non-interactive sign-ins** are separate log streams — a
  non-interactive sign-in (token refresh, service-to-service) can show legitimate-
  looking success even during an active token-theft compromise, because the attacker
  is replaying a stolen token rather than authenticating interactively. Check both.
- **"Impossible travel"** (two sign-ins from geographically implausible locations in
  too short a window) is a strong but not conclusive indicator — VPNs, corporate
  proxies and mobile carrier IP reassignment all produce false positives; corroborate
  with device ID, user agent and conditional access policy results in the same log
  entry rather than geography alone.
- **Conditional Access result field** on each sign-in shows whether MFA was satisfied,
  skipped (legacy auth path), or the policy didn't apply — a compromise via legacy
  authentication protocols (IMAP/POP/older Exchange clients) that bypass modern MFA
  enforcement shows as a "successful" sign-in with no MFA challenge at all; this is a
  common BEC entry vector and the log entry looks unremarkable unless you check this
  field specifically.
- **Risky sign-ins / risk detections** (Identity Protection) flag anomalous token use,
  password spray patterns, and known-malicious IP matches — available at higher
  licence tiers; check what's actually enabled for the tenant before concluding
  "no risk was flagged" means "no risk occurred."

## 2. Microsoft 365 Unified Audit Log (UAL)
- Covers mailbox access/rule changes, SharePoint/OneDrive file access, Teams activity
  — the primary source for "did the attacker read/exfiltrate mail or files" once
  inside. Look specifically for `New-InboxRule`/`Set-InboxRule` (mailbox rule
  persistence, e.g. auto-forwarding or hiding replies), `MailItemsAccessed` (bulk mail
  access, a strong exfiltration signal when counts spike), and
  `Add service principal`/consent events (below).
- **Retention is licence-tier dependent and often shorter than expected** — verify
  current tenant retention before assuming historical UAL data exists; this is the
  exact gap
  computing-software.digital-forensics-incident-response.evidence-handling.cloud-and-legal-process-evidence-handling's
  preservation-request guidance exists to catch before it's too late.

## 3. Malicious OAuth app consent
A major, easy-to-miss persistence mechanism: an attacker with brief account access
grants a malicious OAuth application (often disguised with a plausible name) consent
to `Mail.Read`/`Files.ReadWrite.All`-style scopes. This **survives a password reset**
— the app token keeps working until the grant itself is revoked. Check Entra's
"Enterprise applications" / app consent audit events for grants around the incident
window, especially any with broad delegated or application-level permissions granted
by a compromised user (admin consent grants are rarer and more significant). This is
one of the most common reasons "we reset the password, access continued" happens.

## 4. AWS CloudTrail
- Management-event CloudTrail (API calls: IAM changes, S3 bucket policy edits,
  snapshot/AMI creation for exfiltration) is on by default with a 90-day rolling
  history in the console's event history view, but **only** if a persistent trail to
  S3/CloudWatch was configured beforehand does data survive past that window or
  include data-events (S3 object-level GetObject, which is what actually proves
  exfiltration of specific objects) — data events are not captured by default at all.
  If no trail existed before the incident, there may be nothing to recover past 90
  days; say this explicitly rather than implying the gap is retrievable.

## Verify
- For every cloud log cited, record its actual retention window and whether the
  relevant event type (sign-in vs audit vs data-event) was enabled before the
  incident — don't assume coverage.
- Check both interactive and non-interactive sign-in logs, and the Conditional Access
  result field, before clearing a user account as "not compromised."
- Explicitly check for OAuth app consent grants before declaring an account-compromise
  incident closed after a password reset.

Unconfirmed: licence-tier retention figures and default-enabled event types change
with vendor policy updates — verify current values for the specific tenant/account
before relying on them in a report.
