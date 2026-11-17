---
id: computing-software.cloud-infrastructure-engineering.google-cloud.attached-service-accounts-scopes-and-the-default-sa
name: attached-service-accounts-scopes-and-the-default-sa
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, service-accounts, default-service-account, attached-service-account, scopes-vs-iam, access-scopes, cloud-platform-scope, compute-default-service-account, per-workload-service-account, service-account-user, metadata-server-tokens, gke-node-service-account]
level: practitioner
status: docs-checked
description: "Attach a dedicated service account per workload to VMs, GKE node pools, Cloud Run, Functions and Cloud Build; know access scopes vs IAM; retire the Compute default account."
sources: ["https://cloud.google.com/compute/docs/access/service-accounts", "https://cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances", "https://cloud.google.com/iam/docs/best-practices-service-accounts", "https://cloud.google.com/run/docs/securing/service-identity"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attached service accounts, scopes and the default SA

**Goal:** every runtime (VM, node pool, Cloud Run service, function, build) runs as its own least-privilege
service account, with tokens from the metadata server and no scope surprises.

## 1. The model
When a service account is attached to a compute resource, processes on it request access tokens and ID tokens
from the metadata server and authenticate as that account; no key file is needed. Anyone who can run code or get a
shell on the resource can use everything the service account can, and by default any process on a VM, even a
low-privilege user, can reach the metadata server. Letting a user attach a service account needs
`iam.serviceAccounts.actAs`, which `roles/iam.serviceAccountUser` includes; grant it narrowly so a developer cannot
launch a VM as a privileged deployer account:
```bash
gcloud iam service-accounts add-iam-policy-binding <SA_EMAIL> --member="user:<USER_EMAIL>" --role=roles/iam.serviceAccountUser
```
The IAM best-practices page says to attach a service account when the workload runs on a Google Cloud resource,
and to use Workload Identity Federation for GKE to give service accounts to pods.

## 2. Scopes vs IAM (Compute Engine VMs)
Access to resources from an instance is limited by both the roles on the attached service account and the instance's
access scopes: both must allow it. Access scopes are the legacy method; they set the default OAuth scopes for the
gcloud CLI and client libraries on the VM, apply per VM for its lifetime, and do not apply to gRPC calls. A new VM gets
a default scope set that includes `devstorage.read_only`, `logging.write`, `monitoring.write`, service control
and `trace.append`, so Cloud Storage writes through OAuth can fail even when IAM allows them.
Best practice: set the `cloud-platform` scope on the VM and control access with IAM roles on a dedicated service
account. The IAM page also says not to rely on access scopes for restriction.
Cloud Run's service identity is a service account only; there are no access scopes to set.

## 3. Attach per product
```bash
gcloud iam service-accounts create web-api --display-name="web-api runtime"
# Compute Engine
gcloud compute instances create web-1 --zone=<ZONE> --service-account=web-api@<PROJECT_ID>.iam.gserviceaccount.com --scopes=cloud-platform
# GKE node pool (workloads in pods: Workload Identity Federation for GKE)
gcloud container node-pools create np1 --cluster=<CLUSTER> --region=<REGION> --service-account=gke-nodes@<PROJECT_ID>.iam.gserviceaccount.com
# Cloud Run / functions
gcloud run deploy web-api --image=<IMAGE> --service-account=web-api@<PROJECT_ID>.iam.gserviceaccount.com
gcloud functions deploy <NAME> --gen2 --run-service-account=web-api@<PROJECT_ID>.iam.gserviceaccount.com ...
# Cloud Build
gcloud builds submit --service-account=projects/<PROJECT_ID>/serviceAccounts/ci@<PROJECT_ID>.iam.gserviceaccount.com ...
```
The scope alias `--scopes=cloud-platform` is recognised only by the gcloud CLI; the API needs the full URI
`https://www.googleapis.com/auth/cloud-platform`. Grant the account only the roles its workload needs.

## 4. Retire the default Compute service account
`<PROJECT_NUMBER>-compute@developer.gserviceaccount.com` exists in projects that have enabled the Compute Engine API.
Depending on organization policy it may be granted the Editor role automatically; Google strongly recommends
enforcing the `iam.automaticIamGrantsForDefaultServiceAccounts` constraint (enforced by default for organizations
created after 3 May 2024) and, if the account already has Editor, replacing it with narrower roles using Policy
Simulator first. Cloud Run uses this account as the service identity if you do not specify one.
Disabling or deleting it can break applications that depend on it; a deleted account can be recoverable within 30 days.
Create a dedicated account per workload instead, and have infrastructure code require `service_account` explicitly.

## 5. Check what a runtime is using
```bash
gcloud compute instances describe web-1 --zone=<ZONE> --format='yaml(serviceAccounts)'
```

## Gotchas
- Never set `GOOGLE_APPLICATION_CREDENTIALS` on a Cloud Run service, job or worker pool that uses its service identity; configure a user-managed service account instead.
- A service account used as the deployer is the runtime identity only if you also configure it in the Cloud Run settings.
- The Google APIs Service Agent (not the default account) creates and manages instances for managed instance groups and autoscaling; do not strip its permissions.
- Access scopes have no effect if the related API is not enabled on the service account's project.

## Verify
- [ ] No production VM shows the `-compute@developer` account in `serviceAccounts`.
- [ ] Production VMs use the `cloud-platform` scope with IAM doing the limiting.
- [ ] A developer without `serviceAccountUser` on the deployer account cannot create a VM with it.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Compute service account page, the create/enable page, the IAM service account best-practices
page and the Cloud Run service identity page: attachment and metadata server tokens, scopes plus IAM, default scopes,
`cloud-platform` best practice, default account Editor behaviour and constraint, Cloud Run default identity,
`actAs` and `serviceAccountUser`. Removed: metadata URLs and curl checks, the stopped-VM rule for changing the account,
MIG template advice, minimum role lists, the Cloud Build legacy default account note, the cross-project org policy name
and a muddled paragraph about guardrail constraints.
