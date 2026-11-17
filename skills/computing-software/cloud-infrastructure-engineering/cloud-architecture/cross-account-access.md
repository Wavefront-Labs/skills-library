---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cross-account-access
name: cross-account-access
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, identity-architecture, cross-account-access, assume-role, external-id, cross-tenant-access, azure-lighthouse, confused-deputy]
level: practitioner
status: draft
description: "Design cross-account and cross-tenant access safely: role assumption with trust policies, external ID for third parties, Azure Lighthouse, and avoiding confused-deputy issues."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_aws-accounts.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html", "https://learn.microsoft.com/azure/lighthouse/overview", "https://cloud.google.com/iam/docs/service-account-impersonation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cross-account and cross-tenant access

## AWS
- Role in target account with a **trust policy** naming the source principal (specific role ARN,
  not the whole account root unless the source governs it).
- Third parties: require `sts:ExternalId` condition (unique per customer) to prevent the
  confused-deputy problem.
- Restrict with `aws:PrincipalOrgID` / `aws:SourceOrgID` conditions for intra-org access, and
  `aws:SourceAccount` / `aws:SourceArn` for service principals.
- Resource-based policies (S3, KMS, SQS) for direct cross-account access; check KMS key policy too.

## Azure
- Same tenant: RBAC across subscriptions.
- Partner/MSP across tenants: **Azure Lighthouse** delegations (eligible authorisations with PIM).
- B2B guest users or multi-tenant apps for users; cross-tenant access settings to control inbound/outbound.

## Google Cloud
- Grant service account or principal roles on the target project; prefer **service account
  impersonation** (`roles/iam.serviceAccountTokenCreator`) over key sharing.
- Org policy `iam.allowedPolicyMemberDomains` limits which domains can be granted.

## Steps
1. Inventory all cross-boundary access (IAM Access Analyzer external access findings).
2. Standardise on role assumption / impersonation; ban long-lived keys.
3. Log assume-role events; alert on unexpected source accounts.

## Gotchas
- Trust policy `Principal: {"AWS": "arn:aws:iam::123456789012:root"}` delegates to everyone the
  other account allows.
- Forgetting KMS key policy, causing access denied that looks like an S3 problem.

## Verify
- [ ] Access Analyzer shows no unintended external access.
- [ ] Third-party roles all require ExternalId.
