---
id: computing-software.cloud-infrastructure-engineering.google-cloud.terraform-example-foundation-stages-and-groups
name: terraform-example-foundation-stages-and-groups
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, landing-zone, terraform-example-foundation, example-foundation-stages, 0-bootstrap, foundation-groups, grp-gcp-groups, enterprise-foundations-blueprint]
level: advanced
status: draft
description: "Deploy Google's terraform-example-foundation: required groups, 0-bootstrap seed and CI/CD projects, then 1-org through 5-app-infra via per-environment branches and tf-wrapper."
sources: ["https://github.com/terraform-google-modules/terraform-example-foundation", "https://cloud.google.com/architecture/security-foundations", "https://github.com/terraform-google-modules/terraform-example-foundation/blob/master/0-bootstrap/README.md"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# terraform-example-foundation stages and foundation groups

The reference implementation of Google's Enterprise Foundations Blueprint.

## 1. Groups first
The foundation grants org roles **only to groups**. `0-bootstrap` takes a `groups` variable
(and can create them through the Cloud Identity API when `create_required_groups = true`):
| Group (typical name) | Purpose |
|---|---|
| `gcp-organization-admins@` | org administration |
| `gcp-billing-admins@` | billing account |
| `gcp-billing-data@` | read billing export |
| `gcp-audit-data@` | read audit log exports |
| optional: `gcp-security-reviewer@`, `gcp-network-viewer@`, `gcp-scc-admin@`, `gcp-global-secrets-admin@`, `gcp-kms-admin@` | least-privilege functional roles |

## 2. Stage map
| Stage | Creates |
|---|---|
| 0-bootstrap | seed project (state bucket, Terraform SAs per stage), CI/CD project (Cloud Build default; GitHub Actions, GitLab, Jenkins, Terraform Cloud variants) |
| 1-org | org policies, `fldr-common` with logging, SCC notifications, billing export, DNS/interconnect hubs |
| 2-environments | `development`, `nonproduction`, `production` folders with env KMS and secrets projects |
| 3-networks-svpc or 3-networks-hub-and-spoke | shared VPCs per env, DNS, NAT, firewall policies, VPC-SC perimeters |
| 4-projects | business-unit folders and service projects attached to the shared VPCs |
| 5-app-infra | example workload (e.g. a VM) deployed through its own pipeline |

## 3. Workflow
```bash
cd 0-bootstrap && cp terraform.example.tfvars terraform.tfvars   # org_id, billing_account, groups, parent_folder
terraform init && terraform apply                                # locally, as an org admin
terraform output                                                  # seed/cicd project ids, SA emails, state bucket
# move state into the new bucket (backend.tf.example -> backend.tf), terraform init -migrate-state
```
From 1-org on, each stage lives in its own repo (`gcp-org`, `gcp-environments`, `gcp-networks`,
`gcp-projects`) and **branches map to environments** (`development`, `nonproduction`,
`production`, plus `plan`). Push to a branch → pipeline runs `tf-wrapper.sh plan/apply`
for that env with that stage's SA. Locally: `./tf-wrapper.sh init production` etc.

## Gotchas
- Order is strict: 3-networks needs 2-environments outputs, 4-projects needs the network outputs (via remote state in the seed bucket).
- Org policies from 1-org (e.g. no external IP, DRS) apply immediately; deploy into a test org or folder first.
- Hub-and-spoke vs shared-VPC is chosen at stage 3 and is costly to change later.
- Quota for projects per billing account is often hit in 4-projects; request an increase early.

## Verify
- [ ] Every org-level IAM binding is to a group from the table.
- [ ] Each stage's pipeline plan on `production` is clean.
- [ ] The human bootstrap identity holds no standing org roles afterwards.
