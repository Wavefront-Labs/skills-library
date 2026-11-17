---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.preventive-guardrails
name: preventive-guardrails
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, preventive-guardrails, detective-guardrails, service-control-policies, azure-policy, organization-policy]
level: practitioner
status: docs-checked
description: "Implement preventive and detective guardrails: SCPs and RCPs, Azure Policy effects, GCP organisation policy constraints and dry-run, Control Tower controls, testing and rollout."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html", "https://learn.microsoft.com/en-us/azure/governance/policy/overview", "https://docs.cloud.google.com/organization-policy/overview", "https://docs.aws.amazon.com/controltower/latest/controlreference/controls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preventive and detective guardrails

## Types
- **Preventive** (block the action): AWS service control policies (SCPs; resource control policies, RCPs, set the
  permission limit on resources and combine with SCPs), Azure Policy `deny` (and `DenyAction`) effects, GCP
  organisation policy constraints such as `constraints/gcp.resourceLocations` and `iam.disableServiceAccountCreation`.
- **Detective** (find and report): Azure Policy `audit` / `auditIfNotExists`; AWS Control Tower detective controls (for
  example "Detect Whether Public Read Access to Amazon S3 Buckets is Allowed"); GCP organisation policies in dry-run mode
  audit-log violations without denying.
- **Corrective**: Azure Policy `modify` and `deployIfNotExists` (the assignment's managed identity needs permission to
  create or update the target resources). Control Tower also has proactive controls (see its Controls Reference).
- An SCP never grants permission: effective permission is the intersection of SCPs and RCPs with identity-based and
  resource-based policies. An Azure Policy `deny` blocks the create or update even when RBAC allows it.

## Typical baseline
Candidates to enforce centrally: restrict regions, deny public storage, require encryption and logging, protect the
audit trail, restrict long-lived credentials and require tags. Express each in the platform's own mechanism
(SCP, Azure Policy built-ins such as Allowed Locations or Add a tag, GCP constraints).

## Steps
1. Start detective: Azure's guidance is to begin with `audit` or `auditIfNotExists` before `deny`, `modify` or
   `deployIfNotExists`; GCP offers dry-run mode for the same purpose.
2. Test before the root: AWS strongly recommends not attaching SCPs to the organisation root untested. Move accounts
   one at a time (or in small groups) into a test OU, and use IAM service last accessed data or CloudTrail to see which
   services an account uses.
3. Manage as code with manual review (Azure recommends Policy as Code; create definitions high in the hierarchy and
   assign one level lower; use initiatives even for a single policy).
4. Use exemptions or exclusions sparingly and track them (Azure: `notScopes` and exemptions; GCP: conditional policies by
   tag, or a child-resource policy that overrides inheritance).
5. Watch for effects after rollout: Azure evaluates on create/update, on assignment changes and in a standard
   cycle once every 24 hours. GCP policies are usually not retroactive: existing violations stay and must be fixed manually.

## Gotchas
- SCPs do not affect the management account (nor service-linked roles); keep workloads out of it. Control Tower
  likewise lets the management account's root and administrators do what controls would deny.
- Do not remove the `FullAWSAccess` SCP unless you replace it with an allow list, or all member-account actions fail.
- SCP size counts every character including whitespace; remove unneeded whitespace if you approach the limit (check the
  current limit on the Organizations quotas page).
- Azure Policy is an explicit-deny system: you cannot allow what a parent assignment denies except by excluding the
  child scope from that assignment. Azure also has per-scope object limits (for example 500 policy definitions and 200
  assignments per scope).
- GCP managed constraints inherited from a parent are not merged with child policies; legacy list constraints are.

## Verify
- [ ] Guardrail set defined as code and applied to all workload branches.
- [ ] Dry-run or audit results reviewed before each switch to enforcement.

## Checked
2026-11-08. Confirmed against the AWS Organizations SCP page, the Azure Policy overview, the GCP Organization Policy
overview and the Control Tower controls page (all read in full): policy semantics, effects, management-account
exceptions, dry-run, testing guidance, limits quoted. Removed as not on those pages: the SCP 5,120-character and 5-per-target
figures, `iam.disableServiceAccountKeyCreation`, `storage.publicAccessPrevention`, AWS Config rules, Security Hub,
Security Command Center, CloudFormation hooks, the CloudTrail AccessDenied monitoring tip and the "provider-managed
roles" claim.
Method: documentation only; no commands were run.
