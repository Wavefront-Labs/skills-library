---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.non-human-identity
name: non-human-identity
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, identity-architecture, non-human-identity, service-accounts, service-principals, credential-rotation, secretless, nhi-inventory]
level: practitioner
status: draft
description: "Manage non-human identities (service accounts, principals, API keys, tokens) across their lifecycle: inventory, ownership, federation over keys, rotation, monitoring and removal."
sources: ["https://owasp.org/www-project-non-human-identities-top-10/", "https://cloud.google.com/iam/docs/best-practices-service-accounts", "https://learn.microsoft.com/entra/workload-id/workload-identities-overview", "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Non-human identity lifecycle

Non-human identities usually outnumber humans many times over and are rarely reviewed.

## Lifecycle
1. **Create** only via IaC/vending with mandatory owner, purpose, and expiry/review tags.
2. **Authenticate without static secrets**: workload identity federation (OIDC from CI/CD,
   Kubernetes service account tokens, managed identities / instance roles). Keys only when
   unavoidable, stored in a secrets manager.
3. **Least privilege**: one identity per workload/purpose; no shared "automation" super-account.
4. **Rotate** remaining secrets automatically; set maximum key age (Org Policy
   `iam.serviceAccountKeyExpiryHours`, disable key creation with `iam.disableServiceAccountKeyCreation`).
5. **Monitor**: unused identities and keys (last authentication), anomalous use (new IPs/regions),
   secret scanning in repos.
6. **Remove**: deprovision when the workload is retired; disable before deleting to catch hidden usage.

## Inventory sources
Entra service principals and app registrations (credentials expiry), AWS IAM roles/users with
access keys, GCP service accounts and keys, Kubernetes service accounts, SaaS API tokens, CI secrets.

## Gotchas
- OAuth app consent grants with broad scopes (e.g. Mail.Read) owned by departed staff.
- Expired client secrets causing outages; alert 30 days before expiry.
- IAM users with access keys created "temporarily" years ago.

## Verify
- [ ] Inventory with an owner for every non-human identity.
- [ ] Count of long-lived keys trending down; none older than policy maximum.
