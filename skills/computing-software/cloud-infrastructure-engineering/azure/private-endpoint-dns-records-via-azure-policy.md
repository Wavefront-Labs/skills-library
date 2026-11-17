---
id: computing-software.cloud-infrastructure-engineering.azure.private-endpoint-dns-records-via-azure-policy
name: private-endpoint-dns-records-via-azure-policy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, private-link, private-endpoint-policy, dine-private-dns, private-dns-zone-group, azure-policy, deployifnotexists]
level: advanced
status: docs-checked
description: "Auto-create private endpoint DNS records in central zones with DeployIfNotExists policies (private DNS zone groups), deny spoke-local privatelink zones, and remediate."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/private-link-and-dns-integration-at-scale", "https://learn.microsoft.com/azure/private-link/private-endpoint-dns-integration", "https://learn.microsoft.com/cli/azure/policy/remediation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy to auto-create private endpoint DNS records

**Goal:** app teams create private endpoints in their spokes; DNS A records appear in the central
privatelink zones automatically, and nobody creates rogue zones.

## Two policies
1. **Deny** creation of private DNS zones with names like `privatelink.*` outside the connectivity subscription (the Cloud Adoption Framework example is `Deny-PrivateDNSZone-PrivateLink`).
2. **DeployIfNotExists** per service: when a PE for group ID `X` exists without a DNS zone group, deploy `privateDnsZoneGroups` pointing to the central zone. Built-in definitions named like "... to use private DNS zones" exist per service, and ALZ has an initiative *Configure Azure PaaS services to use private DNS zones* that bundles them; prefer built-ins over custom policies where one exists.

## DINE rule shape (simplified)
```json
"if": { "allOf": [
  { "field": "type", "equals": "Microsoft.Network/privateEndpoints" },
  { "count": { "field": "Microsoft.Network/privateEndpoints/privateLinkServiceConnections[*].groupIds[*]",
               "where": { "field": "Microsoft.Network/privateEndpoints/privateLinkServiceConnections[*].groupIds[*]", "equals": "blob" } },
    "greaterOrEquals": 1 } ] },
"then": { "effect": "deployIfNotExists", "details": {
  "type": "Microsoft.Network/privateEndpoints/privateDnsZoneGroups",
  "roleDefinitionIds": [ "/providers/Microsoft.Authorization/roleDefinitions/4d97b98b-1d4f-4787-a291-c67834d212e7" ],
  "deployment": { "properties": { "mode": "incremental", "template": { "...": "creates zone group with privateDnsZoneId parameter" } } } } }
```

## Assignment
- Assign at the landing zones MG with parameter `privateDnsZoneId` = central zone resource ID (one assignment per service, or the ALZ initiative with a parameter per zone).
- The policy's managed identity needs the role(s) listed in `roleDefinitionIds` at the assignment scope **and** **Private DNS Zone Contributor** in the subscription and resource group that host the private DNS zones.
```bash
az role assignment create --assignee-object-id <policy-mi> --assignee-principal-type ServicePrincipal \
  --role "Private DNS Zone Contributor" --scope /subscriptions/<conn-sub>/resourceGroups/rg-privatedns
```

## Remediate existing PEs
```bash
az policy remediation create -n rem-kv-dns --policy-assignment <assignment-id> \
  --management-group mg-landingzones --resource-discovery-mode ReEvaluateCompliance
```

## Gotchas
- DeployIfNotExists runs after the private endpoint is created, not with it, so the record can lag; if apps resolve names immediately at deploy time, create the zone group in the same IaC deployment as the endpoint.
- A service whose endpoints need several group IDs or zones needs policies covering every one; if a groupId clashes with another service, match on both `privateLinkServiceId` and groupId (the second CAF policy variant).
- If teams created zone groups pointing to their own zones before the Deny, records live in the wrong zones — inventory zone groups and fix.

## Verify
- [ ] A new blob PE in a spoke gets an A record in the central zone shortly after creation (`az network private-dns record-set a list -g rg-privatedns -z privatelink.blob.core.windows.net`).
- [ ] Attempt to create `privatelink.blob.core.windows.net` in a spoke is denied.

## Checked

2026-10-31. Confirmed against the Learn Cloud Adoption Framework page on Private Link and DNS integration at scale (deny policy for privatelink zones, DeployIfNotExists policy on groupId and the groupId plus privateLinkServiceId variant, privateDnsZoneGroups type, roleDefinitionIds, Private DNS Zone Contributor for the policy identity, built-in policy naming and the ALZ initiative), the private endpoint DNS integration page (zone groups) and the az policy remediation reference (--resource-discovery-mode values). Removed: the Deny-Private-DNS-Zones and Deploy-Private-DNS-Zones names, the ~50 services count, the Network Contributor role name, the 10-15 minute figure and the Cosmos, ADF and AMPLS examples (not in the fetched docs). Commands were checked with check_commands.py.

Method: documentation only; no commands were run.
