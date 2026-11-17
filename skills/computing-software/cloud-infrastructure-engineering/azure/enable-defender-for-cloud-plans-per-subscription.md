---
id: computing-software.cloud-infrastructure-engineering.azure.enable-defender-for-cloud-plans-per-subscription
name: enable-defender-for-cloud-plans-per-subscription
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, defender-for-cloud, defender-plans, enable-defender, defender-pricing, az-security-pricing, alz-policies]
level: practitioner
status: draft
description: "Enable Microsoft Defender for Cloud plans per subscription (CLI, Policy at MG scope), choose sub-plans and extensions, estimate cost, and audit coverage across the estate."
sources: ["https://learn.microsoft.com/azure/defender-for-cloud/connect-azure-subscription", "https://learn.microsoft.com/azure/defender-for-cloud/enable-all-plans", "https://learn.microsoft.com/cli/azure/security/pricing", "https://learn.microsoft.com/azure/defender-for-cloud/cost-estimation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enable Defender plans per subscription

**Goal:** every subscription has the intended Defender plans on from day one, with the cost
known in advance and drift detected.

## Plans (pricing names)
`VirtualMachines` (Servers P1/P2), `CloudPosture` (Defender CSPM), `Containers`, `StorageAccounts`,
`SqlServers`, `SqlServerVirtualMachines`, `OpenSourceRelationalDatabases`, `CosmosDbs`, `AppServices`,
`KeyVaults`, `Arm`, `Api`, `AI`. Foundational CSPM (free) is always on.

## Enable with CLI
```bash
az account set -s <sub>
az security pricing create -n VirtualMachines --tier Standard --subplan P2
az security pricing create -n CloudPosture --tier Standard
az security pricing create -n StorageAccounts --tier Standard --subplan DefenderForStorageV2 \
  --extensions name=OnUploadMalwareScanning isEnabled=True additionalExtensionProperties='{"CapGBPerMonthPerStorageAccount":"5000"}' \
               name=SensitiveDataDiscovery isEnabled=True
az security pricing create -n KeyVaults --tier Standard --subplan PerKeyVault
az security pricing list --query "value[].{plan:name,tier:pricingTier,sub:subPlan}" -o table
```

## Enable at scale (recommended)
Assign built-in policies at the landing-zone MG with DINE: *Configure Microsoft Defender for
Servers to be enabled* (with P2 parameter), *...for Containers*, *...for Storage*, etc., or the ALZ
**Deploy-MDFC-Config** initiative (also sets security contacts and continuous export).
Remediation task covers existing subscriptions; new subscriptions are covered automatically.
Exclude sandbox subscriptions via `notScopes` if cost-sensitive.

## Plan-level exceptions
- Servers plan can be set **per resource** (enable/disable on specific VMs) via API `Microsoft.Security/pricings` at resource scope — use for test VMs.
- Storage: exclude accounts via tag/resource-level setting.

## Cost estimate
Defender for Cloud → Environment settings → **Cost calculator** per subscription/connector
(counts servers, storage transactions, DBs). Biggest drivers: Servers P2 per node, Storage per
account + malware scanning per GB, Containers per vCore.

## Coverage audit
```kusto
securityresources
| where type == "microsoft.security/pricings"
| project subscriptionId, plan = name, tier = tostring(properties.pricingTier), subPlan = tostring(properties.subPlan)
| evaluate pivot(plan, take_any(tier))
```

## Gotchas
- Servers P2 includes MDE licensing and 500 MB/day free Log Analytics ingestion per node for security data tables — confirm workspace linkage.
- Disabling a plan stops protection immediately; re-enabling doesn't restore missed scans.
- Plans enabled at subscription apply to new resources automatically; Arc servers count under Servers plan.

## Verify
- [ ] ARG pivot shows all production subscriptions with the standard plan set.
- [ ] Policy compliance for Defender initiatives at 100% (exemptions documented).
