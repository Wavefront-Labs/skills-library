---
id: computing-software.cloud-infrastructure-engineering.google-cloud.resource-labels-and-labelling-strategy
name: resource-labels-and-labelling-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, resource-labels, project-labels, labelling-strategy, labels, cost-allocation-labels, label-enforcement, labels-vs-tags, billing-export-labels, gcloud-labels, label-taxonomy]
level: practitioner
status: docs-checked
description: "Define a label taxonomy (env, owner, cost-centre, workload) that flows into billing export, apply it to projects and Compute resources, and query it."
sources: ["https://docs.cloud.google.com/resource-manager/docs/creating-managing-labels", "https://docs.cloud.google.com/compute/docs/labeling-resources", "https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery-tables/standard-usage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource labels and labelling strategy

**Goal:** every billable resource carries the few labels finance and ops need, applied by automation, so the
billing export can be sliced by team without anyone tagging after the fact.

## 1. What labels are
- Key/value pairs used to organise resources and track costs across teams or environments.
- Project labels apply to projects only (folders and organizations do not support labels) and do **not**
  propagate to child resources: label the service resources too.
- Compute Engine limits: up to 64 labels per resource; keys 1-63 characters and must start with a lowercase letter
  (or international character); values may be empty and up to 63 characters; keys and values may contain only
  lowercase letters, numbers, underscores and dashes.
- Not every billing SKU supports labels (the page gives Pub/Sub egress billing SKUs as an example).

## 2. A taxonomy that works
| key | values | why |
|---|---|---|
| `env` | `prd`, `stg`, `dev`, `sbx` | cost split and policy |
| `owner` | team alias (`payments`) | who to page |
| `cost-centre` | finance code | chargeback |
| `workload` | application name | per-app cost |
Keep it to a handful of keys; every extra key is one more thing left blank. Values lowercase, no spaces.

## 3. Apply
```bash
gcloud projects update <PROJECT_ID> --update-labels=env=prd,owner=payments
gcloud projects update <PROJECT_ID> --remove-labels=KEY1,KEY2
gcloud compute instances update <VM> --zone=<ZONE> --update-labels=workload=api
gcloud compute disks update <DISK> --zone=<ZONE> --update-labels=owner=payments
```
The project form is the one shown on the Resource Manager labels page; the Compute forms are from the Compute
labelling page, which also covers the REST `setLabels` methods. Labels on a VM do not label its disks: set both.

## 4. Query in billing export
The standard usage export has `labels` (resource labels, key/value), `project.labels` (labels of the project
where usage occurred) and `credits` (with `credits.amount`).
```sql
SELECT (SELECT value FROM UNNEST(labels) WHERE key='owner') AS owner,
       SUM(cost) + SUM(IFNULL((SELECT SUM(c.amount) FROM UNNEST(credits) c),0)) AS net
FROM `<BILLING_DATASET>.gcp_billing_export_v1_<ID>`
WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY owner ORDER BY net DESC
```
Rows with `owner IS NULL` are unlabelled spend: report that number regularly. Group by `project.labels` as a
fallback for resources missing a label.

## Verify
- [ ] The null-`owner` share of spend is falling and reported regularly.
- [ ] A new VM and its disks both show the expected labels in `gcloud compute instances describe` and `disks describe`.

## Checked
2026-11-09. Confirmed against Create and update labels for projects, Labelling resources (Compute Engine) and the
standard usage cost data schema (searched for label and credit fields and limits, not read in full). The
`gcloud projects update --update-labels` flag was flagged as alpha-only by the reference check but appears in the
Resource Manager page, so it is attributed to that page. Removed: Terraform `default_labels` (registry page
unreadable), labels-versus-tags comparison, GKE label propagation, enforcement options (custom org policy
constraint, `gcloud terraform vet`, asset search), the `data-class` key, storage bucket command, and billing-export
timing claims.
Method: documentation only; no commands were run.
