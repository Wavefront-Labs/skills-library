---
id: computing-software.cybersecurity-defensive.security-architecture.data-residency
name: data-residency
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [data-residency, data-sovereignty, gdpr-transfers, cloud-region-controls, organization-policy, schrems-ii, eu-data-boundary]
level: practitioner
status: draft
description: "Enforce data residency and sovereignty: map data to jurisdictions, restrict cloud regions with policy, control replicas, backups, logs and support access, and document transfers."
sources: ["https://cloud.google.com/resource-manager/docs/organization-policy/defining-locations", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples_general.html", "https://learn.microsoft.com/en-us/azure/governance/policy/samples/built-in-policies", "https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection_en"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data residency and sovereignty

**Residency** = where data is stored/processed. **Sovereignty** = whose laws can compel access
(a US provider in an EU region is still subject to US law).

## Steps
1. Map each data class to its residency requirement (contract, GDPR transfer rules, sector law).
2. Enforce allowed regions in cloud policy:
   - AWS SCP deny with `aws:RequestedRegion` not in the allowed list (exclude global services such as IAM, CloudFront, Route 53, Support via `NotAction`).
   - GCP org policy `constraints/gcp.resourceLocations` with value groups like `in:eu-locations`.
   - Azure Policy "Allowed locations" and "Allowed locations for resource groups" assigned at management group.
3. Check the hidden copies: cross-region replication, backups and DR region, log/analytics workspaces, CDN caches, support case uploads, ML/AI service processing location, SaaS sub-processors.
4. Restrict provider personnel access where offered (Customer Lockbox, Access Approval, Access Transparency, AWS Nitro no-operator-access claims) and hold keys yourself (HYOK/EKM) for sovereignty concerns.
5. Document transfers (SCCs, transfer impact assessment) for anything that must leave.

## Gotchas
- Global services (IAM, DNS, some telemetry) cannot be region-pinned; document them.
- Region-pinning SCPs break bootstrap if they deny global endpoints; test in a sandbox OU.
- Encryption with provider-managed keys does not change sovereignty exposure.

## Verify
- [ ] Attempt to create a bucket/VM in a disallowed region is denied by policy.
- [ ] Inventory query (AWS Config aggregator / Azure Resource Graph / Cloud Asset Inventory) shows no resources outside allowed regions.
- [ ] Backup and log destinations confirmed in-region.
