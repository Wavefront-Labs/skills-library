---
id: computing-software.cloud-infrastructure-engineering.google-cloud.capping-usage-with-consumer-quota-overrides
name: capping-usage-with-consumer-quota-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [consumer-override, quota-override, quotas, cost-control, quota-preferences]
level: practitioner
status: docs-checked
description: "Cap a Google Cloud project quota below its default with a quota override, reset it, and know the roles, console steps and gcloud flags involved."
sources: ["https://docs.cloud.google.com/docs/quotas/view-manage", "https://docs.cloud.google.com/sdk/gcloud/reference/beta/quotas/preferences/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer quota overrides

**Goal:** limit blast radius and spend by capping how much of a quota one project may use.

## What it is
A quota override restricts usage of a resource by setting the quota value below the default quota value. It is also called capping usage. Overrides are not available to all services; check the quota and system limits documentation for the service. Adjustments that raise a quota are requests subject to review (Apply for higher quota in the console).

## Console
1. IAM & Admin > Quotas & System Limits.
2. Select the checkbox next to the quota, click **Edit**, enter the value in **New value**, then **Done** and **Submit request**.
3. If you see the checkbox "I understand that this request will remove any overrides", the new value is equal to or greater than the default and will remove the previous override.
4. To reset: filter with **Has override: True**; an **Override** marker appears next to such quotas; click it, tick **Reset value** to acknowledge, then click **Reset value**. Manually, set New value equal to the Default value shown under the quota name.

## CLI
`gcloud quotas info` and `gcloud quotas preferences` need the beta commands component installed. The beta create command:
```
gcloud beta quotas preferences create --service=SERVICE --project=PROJECT_ID --quota-id=QUOTA_ID --preferred-value=VALUE [--dimensions=region=REGION]
```
Required: `--preferred-value` (must be >= -1; -1 means unlimited), `--quota-id`, `--service`, and exactly one of `--folder`, `--organization`, `--project`. Optional: `--dimensions=[KEY=VALUE,...]`, `--preference-id`, `--email`, `--justification`. Two guard flags exist, both default false: `--allow-high-percentage-quota-decrease` (reduce the effective limit by more than 10 percent) and `--allow-quota-decrease-below-usage` (reduce below current usage). The command is beta and might change without notice.

## Permissions
View: Quota Viewer (`roles/servicemanagement.quotaViewer`). Request adjustments: Quota Administrator (`roles/servicemanagement.quotaAdmin`); the permissions required are `serviceusage.quotas.update` and `cloudquotas.quotas.update`. Roles can be granted on the project, folder or organization. Restrict who holds it.

## Scope
Quota increase adjustments are mostly project-level; decrease adjustments can be requested for project, organization and folder level quotas.

## Gotchas
- Quotas with a region or zone dimension are set per dimension (`--dimensions`); check which dimension the cap applies to.
- Capping below current usage needs `--allow-quota-decrease-below-usage` on the CLI; check the effect on running workloads before doing it.
- Record caps in IaC or documentation so they are not mistaken for a platform limit.

## Verify
The Quotas & System Limits page shows the quota with an Override marker (filter **Has override: True**) and the lower value.

## Checked
2026-11-08: confirmed against the Cloud Quotas "View and manage quotas" page and the `gcloud beta quotas preferences create` reference: override definition, console steps, roles and permissions, reset steps, flags and defaults. Removed: unsourced claims about budgets versus caps, autoscaling breakage, and per-user cap use cases; removed the page-less claim that exact flags must come from `--help`.
Method: documentation only; no commands were run.
