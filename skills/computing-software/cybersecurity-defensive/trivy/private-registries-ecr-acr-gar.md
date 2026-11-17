---
id: computing-software.cybersecurity-defensive.trivy.private-registries-ecr-acr-gar
name: private-registries-ecr-acr-gar
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [ecr, acr, gar, artifact-registry, azure-client-id, google-application-credentials, acrpull, irsa]
level: advanced
status: docs-checked
description: "Configure Trivy to scan from AWS ECR, Azure ACR and Google Artifact Registry using cloud SDK credentials and the least privileges each needs."
sources:
  - https://trivy.dev/latest/docs/guide/advanced/private-registries/ecr/
  - https://trivy.dev/latest/docs/guide/advanced/private-registries/acr/
  - https://trivy.dev/latest/docs/guide/advanced/private-registries/gar/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In the page's Helm-style values the IRSA annotation sits under `trivy.serviceAccount.annotations`, while the kube2iam or Kiam annotation sits under `podAnnotations`.
Trivy uses each cloud's Go SDK, so the `aws`, `az` and `gcloud` command line tools are not required.

AWS ECR: standard AWS CLI environment variables work. To grant pulls from a private ECR in Kubernetes, either annotate the Trivy service account with the role, as in `eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/IAM_ROLE_NAME` (the page's "IAM Role Service account" option), or annotate the pod with `iam.amazonaws.com/role: arn:aws:iam::ACCOUNT_ID:role/IAM_ROLE_NAME` when using kube2iam or Kiam.

Azure ACR: the service principal needs the `AcrPull` role. Create one scoped to the registry with `az ad sp create-for-rbac --name TrivyTest --role AcrPull --scope "/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.ContainerRegistry/registries/<registry_name>"`, then export `AZURE_CLIENT_ID` (appId), `AZURE_CLIENT_SECRET` (password) and `AZURE_TENANT_ID` (tenant). `TRIVY_USERNAME` must be set to an empty string.

Google Artifact Registry: the service-account credential file needs `roles/artifactregistry.reader`. Export `GOOGLE_APPLICATION_CREDENTIALS=/path/to/credential.json` (again with an empty `TRIVY_USERNAME`). The page's test pattern mounts the file into the `aquasec/trivy` container and scans `LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/IMAGE:TAG`.

## Checked

2026-11-03. Read and confirmed against the Private Registries overview page (and ACR, ECR, GAR subpages) on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: the 'IRSA' expansion (the page says IAM Role Service account).

Method: documentation only; no commands were run.
