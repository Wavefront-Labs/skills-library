---
id: computing-software.cloud-infrastructure-engineering.google-cloud.fabric-fast-stages-landing-zone
name: fabric-fast-stages-landing-zone
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, landing-zone, fabric-fast, fast-stages, fast-bootstrap, cloud-foundation-fabric, terraform]
level: advanced
status: draft
description: "Stand up a Google Cloud landing zone with Cloud Foundation Fabric FAST: bootstrap as org admin, migrate state, chain stages via the outputs bucket, and run later stages from CI."
sources: ["https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/fast", "https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/blob/master/fast/README.md", "https://cloud.google.com/architecture/landing-zones"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fabric FAST stages

FAST (in `GoogleCloudPlatform/cloud-foundation-fabric/fast`) is a set of Terraform root
modules ("stages") that build an org in layers, each run by a different service account with
just enough permissions. **Pin a release tag**; stage names and variables change between
major versions (recent releases merged bootstrap and resource management into a YAML-driven
`0-org-setup` stage). Read the README of the tag you pin.

## 1. Stage layout (classic naming)
| Stage | Builds | Runs as |
|---|---|---|
| 0-bootstrap | automation project, IaC SAs and state buckets, org-level IAM, log sinks, billing export | org admin user once, then its own SA |
| 1-resman | top folders (networking, security, teams), per-stage SAs and buckets | bootstrap SA |
| 2-networking-* | hub/spoke or shared VPC variants, DNS, NAT, VPN | networking SA |
| 2-security | KMS, Secret Manager, VPC-SC | security SA |
| 2-project-factory / 3-* | team projects, GKE, data platform | per-stage SAs |

Stages talk through **generated files**: each stage writes `providers/<next>-providers.tf`
and `tfvars/<stage>.auto.tfvars.json` to an outputs GCS bucket (and optionally a local dir).

## 2. First run
```bash
cd fast/stages/0-bootstrap
gcloud auth application-default login            # as an org admin with the prerequisite roles
cp terraform.tfvars.sample terraform.tfvars      # organization id/domain/customer_id, billing account, prefix, groups
terraform init && terraform apply -var bootstrap_user=$(gcloud config get-value account)
# switch to the generated provider (GCS backend + SA impersonation) and move state
gcloud storage cp gs://<prefix>-prod-iac-core-outputs-0/providers/0-bootstrap-providers.tf ./
terraform init -migrate-state
terraform apply          # without bootstrap_user: removes the human's temporary roles
```

## 3. Each subsequent stage
```bash
cd ../1-resman
gcloud storage cp gs://<prefix>-prod-iac-core-outputs-0/providers/1-resman-providers.tf ./
gcloud storage cp gs://<prefix>-prod-iac-core-outputs-0/tfvars/0-globals.auto.tfvars.json ./
gcloud storage cp gs://<prefix>-prod-iac-core-outputs-0/tfvars/0-bootstrap.auto.tfvars.json ./
terraform init && terraform apply
```
Bootstrap can create CI/CD (GitHub/GitLab Workload Identity Federation and repos per stage);
after stage 1, run stages from pipelines, not laptops.

## Gotchas
- The `prefix` is baked into every bucket and project ID; choose it once (short, globally unique).
- Prerequisite roles for the bootstrap user include Organization Admin, Billing Account Admin (or user on an external billing account), Org Policy Admin; missing one fails late.
- Do not edit generated provider files; re-copy after re-running the upstream stage.
- Upgrading FAST across releases means reading the CHANGELOG for moved resources — expect `terraform state mv` / `moved` blocks.

## Verify
- [ ] `terraform plan` in every stage is clean when run as its own SA from CI.
- [ ] The bootstrap user no longer has org-level roles after the second apply.
- [ ] The outputs bucket holds provider and tfvars files for each applied stage.
