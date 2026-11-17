---
id: computing-software.cloud-infrastructure-engineering.google-cloud.infrastructure-manager-deployments
name: infrastructure-manager-deployments
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, infrastructure-as-code, infra-manager-deploy, gcloud-infra-manager, terraform, previews]
level: practitioner
status: docs-checked
description: "Run Terraform through Infrastructure Manager: gcloud infra-manager deployments apply from Git or GCS, previews, service account roles, and inspecting deployments and revisions."
sources: ["https://cloud.google.com/infrastructure-manager/docs/deploy-resources", "https://cloud.google.com/infrastructure-manager/docs/configure-service-account", "https://cloud.google.com/sdk/gcloud/reference/infra-manager"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Infrastructure Manager deployments

Infrastructure Manager (Infra Manager) runs Terraform for you using Cloud Build.

## 1. Service account
Create a deployment SA with `roles/config.agent` plus the roles the Terraform needs; you need
`roles/config.admin` and `iam.serviceAccountUser` on that SA.

## 2. Preview then apply
```bash
gcloud infra-manager previews create projects/<P>/locations/us-central1/previews/net-preview \
  --service-account=projects/<P>/serviceAccounts/im-deployer@<P>.iam.gserviceaccount.com \
  --git-source-repo=https://github.com/<ORG>/<REPO> --git-source-directory=envs/prod/networking --git-source-ref=<GIT_REF> \
  --input-values=project_id=<P>,region=us-central1

gcloud infra-manager deployments apply projects/<P>/locations/us-central1/deployments/prod-net \
  --service-account=projects/<P>/serviceAccounts/im-deployer@<P>.iam.gserviceaccount.com \
  --git-source-repo=https://github.com/<ORG>/<REPO> --git-source-directory=envs/prod/networking --git-source-ref=<GIT_REF> \
  --input-values=project_id=<P>,region=us-central1 --tf-version-constraint=<TF_VERSION>
```
Sources: Git (`--git-source-repo`, `--git-source-directory`, `--git-source-ref`), Cloud Storage (`--gcs-source`) or a local directory (`--local-source`). Omit `--tf-version-constraint` to get the latest supported Terraform version.

## 3. Inspect
```bash
gcloud infra-manager deployments describe projects/<P>/locations/us-central1/deployments/prod-net
gcloud infra-manager revisions list --deployment=projects/<P>/locations/us-central1/deployments/prod-net
gcloud infra-manager deployments export-statefile projects/<P>/locations/us-central1/deployments/prod-net
```

## Gotchas
- Terraform versions are limited to those Infra Manager supports; the console list depends on the region you pick.
- Deployments run as the service account you supply, so it needs the roles the Terraform resources require, not only `roles/config.agent`.

## Verify
- [ ] `deployments describe` shows a healthy state after apply; a re-preview shows no changes.

## Checked
2026-10-31. Confirmed against the Infra Manager deploy-resources page (`roles/config.admin`, Cloud Build, `--git-source-repo`/`--git-source-directory`/`--git-source-ref`, `--gcs-source`, `--local-source`, `--tf-version-constraint`, latest version default, supported-version list by region) and the service account page (`roles/config.agent`, `iam.serviceAccountUser`). Commands checked against the gcloud reference with check_commands.py. Removed unconfirmed claims: managed-state wording, preview export and `terraform show` steps, lock/unlock, `--import-existing-resources`, backend block advice, pinned Terraform and Git versions, ACTIVE/APPLIED states. The preview-infra source page returned 404 and was dropped.
Method: documentation only; no commands were run.
