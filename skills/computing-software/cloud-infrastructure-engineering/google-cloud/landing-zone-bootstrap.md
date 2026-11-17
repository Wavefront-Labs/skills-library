---
id: computing-software.cloud-infrastructure-engineering.google-cloud.landing-zone-bootstrap
name: landing-zone-bootstrap
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, landing-zone, org-bootstrap, fabric-fast, terraform-example-foundation, project-factory, cloud-foundation-toolkit, cft, folder-structure, seed-project, terraform-state-bucket, security-foundations-blueprint, environment-folders, shared-vpc-host, org-design, enterprise-foundations]
level: advanced
status: docs-checked
description: "Bootstrap a GCP organization as code with Fabric FAST or terraform-example-foundation: seed project, state bucket, folders, org policies, Shared VPC."
sources: ["https://cloud.google.com/architecture/landing-zones", "https://github.com/terraform-google-modules/terraform-example-foundation", "https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/fast", "https://cloud.google.com/docs/enterprise/setup-checklist"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Landing zone bootstrap

**Goal:** an organization where every project is born from a factory with the right folder,
labels, APIs, IAM and network attachment, and where humans hold as little org-level write as possible.

## 1. Pick a reference, do not hand-roll
| Option | Shape | Choose when |
|---|---|---|
| **terraform-example-foundation** (Cloud Foundation Toolkit) | stages 0-bootstrap, 1-org, 2-environments, 3-networks-svpc or 3-networks-hub-and-spoke, 4-projects, 5-app-infra. Stage 0 is run manually; later stages run in your CI/CD tool (Cloud Build by default) | you want Google's opinionated landing zone layout |
| **Fabric FAST** (cloud-foundation-fabric) | numbered stages as composable root modules; the first stage deals with organization-wide security setup and the second partitions the hierarchy with guardrails; YAML-based factories for subnets, firewall rules and projects; CI/CD via Workload Identity Federation | you want a lightweight, customisable reference and will modify the code |
| Enterprise setup checklist (console) | click-through | small organisations without an IaC team |

Google's landing-zone design guide recommends infrastructure as code (for example Terraform) with a GitOps CI/CD pipeline so deployments are repeatable and controlled.

## 2. Stage 0: bootstrap (run once, by a human with the needed org-level roles)
- In terraform-example-foundation this creates a bootstrap folder holding `prj-b-seed` (stores Terraform state and holds the service accounts that create or modify infrastructure) and `prj-b-cicd` (holds the CI/CD tool).
- A distinct service account is created for each stage, granted only the IAM permissions that stage needs. Use the reference's role lists as the least-privilege starting point.
- With Cloud Build, triggers run `terraform plan` for non-environment branches and `terraform apply` on merge to an environment branch (development, nonproduction or production).

## 3. Later stages in terraform-example-foundation
- **1-org**: a common folder for shared-resource projects (examples named in the README: `prj-c-logging` as the destination for organization-wide sinks, `prj-c-billing-export`, `prj-c-scc` for Security Command Center notifications, `prj-c-kms`, `prj-c-secrets`) and a network folder for network projects, including one Shared VPC host project per environment.
- **2-environments**: per-environment folders and projects (development, nonproduction, production).
- **3-networks-svpc / 3-networks-hub-and-spoke**: create the actual Shared VPC networks in the host projects.
- **4-projects** and **5-app-infra**: workload projects and the infrastructure inside them.
- Org-wide log sinks live in the logging project and are created before workload projects exist.

## 4. Project factory
Model a project as a declarative record (YAML or tfvars) that a factory turns into a project with billing linked, APIs enabled, Shared VPC attachment, group-based IAM, labels and a budget. FAST ships a project factory stage; its README notes you can remove stages you do not need. Developers then request projects by pull request.

## Gotchas
- Stage 0 is run manually by a person with sufficient org permissions; everything after it should run through the pipeline.
- Project IDs are global and cannot be reused: use a prefix convention such as the reference's `prj-<env>-...` names.
- Keep `plan` on pull requests and require review before apply: a landing-zone pipeline has org-wide blast radius.

## Verify
- [ ] The organization IAM policy lists groups and the stage service accounts, not individual users beyond break-glass accounts.
- [ ] Creating a project by editing the factory record yields a project with billing, APIs, network attachment, labels and budget in one pipeline run.
- [ ] The central log project receives entries from a brand-new project without per-project configuration.

## Checked
2026-11-09. Confirmed in the terraform-example-foundation README (stage names, manual stage 0, `prj-b-seed` / `prj-b-cicd`, per-stage service accounts, Cloud Build trigger behaviour, common and network folders and the `prj-c-*` projects), the FAST README (stages, YAML factories, Workload Identity Federation CI/CD, removable project factory) and the Google landing-zones guide (IaC and GitOps advice). Removed: Jenkins, FAST stage numbering and names beyond the README text, state-bucket settings, the specific org-role and org-policy lists, tag keys, the YAML example, gcloud verify commands, cross-skill references and the security-foundations source (unread).
Method: documentation only; no commands were run.
