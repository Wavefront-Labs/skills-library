---
id: computing-software.cloud-infrastructure-engineering.google-cloud.access-transparency-logs
name: access-transparency-logs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, assured-workloads, access-transparency-logs, google-personnel-access, justification-reasons, compliance-logging]
level: practitioner
status: docs-checked
description: "Verify Access Transparency is on for the organization, understand logs of Google personnel access and their justifications, route them to your SIEM, and pair with Access Approval."
sources: ["https://docs.cloud.google.com/assured-workloads/access-transparency/docs/overview", "https://docs.cloud.google.com/assured-workloads/access-transparency/docs/enable"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access Transparency logs

Access Transparency logs record the actions Google personnel take when accessing Customer Data: affected resource and action, time, the reason for the action and accessor information. Cloud Audit Logs records what your own organization's members did; Access Transparency records what Google personnel did, and the two together cover both. Access Transparency is a default security control for every Google Cloud organization.

## Verify it is enabled
- Need `roles/accessapproval.viewer` or Access Transparency Admin (`roles/axt.admin`).
- Console: Security > Access Approval, Home tab shows Access Transparency enabled; or IAM > Settings at the organization level.
- If it is disabled, the Access Approval UI may be inaccessible until it is re-enabled.

## Using the logs
- Every access requires a valid justification; the justification reason codes are listed in the Access Transparency docs ("Justification reason codes"), so take reason values from there.
- Only services listed under "Supported services" produce Access Transparency logs.
- Route them with your security log sinks and alert on reasons you do not expect.

## With Access Approval
If you need to approve access requests by Google personnel before they happen, use Access Approval; Access Transparency logs the access itself.

## Gotchas
- Not every service is covered; check the supported services list.
- Pricing: see the Access Transparency pricing page.

## Verify
- [ ] The organization IAM Settings page shows Access Transparency enabled.

## Checked
2026-10-31. Confirmed on the Access Transparency overview and enabling pages: default control for every organization, required roles, console paths, purpose of the logs, justification requirement, supported-services list. Removed: support-plan requirement, manual enable step, log name and gcloud read command, reason-type enum list and field names, free-of-charge claim (not confirmed on the fetched pages).
Method: documentation only; no commands were run.
