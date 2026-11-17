---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.just-in-time-access
name: just-in-time-access
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, identity-architecture, just-in-time-access, privileged-access-management, pam, entra-pim, temporary-elevated-access, privileged-access-manager, zero-standing-privileges, approval-workflow]
level: practitioner
status: draft
description: "Remove standing admin access with just-in-time elevation: eligible vs active roles, approval and justification, time limits, session logging and native tools per cloud."
sources: ["https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-configure", "https://docs.aws.amazon.com/singlesignon/latest/userguide/temporary-elevated-access.html", "https://cloud.google.com/iam/docs/pam-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Just-in-time privileged access

Goal: **zero standing privileges** for production admin; people are *eligible* and activate for
a short, logged window.

## Tools
- Azure/Entra: **Privileged Identity Management** — eligible role assignments for Entra roles and
  Azure RBAC; activation with MFA, justification, ticket number, approval, max duration (e.g. 1-4 h).
- AWS: IAM Identity Center **temporary elevated access** with partner solutions or the AWS TEAM
  open-source solution (request/approve permission set assignments for a time window).
- GCP: **Privileged Access Manager** — entitlements with approvers and max duration granting IAM roles temporarily.
- Third-party PAM (CyberArk, Teleport, StrongDM) for multi-cloud and infrastructure sessions.

## Design
1. Classify roles: standing (read-only, dev environments) vs JIT (prod write/admin, break-glass excluded).
2. Activation policy: MFA, justification, ticket link; approval for highest-impact roles
   (second person); auto-approve with notification for routine operator roles.
3. Duration: shortest workable; no "8-hour" admin by default.
4. Log and alert on activations; review activations weekly.
5. Emergency path when approvers are unavailable (break-glass) with heavier alerting.

## Verify
- [ ] Count of standing prod admin assignments ≈ 0 (excluding break-glass).
- [ ] Activations visible in audit logs with justification.
