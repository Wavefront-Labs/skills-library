---
id: computing-software.cloud-infrastructure-engineering.google-cloud.binding-kubernetes-service-accounts-to-iam-on-gke
name: binding-kubernetes-service-accounts-to-iam-on-gke
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gke-workload-identity, ksa-gsa-binding, kubernetes-service-account-binding, workload-identity-federation-for-gke, iam-gke-security-workloadidentityuser, principal-kubernetes, direct-iam-for-kubernetes, gke-metadata-server, workload-identity-annotation]
level: practitioner
status: docs-checked
description: "Give GKE pods a Google identity: grant IAM to the KSA principal directly or via the legacy KSA-to-GSA annotation, enable the metadata server, verify in-pod."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/how-to/workload-identity"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binding Kubernetes service accounts to IAM on GKE

**Goal:** a pod authenticates to Google APIs as *its own* identity (namespace + KSA), not as
the node, with the binding expressed in IAM and verifiable from inside the container.

## 1. Enable on cluster and node pools
```bash
gcloud container clusters update <C> --region=<R> --workload-pool=<PROJECT_ID>.svc.id.goog
gcloud container node-pools update <NP> --cluster=<C> --region=<R> --workload-metadata=GKE_METADATA
```
In Autopilot, Workload Identity Federation for GKE is always enabled. `--workload-metadata=GKE_METADATA` configures the node pool to use the GKE metadata server; a node pool without it does not give Pods their own identity, so check every pool.

## 2. Option A — direct IAM (no GSA, preferred)
Grant roles straight to the Kubernetes principal:
```bash
gcloud projects add-iam-policy-binding <P> --role=roles/storage.objectViewer \
  --member="principal://iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/<PROJECT_ID>.svc.id.goog/subject/ns/<NAMESPACE>/sa/<KSA>"
```
No annotation needed. For other principal identifier forms (for example a whole namespace) see the principal identifiers reference. Confirm that the Google APIs you call support federated principals (see the supported-services reference); if one does not, use Option B.

## 3. Option B — KSA impersonates a GSA (legacy, universal)
```bash
gcloud iam service-accounts create app-gsa
gcloud iam service-accounts add-iam-policy-binding app-gsa@<P>.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser --member="serviceAccount:<PROJECT_ID>.svc.id.goog[<NAMESPACE>/<KSA>]"
kubectl annotate serviceaccount <KSA> -n <NAMESPACE> iam.gke.io/gcp-service-account=app-gsa@<P>.iam.gserviceaccount.com
```
Grant the app's roles to `app-gsa`. Both the IAM allow policy binding and the annotation are required for this method.

## 4. Pod spec
```yaml
spec:
  serviceAccountName: <KSA>
  nodeSelector: { iam.gke.io/gke-metadata-server-enabled: "true" }   # Standard clusters only; Autopilot rejects this selector
```

## 5. Verify from inside
Run a Pod that uses `serviceAccountName: <KSA>` in `<NAMESPACE>` and call a Google API it should be allowed to use (for example list the bucket); the same call from a Pod using a different KSA should be denied. If the node service account is used instead, the Pod is on a node pool without the GKE metadata server or the KSA is wrong.

## Gotchas
- Option B member format is `serviceAccount:<PROJECT_ID>.svc.id.goog[<NAMESPACE>/<KSA>]`; quote it in shells and Terraform.
- The workload pool for a cluster is `<CLUSTER_PROJECT_ID>.svc.id.goog`.
- Do not mix Option A principals and Option B annotations for the same workload.

## Verify
- [ ] The Pod can call the intended API, and a Pod with the default KSA gets `PERMISSION_DENIED`.
- [ ] All prod node pools use the GKE metadata server (`--workload-metadata=GKE_METADATA`).
- [ ] Audit logs for the app's API calls show the intended principal, never the node service account.

## Checked

2026-10-24, GKE Workload Identity Federation how-to page on docs.cloud.google.com. Confirmed: `--workload-pool`, `--workload-metadata=GKE_METADATA`, Autopilot always on, the `principal://` format for direct IAM, legacy binding member format and `roles/iam.workloadIdentityUser`, annotation key, requirement of both binding and annotation, nodeSelector key (Standard only), supported-API caveat. Removed unconfirmed claims: gke-metadata-server DaemonSet description, namespace principalSet format, hostNetwork and startup-race notes, Terraform submodule, fleet pool form, curl metadata outputs.

Method: documentation only; no commands were run.
