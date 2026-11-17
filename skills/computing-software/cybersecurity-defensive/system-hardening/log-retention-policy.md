---
id: computing-software.cybersecurity-defensive.system-hardening.log-retention-policy
name: log-retention-policy
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [audit-log-management, log-retention-policy, data-retention, hot-warm-cold, legal-hold, compliance-retention, m-21-31]
level: practitioner
status: docs-checked
description: "Define a security log retention policy: map legal minimums, tier hot, warm and archive storage, protect integrity, and handle legal holds and deletion."
sources: ["https://csrc.nist.gov/pubs/sp/800/92/final", "https://learn.microsoft.com/en-us/purview/audit-solutions-overview", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log retention policy

**Goal:** logs are kept long enough to investigate breaches and meet obligations, cheaply, immutably, and deleted when they should be.

## Inputs
- Regulatory minimums: list every standard and law that applies to you (PCI DSS Requirement 10, HIPAA, SOX, US OMB M-21-31 for federal agencies, sector and national laws) and take the exact durations from the current text of each; do not copy figures from memory.
- Investigation reality: breaches are often found late, so long retention of authentication, DNS, proxy, EDR and cloud control-plane logs pays off.
- Privacy law (GDPR storage limitation): retain personal data in logs no longer than necessary; justify durations.

## Policy table
Set the durations from the legal inputs above and your investigation needs; the columns are the decision to record.

| Log class | Hot (searchable) | Total retention | Notes |
|---|---|---|---|
| Identity/auth (AD, IdP) | per policy | per policy | |
| Cloud control plane (CloudTrail, Activity Log) | per policy | per policy | cheap, high value |
| EDR telemetry | vendor limit | exported copy | export raw if vendor limits |
| Firewall/proxy/DNS | per policy | per policy | high volume - compress |
| Application/audit trails | per policy | per business/legal | |

## Implementation
- Tiering: SIEM hot index -> warm/cheaper tier -> object storage archive. Make sure archived data can be restored or queried within an agreed time.
- Integrity: WORM/immutability (S3 Object Lock compliance mode, where no user including the root user can delete or overwrite a protected version until retention ends; or your cloud's equivalent), separate account/subscription, restricted delete rights, hashes for exported batches.
- Lifecycle rules automate deletion at end of retention.

## Legal hold
A process to suspend deletion for specific sources/time ranges when litigation or investigations require it (S3 Object Lock legal hold, which has no expiry until removed, or your platform's equivalent). Document who can apply and release.

## Gotchas
- Retention configured in the SIEM but raw logs on hosts rotate after a week and forwarding gaps are unrecoverable.
- Vendor SaaS retention can be shorter than policy (Microsoft 365 Audit (Standard) keeps records 180 days by default, with longer defaults for some Entra ID, Exchange, OneDrive and SharePoint records) - check each vendor and export.

## Verify
- [ ] Each log class has a documented retention, legal basis and implemented lifecycle rule.
- [ ] Restore test of data near the end of its retention period succeeds within the target time.

## Checked
2026-10-31. Confirmed: S3 Object Lock compliance mode and legal hold behaviour (AWS S3 User Guide); Microsoft Purview Audit (Standard) 180-day default and longer default retention for some services. Removed: all PCI DSS, HIPAA, SOX and OMB M-21-31 durations (the M-21-31 PDF could not be read as text, PCI DSS is blocked), the tier durations, EDR vendor retention, and named Azure, Splunk and Sentinel archive products, none of which were confirmed on fetched pages.
Method: documentation only; no commands were run.
