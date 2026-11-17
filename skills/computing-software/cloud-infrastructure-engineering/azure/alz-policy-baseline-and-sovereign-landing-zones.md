---
id: computing-software.cloud-infrastructure-engineering.azure.alz-policy-baseline-and-sovereign-landing-zones
name: alz-policy-baseline-and-sovereign-landing-zones
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, landing-zone, alz-policies, policy-baseline, sovereign-landing-zone, slz, azure-policy, alz-library]
level: advanced
status: draft
description: "Adopt and maintain the ALZ policy baseline (assignments per MG, library updates, parameter tuning) and extend it with the Sovereign Landing Zone policy portfolio."
sources: ["https://github.com/Azure/Enterprise-Scale/wiki/ALZ-Policies", "https://azure.github.io/Azure-Landing-Zones/library/", "https://learn.microsoft.com/industry/sovereignty/slz-overview", "https://learn.microsoft.com/industry/sovereignty/policy-portfolio-baseline"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ALZ policy baseline and sovereign landing zones

**Goal:** know what the ALZ policy baseline assigns where, tune it without forking, upgrade it
safely, and layer sovereignty controls when regulation demands.

## What ALZ assigns (by MG)
| MG | Notable assignments |
|---|---|
| Intermediate root | Microsoft Cloud Security Benchmark (audit), Defender for Cloud plans (DINE), Activity Log to LAW, resource diagnostics to LAW, allowed locations (optional), deny classic resources |
| Platform/Connectivity | Enable DDoS on VNets |
| Platform/Identity | Deny public IP, deny management ports from internet, subnet must have NSG, backup for VMs |
| Landing Zones | Deny IP forwarding, subnet NSG, deny storage HTTP, enforce TLS, AKS policies, SQL auditing, Key Vault guardrails |
| Landing Zones/Corp | Deny public endpoints, private DNS DINE, deny hybrid networking |
| Decommissioned | Deny everything except delete, deallocate VMs |
| Sandbox | Deny VNet peering/gateways |
The definitions come from the **ALZ library** (`alz` policy library repo), versioned; Terraform `avm-ptn-alz` and ALZ Bicep consume a pinned library version.

## Tune without forking
- Parameters per assignment (`policy_assignments_to_modify` in Terraform pattern / `.bicepparam`): workspace ID, email contacts, effect overrides (`Audit` instead of `Deny`).
- `enforcement_mode = DoNotEnforce` per assignment for staged adoption.
- Exemptions for individual resources; never edit the library definition in place.
- Add custom initiatives as *additional* archetypes (`custom_archetype` override files) rather than editing built-in archetypes.

## Upgrading the library
1. Read the ALZ "What's new" — note new assignments, changed effects (Audit→Deny), renamed definitions.
2. Bump the library ref in IaC, run plan in a **canary** tenant/MG first.
3. Watch for DINE assignments whose role requirements changed (identity needs new roles).
4. Roll to production; review compliance deltas for a week.

## Sovereign Landing Zone (SLZ)
For EU/public-sector data sovereignty:
- Extra MGs **Confidential Corp** / **Confidential Online** requiring confidential computing SKUs.
- Sovereignty Baseline policy initiatives: *Global* (allowed locations, deny resources lacking CMK support) and *Confidential* (allowed confidential VM/AKS SKUs, CMK in Managed HSM).
- Deploy via the SLZ Bicep repo or the Terraform ALZ module with the `sovereign_*` archetypes; country-specific portfolios (e.g. BIO for NL) layer on top.

## Gotchas
- Allowed locations at root blocks global resources unless `global` is in the list.
- Some ALZ DINE policies deploy into the management subscription; their identities need roles there, not just at the assignment scope.
- Effects changed to Deny in a library upgrade will fail pipelines of app teams the day you merge — announce.

## Verify
- [ ] `az policy assignment list --scope <mg-id> -o table` matches the library version's expected set.
- [ ] Library version is pinned in IaC and recorded in the platform changelog.
- [ ] For SLZ: a non-confidential VM SKU deployment in Confidential Corp is denied.
