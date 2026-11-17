---
id: computing-software.cloud-infrastructure-engineering.google-cloud.wif-direct-resource-access-vs-impersonation
name: wif-direct-resource-access-vs-impersonation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workload-identity-federation, wif-direct-resource-access, principalset-identifiers, principal-identifiers, service-account-impersonation, iam]
level: practitioner
status: docs-checked
description: "Choose between granting federated principals (principal:// and principalSet://) roles directly on resources and impersonating a service account, with identifier syntax and limits."
sources: ["https://cloud.google.com/iam/docs/principal-identifiers", "https://cloud.google.com/iam/docs/workload-identity-federation", "https://cloud.google.com/iam/docs/federated-identity-supported-services", "https://cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Direct resource access vs service account impersonation

## Identifier syntax
| Who | Member string |
|---|---|
| One subject | `principal://iam.googleapis.com/projects/<PN>/locations/global/workloadIdentityPools/<POOL>/subject/<SUB>` |
| By attribute | `principalSet://iam.googleapis.com/projects/<PN>/locations/global/workloadIdentityPools/<POOL>/attribute.<NAME>/<VALUE>` |
| By group | `principalSet://iam.googleapis.com/projects/<PN>/locations/global/workloadIdentityPools/<POOL>/group/<GROUP_ID>` |
| Whole pool | `principalSet://iam.googleapis.com/projects/<PN>/locations/global/workloadIdentityPools/<POOL>/*` |
| GKE pods of one Kubernetes service account | `principal://iam.googleapis.com/projects/<PN>/locations/global/workloadIdentityPools/<PROJECT_ID>.svc.id.goog/subject/ns/<NS>/sa/<KSA>` |

Granting a role to a whole pool is risky; Google recommends limiting access with attributes and conditions.

## Direct access
```bash
gcloud storage buckets add-iam-policy-binding gs://artifacts \
  --role=roles/storage.objectViewer \
  --member="principalSet://iam.googleapis.com/projects/$PN/locations/global/workloadIdentityPools/github/attribute.repository/acme/app"
```
Google recommends direct resource access. The token exchange returns a federated access token; most
Google Cloud APIs accept it but some have limitations, so check the supported-products page per API.
Example limit: Cloud Storage identity federation works only with uniform bucket-level access buckets.

## Impersonation
The alternative: grant the service account `roles/iam.workloadIdentityUser` to the federated principal.
Use it when the API has limitations with federation. Example: federated identities cannot generate
Cloud Storage signed URLs.

## Decision
- Default to direct access where the supported-products page lists the API without a blocking limitation.
- Use impersonation per trust boundary (one SA per pipeline/environment), not one SA for everything.
- Mixed is fine: direct for reads, impersonation for steps that need an SA.

## Gotchas
- Use fully qualified resource names and the project **number**, not the ID, when granting roles to external identities.
- A service account access token lasts at most 1 hour by default; the maximum can be extended to 12 hours by organization policy.

## Checked
Date: 2026-10-31. Confirmed in the Google Cloud pages principal-identifiers (all identifier rows above),
workload-identity-federation access management (direct access recommended, impersonation alternative,
`roles/iam.workloadIdentityUser`, project number, whole-pool warning), federated-identity-supported-services
(Cloud Storage uniform bucket-level access, no signed URLs) and the restricting-service-accounts page
(1 hour default, 12 hour maximum). Removed unconfirmed claims: credential-config flag behaviour, ID token and
`signBlob` needs, Terraform/gsutil needing SA emails, attribute case sensitivity, organization policy
constraint names, and the audit-log field check. The `gcloud storage` command was checked against the CLI reference.
Method: documentation only; no commands were run.
