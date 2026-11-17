---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.workload-identity
name: workload-identity
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, identity-architecture, workload-identity, workload-identity-federation, irsa, eks-pod-identity, azure-workload-identity, managed-identities, github-oidc, keyless-authentication, spiffe]
level: practitioner
status: docs-checked
description: "Authenticate workloads without static keys: EKS Pod Identity, AKS Workload Identity, Google Workload Identity Federation, GitHub OIDC claims, scoped trust, key removal."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html", "https://learn.microsoft.com/azure/aks/workload-identity-overview", "https://cloud.google.com/iam/docs/workload-identity-federation", "https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workload identity without static keys

## By runtime
| Runtime | Mechanism |
|---|---|
| VMs | cloud-attached identities: EC2 instance profiles, Azure managed identities, attached service accounts |
| Kubernetes on AWS | EKS Pod Identity (associates an IAM role with a Kubernetes service account) or IAM roles for service accounts (IRSA) |
| Kubernetes on Azure | AKS Workload Identity (federated identity credentials on a managed identity) |
| CI/CD | **OIDC federation**: the job requests a short-lived OIDC token and presents it to the cloud provider |
| Cross-cloud / on-prem | Google Workload Identity Federation accepts X.509 client certificates, AWS or Azure workloads, on-premises Active Directory, GitHub/GitLab and any OIDC or SAML 2.0 provider |
| Service-to-service | SPIFFE/SPIRE or mesh-issued identities (not covered by the cited pages) |

## What the vendors document
- EKS Pod Identity is described as simpler than IRSA because it does not use OIDC identity providers.
  It uses a single IAM principal added to the role trust policy, instead of a separate principal
  per cluster as IRSA does, and access is logged through CloudTrail.
- AKS Workload Identity: at most 20 federated identity credentials per managed identity, and a
  newly added credential takes a few seconds to propagate. Direct federation needs a token whose
  audience is `api://AzureADTokenExchange`; reusing the identity-binding token file
  (`api://AKSIdentityBinding`) for direct federation fails with AADSTS700212. Identity bindings let
  several clusters share one managed identity through one federated credential.
- Google Workload Identity Federation: for OIDC and SAML providers you must supply the attribute
  mapping; `google.subject` is required, unique and at most 127 characters. For AWS it maps to the
  caller ARN by default, for X.509 to the certificate subject common name.

## Scope trust tightly
- GitHub's OIDC token carries a `sub` claim. Documented examples:
  `repo:octo-org/octo-repo:environment:prod` and `repo:my-org/my-repo:ref:refs/heads/main`. The cloud
  provider checks the subject and other claims against the conditions on the role trust definition,
  so trust one exact subject per role. A wildcard such as `repo:org/*` would let any repository assume the role.
- GitHub documents that repositories created after 15 July 2026 use an immutable default subject
  format that includes owner and repository IDs; check the OpenID Connect reference before writing conditions.
- One identity per workload, least privilege.

## Remove keys
1. Inventory existing access keys, service account keys and client secrets with last-used dates.
2. Migrate each consumer to federation; disable then delete keys.
3. Prevent new ones with the organisation-level policy controls your cloud offers (look up the
   current policy name in that cloud's docs).

## Verify
- [ ] No service account keys or IAM user access keys used by workloads.
- [ ] CI role assumption from an unauthorised branch fails.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the four cited pages: Pod Identity versus IRSA, the 20-credential AKS limit, the two token
audiences and AADSTS700212, Google federation sources, `google.subject` rules, GitHub `sub` examples and
the July 2026 subject-format note. Removed as uncheckable from the cited pages: IMDSv2, IAM Roles
Anywhere, the named GCP organisation policy, the SCP example, and the `aud = sts.amazonaws.com` condition.
