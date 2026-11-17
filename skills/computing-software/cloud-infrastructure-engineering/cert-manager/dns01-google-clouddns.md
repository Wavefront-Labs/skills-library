---
id: computing-software.cloud-infrastructure-engineering.cert-manager.dns01-google-clouddns
name: dns01-google-clouddns
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [clouddns, google, gcp, dns01, workload-identity, serviceaccountsecretref]
level: practitioner
status: docs-checked
description: "Configure cert-manager DNS01 with Google Cloud DNS using a service account key Secret or GKE Workload Identity, with required roles and the secret-not-found pitfall."
sources:
  - https://cert-manager.io/docs/configuration/acme/dns01/google/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Solver fields: `spec.acme.solvers[].dns01.cloudDNS.project` (GCP project ID) and, for static credentials only, `serviceAccountSecretRef.name` and `.key` (here `key.json`).

Static credentials:
1. `gcloud iam service-accounts keys create key.json --iam-account dns01-solver@$PROJECT_ID.iam.gserviceaccount.com`
2. `kubectl create secret generic clouddns-dns01-solver-svc-acct --from-file=key.json`
3. Rotate periodically; the local `key.json` can be deleted afterwards.

Workload Identity on GKE: omit `serviceAccountSecretRef`. In GCP bind `roles/iam.workloadIdentityUser` to `serviceAccount:$PROJECT_ID.svc.id.goog[cert-manager/cert-manager]`; annotate the cert-manager ServiceAccount with `iam.gke.io/gcp-service-account` (Helm `serviceAccount.annotations`). Ambient credentials are enabled for ClusterIssuer and disabled for Issuer; enable for Issuers with `--issuer-ambient-credentials`.

Roles: `roles/dns.admin` is the convenience choice. Least privilege needs `dns.resourceRecordSets.*`, `dns.changes.*` and `dns.managedZones.list`. Without `dns.admin`, the GKE node service account needs the `https://www.googleapis.com/auth/cloud-platform` scope.

Pitfalls:
- The zone must be a Public DNS Zone so the challenge checker can query it.
- ClusterIssuer Secrets go in the cluster resource namespace (default `cert-manager`); Issuer Secrets in the Issuer's namespace. A "secret not found" error usually means the wrong namespace.

## Checked

2026-11-03. Confirmed on the cert-manager Google CloudDNS page (configuration/acme/dns01/google): solver fields, key creation and Secret commands, Workload Identity binding and annotation, ambient credentials defaults and flag, dns.admin versus custom role permissions, access scope, public zone requirement, namespace pitfall. Nothing removed.
Method: documentation only; no commands were run.
