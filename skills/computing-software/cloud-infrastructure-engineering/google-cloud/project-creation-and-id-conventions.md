---
id: computing-software.cloud-infrastructure-engineering.google-cloud.project-creation-and-id-conventions
name: project-creation-and-id-conventions
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, projects, project-creation, project-id-naming, gcloud-projects-create, project-id, project-number, enable-apis, gcloud-services-enable, project-naming-convention, default-service-account-removal]
level: practitioner
status: docs-checked
description: "Create GCP projects with gcloud projects create under the right folder, pick immutable project IDs with a naming convention, link billing and enable APIs in one script."
sources: ["https://cloud.google.com/resource-manager/docs/creating-managing-projects", "https://cloud.google.com/sdk/gcloud/reference/projects/create", "https://cloud.google.com/service-usage/docs/enable-disable"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Project creation and project ID conventions

**Goal:** every project is created the same way — right parent, right ID, billing linked,
baseline APIs on, default SA neutered — so nothing depends on who clicked what in the console.

## 1. The three identifiers
| | Mutable | Globally unique | Used by |
|---|---|---|---|
| Project **ID** (`acme-prod-payments-a1b2`) | no, ever | yes | gcloud, APIs, URLs |
| Project **name** | yes | no | console display |
| Project **number** | no | yes | used in resource names such as WIF pool paths |

An ID is 6 to 30 characters of lowercase letters, digits and hyphens (see the creating-projects page for the first and last
character rules), and is permanent after creation. A project name is 4 to 30 characters and can be edited at any time. Because the ID is
immutable, decide the convention before the first project.

Convention that survives reorganisations: `<org-short>-<env>-<workload>-<4 random>`
e.g. `acme-prd-payments-7k2q`. The random suffix avoids global collisions and stops people
guessing project IDs. Do not encode team names (teams change); encode environment (it never does).

## 2. Create
```bash
gcloud projects create acme-prd-payments-7k2q --name="Payments (prod)" \
  --folder=123456789012 --labels=env=prd,workload=payments,owner=payments-team
gcloud beta billing projects link acme-prd-payments-7k2q --billing-account=<BILLING_ACCOUNT_ID>
gcloud services enable compute.googleapis.com logging.googleapis.com monitoring.googleapis.com \
  --project=acme-prd-payments-7k2q
```
Required: the Project Creator role (`roles/resourcemanager.projectCreator`, which contains `resourcemanager.projects.create`) on the parent.
Project creation is quota-limited per user and service account; see the Resource Manager quotas and limits page before a migration wave.

## 3. Post-create baseline (script it)
1. Avoid the default network with the org policy `compute.skipDefaultNetworkCreation`.
2. Stop the automatic Editor grant to default service accounts with org policy `iam.automaticIamGrantsForDefaultServiceAccounts` (enforced by default for organisations created on or after 2024-05-03).
3. Enable the APIs the workload needs with `gcloud services enable`.
4. Add Essential Contacts and budget.

## Gotchas
- `gcloud projects create` takes `--folder` or `--organization` for the parent; set `--folder` always so projects do not land at the wrong level.

## Verify
- [ ] `gcloud projects get-ancestors <ID>` shows the intended folder chain.
- [ ] The project is linked to the billing account and the baseline APIs are enabled (check in the console or with the matching gcloud list commands).

## Checked

- Date: 2026-10-27
- Confirmed against the creating-projects page (project ID 6-30 characters, lowercase letters, numbers, hyphens, permanent after creation; name 4-30 characters, editable), gcloud references for `projects create` (`--folder`, `--organization`, `--name`, `--labels`), `beta billing projects link --billing-account`, `services enable`, `projects get-ancestors`, the roles page (Project Creator contains `resourcemanager.projects.create`) and the constraints list (`compute.skipDefaultNetworkCreation`, `iam.automaticIamGrantsForDefaultServiceAccounts`).
- Removed: 30-day ID reuse and reserved-word rules, the ~30-project quota figure, billing permission names, the Terraform block, default-VPC deletion command, `serviceusage` ordering claim, async/propagation notes and the unverified `billing projects describe` and `services list` verification commands.

Method: documentation only; no commands were run.
