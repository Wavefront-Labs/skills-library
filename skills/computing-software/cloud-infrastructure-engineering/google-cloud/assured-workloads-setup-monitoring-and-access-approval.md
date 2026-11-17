---
id: computing-software.cloud-infrastructure-engineering.google-cloud.assured-workloads-setup-monitoring-and-access-approval
name: assured-workloads-setup-monitoring-and-access-approval
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, assured-workloads, assured-workloads-create, folder-creation-assured, assured-workloads-monitoring, compliance-violations, data-boundary, regions-and-support-restriction, access-approval-config, approval-requests, audit-manager, compliance-manager]
level: advanced
status: docs-checked
description: "Create Assured Workloads folders for a compliance regime or data boundary, watch and remediate compliance violations, configure Access Approval, and produce audit evidence."
sources: ["https://docs.cloud.google.com/assured-workloads/docs/overview", "https://docs.cloud.google.com/assured-workloads/docs/monitor-folder", "https://docs.cloud.google.com/assured-workloads/docs/supported-products", "https://assuredworkloads.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assured Workloads: setup, monitoring and Access Approval

## 1. Create the workload (a controlled folder)
```bash
gcloud assured workloads create --organization=<ORG_ID> --location=eu \
  --display-name=eu-sovereign --compliance-regime=EU_DATA_BOUNDARY_AND_SUPPORT \
  --billing-account=billingAccounts/<BA> \
  --next-rotation-time=2027-01-01T00:00:00Z --rotation-period=7776000s
gcloud assured workloads describe <WORKLOAD_ID> --location=eu --organization=<ORG_ID>
```
Control packages include CJIS, IL2/IL4/IL5, ITAR, FedRAMP, healthcare and life sciences, and regional data boundaries such
as `EU_DATA_BOUNDARY_AND_SUPPORT`. Older enum names (for example `EU_REGIONS_AND_SUPPORT`, `HIPAA`, `HITRUST`) are legacy or
deprecated in the Assured Workloads API: list the current values in the API reference. The workload applies organization
policy constraints to the folder, and only the **supported products** for the control package may be used: check the list
before designing the architecture.

## 2. Monitor violations
```bash
gcloud assured workloads violations list --organization=<ORG_ID> --location=eu --workload=<WORKLOAD_ID>
gcloud assured workloads violations describe <VIOLATION> --organization=<ORG_ID> --location=eu --workload=<WORKLOAD_ID>
gcloud assured workloads violations acknowledge <VIOLATION> --organization=<ORG_ID> --location=eu --workload=<WORKLOAD_ID> --comment="Approved exception CHG-1234"
```
Violations come from changes that move a control away from the compliant value (for example changing an org policy
constraint of the control package). By default, members of the Legal category in Essential Contacts are emailed when a
violation occurs, is resolved or an exception is made. Fix by reverting the change; acknowledge only documented exceptions.

## 3. Access Approval
```bash
gcloud access-approval settings update --folder=<FOLDER_ID> --enrolled_services=all \
  --notification_emails=cloud-approvals@example.com
gcloud access-approval requests list --folder=<FOLDER_ID>
gcloud access-approval requests approve <REQUEST_NAME>
gcloud access-approval requests dismiss <REQUEST_NAME>
```
Access Approval is for approving Google personnel access requests; see the Access Approval docs for the settings and
request lifecycle before relying on the commands above.

## Gotchas
- Create resources inside the workload folder from day one.
- Changing a control package's org policy constraint creates a violation: use supported alternatives.

## Verify
- [ ] Creating a resource in a non-allowed region inside the folder fails with a location constraint.
- [ ] `violations list` is empty or every item has an acknowledged exception.
- [ ] A test Access Approval request reaches the approvers' mailbox.

## Checked
2026-10-28. Confirmed against the Assured Workloads overview and monitoring pages and the Assured Workloads API v1 discovery document
(`complianceRegime` values and deprecations; Legal Essential Contacts notification). Commands verified against the gcloud reference;
`--parent` removed (not a flag of `workloads create`). Removed: constraint names, Premium and retroactive-compliance claims,
Audit Manager and Access Approval KMS-signing details.
Method: documentation only; no commands were run.
