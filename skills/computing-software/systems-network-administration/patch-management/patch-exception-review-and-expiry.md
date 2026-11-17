---
id: computing-software.systems-network-administration.patch-management.patch-exception-review-and-expiry
name: patch-exception-review-and-expiry
category: computing-software
field: systems-network-administration
product: patch-management
tags: [exception-expiry, patch-exception, risk-acceptance, exception-process, residual-risk, poam]
level: practitioner
status: draft
description: "Run the lifecycle of patch exceptions: required fields, maximum durations by severity, periodic review, expiry enforcement and reporting so exceptions don't become permanent."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://csrc.nist.gov/pubs/sp/800/37/r2/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Patch exception review and expiry

An exception is a time-limited, owned risk acceptance for not remediating within SLA.
Without expiry, exceptions become the place vulnerabilities go to live forever.

## Required fields
| Field | Notes |
|---|---|
| Assets and findings/actions | specific hosts, not "all of app X" |
| Reason | vendor not supported, app incompatibility (ticket ref), no fix available, operational constraint |
| Compensating controls | what reduces risk now (segmentation, WAF rule, disabled feature) with evidence |
| Residual risk rating | after controls |
| Risk owner | business owner with authority, not the sysadmin |
| Approver | per severity (CISO for Critical/KEV) |
| **Expiry date** | hard maximum |
| Remediation plan | what will end the exception (upgrade project, vendor date) |

## Maximum durations (example)
| Priority | Max exception | Approver |
|---|---|---|
| P1 / KEV | 30 days, renewable once | CISO |
| P2 | 90 days | Security manager + risk owner |
| P3/P4 | 180 days | Risk owner |
No-fix-available cases: review at each vendor update; expiry tied to fix release + SLA.

## Review cadence
- Monthly: list exceptions expiring in the next 30 days to owners.
- At expiry: remediated → close; not → **re-approval with fresh justification** (counts as
  renewal, visible in metrics) or escalate. Expired-and-unrenewed shows as SLA breach.
- Quarterly: report counts, ages, renewals by business unit to leadership.

## Tooling
Use the vulnerability tool's accept-risk feature (Tenable "Accept", Qualys "Ignore" with
expiry, Defender "Exception") **with expiry**, linked to a GRC/ticket record; never suppress
findings without expiry. For FedRAMP/FISMA, track as POA&M items with milestones.

## Gotchas
- Blanket exceptions by plugin ID across the fleet hide new assets; scope by asset.
- Changing the asset (new IP, rebuild) can orphan the exception; re-link or re-approve.

## Verify
No active exception without expiry, owner and compensating control; zero expired-but-active
exceptions in the monthly report.
