---
id: computing-software.systems-network-administration.patch-management.emergency-change-approval-for-patching
name: emergency-change-approval-for-patching
category: computing-software
field: systems-network-administration
product: patch-management
tags: [emergency-change, ecab, change-enablement, emergency-patching, itil-4, pre-authorised-change]
level: practitioner
status: draft
description: "Run emergency changes for urgent patches: when they qualify, ECAB or delegated approval, minimum documentation up front, retrospective records, and pre-authorised emergency models."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-change-enablement
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Emergency change approval for patching

**Goal:** deploy an urgent fix within hours without bypassing control.

## Qualifies as emergency when
- A vulnerability is being actively exploited (KEV, vendor statement, own incident) on exposed or critical assets, or
- An outage or major incident needs a fix now.
"We forgot to raise the change" does not qualify.

## Approval path
- **Emergency change authority** (often called ECAB): a small named group able to convene in minutes (on-call change manager, service owner, security lead). One approver may be delegated for out-of-hours.
- Document at least: what, where (asset list), why (threat), risk and backout, who executes, approver and time.
- Full record completed retrospectively within an agreed window (e.g. two business days).

## Pre-authorised emergency model
Agree in advance a change model for "KEV patch on Tier 0/1": approved package source, test minimum (one pilot host, health check), deployment sequence, rollback. Under the model, the on-call change manager approves alone and the change is logged automatically.

## Execution
1. Pilot one representative host; health check.
2. Deploy in fast rings with short soak (minutes to an hour).
3. Communicate start, progress and completion to service desk and stakeholders.
4. Monitor closely for 24 hours.

## After
Retrospective record, post-implementation review, and if the same scenario recurs often, convert it into a standard change model.

## Gotchas
- High emergency-change volume is a symptom: routine patching is too slow or planning poor; report the ratio.
- Emergency does not mean untested; one pilot host is the minimum.

## Verify
Every emergency change has an approver and timestamp before implementation, and a completed record within the window.
