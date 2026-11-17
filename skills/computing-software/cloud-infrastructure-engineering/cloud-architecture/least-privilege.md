---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.least-privilege
name: least-privilege
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, identity-architecture, least-privilege, iam-policy-design, permission-boundaries, access-analyzer, unused-access, abac, iam-recommender, privilege-escalation]
level: advanced
status: draft
description: "Design least-privilege cloud roles and keep them so: role taxonomy, policies generated from activity, guardrails, boundaries, ABAC, unused-access reviews."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html", "https://cloud.google.com/policy-intelligence/docs/role-recommendations-overview", "https://learn.microsoft.com/azure/role-based-access-control/best-practices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Least-privilege role design

## Steps
1. **Role taxonomy**: humans by job function × environment (read-only, operator, admin); workloads
   one role each. Prod admin is rare and time-bound (JIT).
2. **Start from managed job-function roles** for humans, then narrow; for workloads write
   specific policies (actions + resource ARNs/scopes + conditions).
3. **Generate from activity**: IAM Access Analyzer policy generation from CloudTrail, GCP IAM
   recommender (role recommendations from 90 days usage), Azure Entra permissions management /
   access reviews. Use in staging, then prod with a buffer.
4. **Guardrails above roles**: SCPs/RCPs, Azure Policy and deny assignments, GCP org policies and
   IAM deny policies — what nobody may do regardless of role.
5. **Permission boundaries** (AWS) to let teams create roles safely without exceeding a ceiling.
6. **ABAC** with tags/session tags for scaling (e.g. allow access where `aws:ResourceTag/team` = `aws:PrincipalTag/team`).
7. **Review**: Access Analyzer unused access findings (unused roles/permissions), GCP recommender,
   Entra access reviews — quarterly.

## Privilege escalation paths to block
`iam:PassRole` with wildcard resources, `iam:CreatePolicyVersion`/`AttachRolePolicy` on self,
`iam:UpdateAssumeRolePolicy`, Lambda/compute creation with powerful roles, GCP `iam.serviceAccounts.actAs`
and `getAccessToken`, Azure `Microsoft.Authorization/roleAssignments/write`.
Scan with tools like PMapper / Cloudsplaining.

## Verify
- [ ] No workload policies with `"Action": "*"` or `"Resource": "*"` on write actions without conditions.
- [ ] Unused permissions report reviewed this quarter.
