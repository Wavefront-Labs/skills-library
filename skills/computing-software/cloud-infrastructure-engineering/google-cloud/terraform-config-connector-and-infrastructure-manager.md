---
id: computing-software.cloud-infrastructure-engineering.google-cloud.terraform-config-connector-and-infrastructure-manager
name: terraform-config-connector-and-infrastructure-manager
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, terraform, terraform-google-provider, config-connector, kcc, infrastructure-manager, deployment-manager, iac, infrastructure-as-code, gcs-backend, state-locking, impersonate-service-account, terraform-google-modules, cloud-foundation-toolkit, gcloud-terraform-vet, policy-validation, import-existing-resources, drift-detection]
level: practitioner
status: draft
description: "IaC on GCP: Terraform with the google provider (GCS state, impersonation, CFT modules, terraform vet), Config Connector for Kubernetes-native resources, Infrastructure Manager, DM migration."
sources: ["https://cloud.google.com/docs/terraform", "https://cloud.google.com/docs/terraform/best-practices-for-terraform", "https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/provider_reference", "https://cloud.google.com/config-connector/docs/overview", "https://cloud.google.com/infrastructure-manager/docs/overview", "https://cloud.google.com/docs/terraform/policy-validation", "https://cloud.google.com/deployment-manager/docs/deployment-manager-eol"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Terraform, Config Connector and Infrastructure Manager

**Goal:** every GCP resource is declared, reviewed and applied by a pipeline identity with
locked remote state, policy-checked before apply, and the right tool chosen per team (Terraform by default).

## 1. Terraform baseline
```hcl
terraform {
  required_version = ">= 1.8"
  required_providers { google = { source = "hashicorp/google", version = "~> 6.0" }, google-beta = { source = "hashicorp/google-beta", version = "~> 6.0" } }
  backend "gcs" { bucket = "prj-c-tfstate-<RANDOM>", prefix = "envs/prod/network" }   # versioned bucket, CMEK, uniform access, locked down
}
provider "google" {
  project = var.project_id
  region  = "europe-west1"
  impersonate_service_account = "tf-prod@prj-c-bootstrap.iam.gserviceaccount.com"   # humans/CI hold only serviceAccountTokenCreator
  default_labels = { managed_by = "terraform", env = "prod" }
  user_project_override = true
  billing_project       = var.project_id
}
```
- **State**: one bucket per org/env class, `prefix` per stack; GCS locks natively; enable object versioning (recover a bad state) and a lifecycle rule to trim versions; `prevent_destroy` on the bucket. Never commit state; never store secrets in state you cannot encrypt (CMEK on the bucket).
- **Identity**: impersonation (`impersonate_service_account`) or Workload Identity Federation from GitHub Actions/Cloud Build; no SA keys. Audit logs then show the human/CI principal via `serviceAccountDelegationInfo`.
- **Stacks**: small blast radius — `org/`, `networking/`, `projects/`, `<app>/` per env; ~100-300 resources per state. Use `terraform-google-modules` (CFT: `project-factory`, `network`, `kubernetes-engine`, `cloud-sql`, `lb-http`) or Fabric modules instead of raw resources for the complex ones.
- `google-beta` for pre-GA fields; `user_project_override` for APIs that bill the caller (e.g. Workflows, some data APIs).
- Daily `terraform plan -detailed-exitcode` in CI = drift detection; `google_*` data sources + `import` blocks (`import { to = google_storage_bucket.x, id = "name" }`) to adopt existing resources; `moved` blocks for refactors.

## 2. Policy before apply
`gcloud beta terraform vet plan.json --policy-library=./policy-library --project=<P>` evaluates the plan against **Policy Library** constraints (CFT/OPA: allowed locations, required labels, no public IPs, CMEK required…) and fails CI on violations; same constraints the org can enforce as org policies get caught earlier. Alternatives: OPA/conftest, Sentinel (HCP). Also `terraform validate`, `tflint` with the google ruleset, `trivy config`.

## 3. Config Connector (KCC)
Kubernetes CRDs for GCP resources (`StorageBucket`, `SQLInstance`, `IAMPolicyMember`, …) reconciled by a controller in GKE (add-on `--addons=ConfigConnector` or the manual operator). Namespaced mode maps each namespace to a project (`ConfigConnectorContext` with a GSA via Workload Identity). Good when a platform team hands app teams a Kubernetes-only interface (GitOps via Config Sync) and resources must self-heal; worse for org-level/bootstrap resources and for teams without Kubernetes. `cnrm.cloud.google.com/deletion-policy: abandon` annotation to detach without deleting; `kubectl get gcp` lists all.

## 4. Infrastructure Manager (managed Terraform)
```bash
gcloud infra-manager deployments apply projects/P/locations/europe-west1/deployments/net \
  --service-account=projects/P/serviceAccounts/tf-prod@P.iam.gserviceaccount.com \
  --git-source-repo=https://github.com/example/infra --git-source-directory=envs/prod/network --git-source-ref=main \
  --input-values=project_id=P,region=europe-west1
gcloud infra-manager deployments list --location=europe-west1; gcloud infra-manager revisions describe ...
```
Runs `terraform apply` in Google-managed Cloud Build with state in a Google-managed bucket, versions as **revisions**, previews (`deployments preview`), and locks. Use when you want Terraform without owning runners/state (also what Marketplace and some console flows use); you lose provider-version control nuances and custom runners — fine for small teams, not for the landing-zone stacks that need private pools and strict pinning (though `--worker-pool` exists).

## 5. Deployment Manager (end of life)
No new deployments; existing templates (Jinja/Python) should be migrated: `gcloud` DM export → `terraform import`/`import` blocks, or the Google-provided DM-to-Terraform conversion tooling. Abandon DM deployments (`gcloud deployment-manager deployments delete --delete-policy=ABANDON`) after Terraform owns the resources.

## Gotchas
- `google_project_iam_policy`/`_binding` are **authoritative** and will remove bindings (including Google service agents) you did not declare; prefer `google_project_iam_member`, or manage the full policy only in the org bootstrap stack.
- Enabling APIs (`google_project_service`) with `disable_on_destroy = true` can disable an API still in use elsewhere; set `false`.
- Resources that take minutes (Cloud SQL, GKE) exceed default timeouts; set `timeouts {}`; GKE node pool changes often force replacement — read the plan.
- Provider major upgrades (5→6) rename fields; pin and upgrade deliberately with `terraform plan` diffs reviewed.
- Terraform-managed org policies and tags need `--condition`-aware resources (`google_org_policy_policy` v2); the old `google_organization_policy` resource lacks dry-run and custom constraints.

## Verify
- [ ] `terraform plan` in CI runs as the impersonated SA (audit log shows delegation) and `terraform vet` blocks a resource with a disallowed location.
- [ ] State bucket shows versioning enabled, CMEK, no public access; two concurrent applies: the second waits on the lock.
- [ ] Daily drift job reports a manual console change (make one in sandbox) with exit code 2.
- [ ] Config Connector: `kubectl apply` of a `StorageBucket` creates the bucket in the namespace's project; deleting the CR with `abandon` leaves it.
