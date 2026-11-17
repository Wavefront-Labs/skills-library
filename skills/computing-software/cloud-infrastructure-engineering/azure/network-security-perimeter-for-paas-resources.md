---
id: computing-software.cloud-infrastructure-engineering.azure.network-security-perimeter-for-paas-resources
name: network-security-perimeter-for-paas-resources
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, network-security-perimeter, nsp, paas-isolation, storage-security, data-exfiltration, access-rules]
level: advanced
status: docs-checked
description: "Put supported PaaS resources (Storage, Key Vault, Event Hubs, Azure Monitor) in a network security perimeter: profiles, access rules, transition vs enforced mode, logs."
sources: ["https://learn.microsoft.com/azure/private-link/network-security-perimeter-concepts", "https://learn.microsoft.com/azure/private-link/create-network-security-perimeter-cli", "https://learn.microsoft.com/azure/private-link/network-security-perimeter-diagnostic-logs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network security perimeter

**Goal:** a logical boundary around PaaS resources that sit outside your virtual networks: members talk to each other, public access is governed by explicit rules, and public traffic is denied by default in enforced mode (exfiltration control).

## Concepts
- **Perimeter**: top-level resource (name, location, resource group). **Profile**: a collection of access rules applied to the resources associated with it. **Access rule**: inbound and outbound rules for access outside the perimeter. **Resource association**: perimeter membership of a PaaS resource. **Network identifier**: public IP or prefix tied to a service endpoint subnet, used with standard service endpoint. **Diagnostic settings** collect the logs.
- Rule types: inbound subscription-based, inbound IP-based, inbound service tags (preview); outbound FQDN-based.
- **Transition mode** (formerly Learning mode) is the default: helps you understand existing access patterns and is the advised step before enforcing. **Enforced mode** must be set by an administrator; all traffic except intra-perimeter traffic is denied unless an Allow rule exists.
- Private endpoint traffic is allowed without explicit access rules.
- Intra-perimeter traffic and subscription-based inbound rules do not support SAS token authentication; such requests are rejected.
- A managed identity is required to support intra-perimeter communication between resources (the quickstart notes some resources, e.g. Azure SQL backend traffic, may work without one).

## Create (CLI, from the quickstart)
Needs Azure CLI 2.38.0 or later and the extension: `az extension add --name nsp`.
```bash
az network perimeter create --name network-security-perimeter --resource-group resource-group -l westcentralus
az network perimeter profile create --name network-perimeter-profile --resource-group resource-group --perimeter-name network-security-perimeter
az network perimeter association create --name network-perimeter-association --perimeter-name network-security-perimeter \
  --resource-group resource-group --access-mode Learning \
  --private-link-resource "{id:<PaaSArmId>}" --profile "{id:<networkSecurityPerimeterProfileId>}"
az network perimeter profile access-rule create --name access-rule --profile-name network-perimeter-profile \
  --perimeter-name network-security-perimeter --resource-group resource-group --address-prefixes "[192.0.2.0/24]"
```
Switch to enforcement by re-running `association create` with `--access-mode Enforced`. The quickstart still uses the name `Learning` for the transition mode value. Its access-rule example is an inbound IP prefix rule.

## Rollout
1. Associate resources in transition mode and enable diagnostic settings.
2. Review the logs. Categories ending `...ResourceRulesAllowed/Denied` apply in transition mode only and show what the resource's own rules decided when perimeter rules denied; `...PerimeterRulesDenied` categories apply in enforced mode.
3. Add inbound and outbound rules, then move associations to enforced mode.

## Limits and gotchas
- Supported resource types are a list on the concepts page (for example Storage and Key Vault GA; Cosmos DB, SQL DB, App Configuration, Azure OpenAI and Event Grid in preview, no production use advised). Check the list before designing.
- Sentinel-enabled Log Analytics workspaces are not supported (analytic rules are automatically disabled). Azure Backup is not supported for storage accounts with a perimeter.
- Service endpoint traffic is not supported: traffic can be denied even when an inbound rule allows 0.0.0.0/0. The page recommends private endpoints for IaaS-to-PaaS.
- Resource names cannot be longer than 44 characters for portal-created associations.
- Recommended limits: 100 perimeters per subscription, 200 profiles per perimeter, 1000 PaaS resources per perimeter; hard limit 200 rule elements per profile for inbound and outbound each.
- Removing an association makes access control fall back to the resource firewall; with `PublicNetworkAccess` set to `SecuredByPerimeter` the resource becomes locked down.
- Log destination: Log Analytics workspace (table `NSPAccessLogs`), Storage or Event Hubs, which must be in the same perimeter as the PaaS resource for logs to flow. Logs may be aggregated; treat missing `count` and `timeGeneratedEndTime` as a count of 1.

## Verify
- [ ] After enforcing, an access attempt from a source with no matching rule is denied and appears in the denied log categories (`NspPublicInboundPerimeterRulesDenied`).
- [ ] Callers you intend to allow match a rule (`matchedRule` in the log).

## Checked

2026-11-07. Read in full: Network security perimeter concepts, Quickstart (Azure CLI), Diagnostic logs.
- Removed (not on the pages): "resources in two perimeters aren't allowed", "enforced mode cuts off trusted services exceptions", the "subscription rules use managed identity of the caller" claim, the `--direction Inbound` flag and `-n allow-office` form (the quickstart's access-rule command has no direction flag), and the Event Hubs/SQL/Log Analytics list in the description (SQL DB is preview).
- Corrected: transition mode is the default, and enforced mode denies all except intra-perimeter traffic; added SAS and service-endpoint limits.
- Not read: the "Transitioning to a network security perimeter" article and the per-service onboarding pages. The CLI reference for `az network perimeter` was not read, so flags beyond the quickstart's are not claimed.

Method: documentation only; no commands were run.
