---
id: computing-software.cloud-infrastructure-engineering.azure.subscription-vending-automation
name: subscription-vending-automation
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, subscription-vending, lz-vending, subscription-creation, subscription-alias, ea-enrollment-account, mca-invoice-section, bicep-lz-vending, terraform-lz-vending, avm, landing-zone, platform-engineering, self-service, subscription-request, budget-on-creation]
level: advanced
status: draft
description: "Automate subscription creation (EA/MCA/MPA alias API) and placement with the lz-vending Bicep/Terraform modules: MG, tags, RBAC, VNet + peering, budget, from a reviewed request file in Git."
sources: ["Microsoft Learn - Subscription vending (Cloud Adoption Framework)", "Microsoft Learn - Programmatically create Azure subscriptions (EA, MCA, MPA)", "GitHub Azure/bicep-lz-vending", "GitHub Azure/terraform-azurerm-lz-vending", "Microsoft Learn - Subscription alias REST API"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subscription vending — a PR creates a landing zone, not a ticket to the platform team

**Goal:** an application team submits one YAML/JSON file; a pipeline creates the subscription
under the right billing scope, drops it in the right management group, tags it, wires RBAC,
a spoke VNet peered to the hub, and a budget — in under 15 minutes, repeatably.

## 1. Billing prerequisites (the part that blocks everyone)
| Agreement | Scope needed for the pipeline identity | Role |
|---|---|---|
| EA | `/providers/Microsoft.Billing/billingAccounts/<id>/enrollmentAccounts/<id>` | Enrollment account **Owner** (SPN added via EA portal / `az billing enrollment-account`) |
| MCA | `.../billingProfiles/<id>/invoiceSections/<id>` | Azure subscription creator on the invoice section |
| MPA (CSP) | `.../customers/<id>` | Admin agent / via partner |
```bash
az billing account list --query "[].{name:name,type:agreementType}" -o table
az billing enrollment-account list -o table      # EA
az billing invoice section list --account-name <BA> --profile-name <BP> -o table   # MCA
```
The pipeline service principal also needs Owner (or a custom role with
`Microsoft.Subscription/aliases/write`, `Microsoft.Management/managementGroups/subscriptions/write`)
at the target management groups.

## 2. The request file
```yaml
# landing-zones/app-payments-prod.yaml
subscriptionDisplayName: sub-payments-prod
subscriptionAliasName: sub-payments-prod
billingScope: /providers/Microsoft.Billing/billingAccounts/<BA>/enrollmentAccounts/<EA>
workload: Production            # or DevTest
managementGroupId: mg-landingzones-corp
tags: {costCentre: "CC1234", owner: "payments-team@<DOMAIN>", env: prod, dataClass: confidential}
roleAssignments:
  - {principalId: <GROUP-ID>, role: Contributor}
  - {principalId: <GROUP-ID>, role: "Reader"}
virtualNetwork:
  enabled: true
  addressSpace: ["10.42.0.0/22"]
  location: westeurope
  hubNetworkResourceId: /subscriptions/<HUB-SUB>/resourceGroups/rg-hub/providers/Microsoft.Network/virtualNetworks/vnet-hub
  useRemoteGateways: true
  dnsServers: ["10.0.0.4"]
budget: {amount: 5000, contactEmails: ["payments-team@<DOMAIN>"]}
```
PR review = approval; CODEOWNERS = platform team. IP ranges are allocated from an IPAM file or
Azure IPAM; the PR check validates no overlap.

## 3. Deploy with the lz-vending module
Bicep (`br/public:avm/ptn/lz/sub-vending:<version>`):
```bicep
targetScope = 'managementGroup'
module lz 'br/public:avm/ptn/lz/sub-vending:0.2.0' = {
  name: 'lz-${req.subscriptionAliasName}'
  params: {
    subscriptionAliasEnabled: true
    subscriptionDisplayName: req.subscriptionDisplayName
    subscriptionAliasName: req.subscriptionAliasName
    subscriptionBillingScope: req.billingScope
    subscriptionWorkload: req.workload
    subscriptionTags: req.tags
    subscriptionManagementGroupAssociationEnabled: true
    subscriptionManagementGroupId: req.managementGroupId
    virtualNetworkEnabled: req.virtualNetwork.enabled
    virtualNetworkAddressSpace: req.virtualNetwork.addressSpace
    virtualNetworkLocation: req.virtualNetwork.location
    virtualNetworkPeeringEnabled: true
    hubNetworkResourceId: req.virtualNetwork.hubNetworkResourceId
    virtualNetworkUseRemoteGateways: req.virtualNetwork.useRemoteGateways
    roleAssignmentEnabled: true
    roleAssignments: [for ra in req.roleAssignments: {principalId: ra.principalId, definition: ra.role, relativeScope: ''}]
    resourceProviders: {'Microsoft.Compute': [], 'Microsoft.Storage': [], 'Microsoft.KeyVault': []}
  }
}
```
```bash
az deployment mg create -m vend.bicep --management-group-id mg-landingzones-corp -l westeurope -p req=@landing-zones/app-payments-prod.yaml   # via a converter step for YAML→JSON
```
Terraform: module `Azure/lz-vending/azurerm` with `subscription_alias_enabled`,
`subscription_management_group_association_enabled`, `virtual_networks`, `role_assignments`,
`budget_enabled` — same shape. Both are idempotent: re-running with the same alias returns the
existing subscription (alias name is the key — never change it).

## 4. After creation (the pipeline's second stage)
- Register resource providers (module does it) and features; create `rg-<app>-<env>` baseline.
- Deploy diagnostic settings/Defender/Policy? **No** — those come from MG inheritance; if the
  pipeline has to add them, your MG policies are wrong.
- Post to the team: subscription id, VNet CIDR, how to request RBAC changes (PR to the same file).
- Add the file path + subscription id to the inventory (ARG: `resourcecontainers | where type == "microsoft.resources/subscriptions"` with `tags`).

## Gotchas
- Subscription creation is async; the alias API returns 201 while the subscription provisions
  (1–10 min). Module waits, but a pipeline timeout under 15 min will flake.
- EA enrollment account SPN permissions take up to an hour; a 403 on `aliases/write` right after setup is not your code.
- Tags on the subscription are not inherited by resources; pair with the *inherit tag from subscription* Modify policy.
- Quota is per subscription: new subscriptions start with default vCPU quotas (often 10–20) — add a quota request step for prod.
- Deleting from the request repo does **not** cancel a subscription; decommission is a manual, logged step (move to `mg-decommissioned`, cancel after 30 days).

## Verify
- [ ] `az account alias show -n <alias>` returns `provisioningState: Succeeded` and a subscription id.
- [ ] `az account management-group subscription show` places it in the intended MG; tags and role assignments match the file.
- [ ] Spoke VNet peered (`peeringState: Connected`) in both directions, effective routes from a test VM include hub ranges.
- [ ] Re-running the pipeline makes no changes (idempotent).
