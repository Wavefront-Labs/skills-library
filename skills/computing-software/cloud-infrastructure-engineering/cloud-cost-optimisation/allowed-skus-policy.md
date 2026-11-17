---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.allowed-skus-policy
name: allowed-skus-policy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-governance, allowed-skus-policy, allowed-regions, instance-type-restrictions, cost-guardrail-policy, azure-policy-allowed-skus]
level: practitioner
status: docs-checked
description: "Restrict costly regions, instance families and SKUs by policy (SCPs, Azure Policy allowed SKUs, Org Policy) with an exception path, per environment and account type."
sources: ["https://learn.microsoft.com/azure/governance/policy/samples/built-in-policies", "https://cloud.google.com/resource-manager/docs/organization-policy/defining-locations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Allowed SKU and region policies

## What to restrict
- **Regions** not used by the business (also a security control).
- **Expensive families** (GPU, high-memory, bare metal) outside approved accounts.
- **Premium tiers** in non-production (premium storage, business-critical DB tiers, dedicated hosts).
- **Commitment purchases** by anyone except FinOps (deny the purchase actions for reservations
  and savings plans; restrict Azure reservation purchase roles).
- **Marketplace subscriptions** without procurement approval.

## Implementations
- **AWS service control policies (SCPs)**: deny instance launches by instance type and deny
  actions outside allowed regions, excluding global services; take the condition keys and
  action names from the AWS Organizations and EC2 documentation (the SCP examples page
  returned no text when checked, so no policy is reproduced here).
- **Azure Policy** built-ins: "Allowed virtual machine size SKUs", "Allowed locations", "Allowed
  storage account SKUs"; assign at management group with parameters per environment.
- **Google Org Policy**: the resource locations constraint (`gcp.resourceLocations`) restricts
  where resources are created.

## Steps
1. Analyse current usage so policies don't break running workloads.
2. Audit mode first; publish allowed lists per environment.
3. Exception process with expiry (tag-based or separate OU).
4. Review lists twice a year as new generations appear (allow newer cheaper families).

## Gotchas
- Allow-lists that exclude newer, cheaper instance generations.
- Region deny that blocks global services (IAM, CloudFront, Route 53) - exclude them.

## Verify
- [ ] Attempt to launch a disallowed SKU in dev is denied with a clear message.

## Checked
2026-11-01. Confirmed in the Azure built-in policy list ("Allowed virtual machine size SKUs", "Allowed locations",
"Allowed storage account SKUs") and the Google Cloud resource locations page (`gcp.resourceLocations`). Removed: the
SCP example with its action names, condition keys and instance-type patterns (the AWS SCP examples page returned no
text), custom machine-type constraints and the default-zero GPU quota claim.
Method: documentation only; no commands were run.
