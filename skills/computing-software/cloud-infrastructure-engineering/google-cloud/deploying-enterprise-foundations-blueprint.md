---
id: computing-software.cloud-infrastructure-engineering.google-cloud.deploying-enterprise-foundations-blueprint
name: deploying-enterprise-foundations-blueprint
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, shared-responsibility, security-foundations-deploy, enterprise-foundations-deploy, terraform-example-foundation, landing-zone]
level: sme
status: docs-checked
description: "Deploy Google's enterprise foundations blueprint (terraform-example-foundation): foundation and infrastructure pipelines, stages 0-5, Cloud Build controls and branching."
sources: ["https://cloud.google.com/architecture/security-foundations", "https://cloud.google.com/architecture/security-foundations/deployment-methodology"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying the enterprise foundations blueprint

The enterprise foundations blueprint (formerly the security foundations blueprint) pairs a guide with the
`terraform-example-foundation` GitHub repository holding the deployable Terraform. It is deployed with a GitOps flow:
Terraform for IaC, a Git repository for version control and approval, and Cloud Build for CI/CD. Clone or fork the repo
into your own Git repository, then follow each stage's README, implementing stages sequentially.

## Pipeline layers
- **Foundation pipeline**: foundation resources used across the platform, owned by a single central team; it also sets
  up the infrastructure pipelines.
- **Infrastructure pipeline**: projects and workload infrastructure (VMs, databases). The blueprint sets up one per
  business unit, in a dedicated project in the common folder, each with a service account that can deploy only to that
  business unit's projects. A single shared pipeline is the alternative.
- **Application pipeline**: workload artifacts (images, containers). Not deployed by this blueprint; see the
  enterprise application blueprint.

## Stages
| Stage | Creates |
|---|---|
| `0-bootstrap` | Bootstraps the organization and the CI/CD pipeline: a CICD project with the Cloud Build foundation pipeline, and a seed project with the Cloud Storage buckets holding Terraform state (protected by Object Versioning) and the highly privileged service accounts the pipeline uses |
| `1-org` | Top-level shared folders, shared-services projects, organization-level logging, baseline security through organization policies |
| `2-environments` | Development, non-production and production environments |
| `3-networks-dual-svpc` or `3-networks-hub-and-spoke` | Shared VPCs in the chosen topology and associated network resources |
| `4-projects` | Folder structure, projects and an infrastructure pipeline |
| `5-app-infra` (optional) | Example workload projects with a Compute Engine instance via the infrastructure pipeline |

## Cloud Build controls to keep (or mirror in other CI)
- Two build configurations: `cloudbuild-tf-plan.yaml` validates with policy checks and a Terraform plan, then
  `cloudbuild-tf-apply.yaml` applies the result; each stage repository has two triggers.
- Terraform policy checks: Open Policy Agent constraints (forked from GoogleCloudPlatform/policy-library) enforced via
  policy validation in the Google Cloud CLI; a failing check stops the apply.
- Least privilege: a separate service account per stage, each trigger running as its stage's account.
- Cloud Build private pools (optionally inside a VPC Service Controls perimeter) and a custom builder with pinned
  library versions to run Terraform.
- Optional manual approval before a build runs.

## Branching strategy
Persistent branches `development`, `non-production` and `production` mirror the environments, plus ephemeral feature
branches. Enforce approved pull requests. A PR to `development` triggers plan and validate; merging triggers apply to
the development environment; promote by PR to `non-production`, then `production`.

## Gotchas
- Bootstrap is the privileged step; afterwards the pipelines act as the service accounts managed in the seed project.
- Review the organisation policies in `1-org` against any existing projects before applying to a non-empty organisation.

## Verify
- [ ] Each stage's pipeline applies with no drift on re-plan; policy checks fail a deliberately non-compliant change.

## Checked
2026-11-09: confirmed against the blueprint overview and Deployment methodology pages (pipelines, stage table, Cloud
Build controls, branching). Removed unconfirmed specifics: group names, deploying-user role list, tool versions, CI
alternatives, example commands, VPC-SC dry-run and quota gotchas, and the exact stage 1 shared project list.
Method: documentation only; no commands were run.
