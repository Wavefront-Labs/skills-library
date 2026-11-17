---
id: computing-software.cloud-infrastructure-engineering.azure.private-endpoint-manual-approval-and-cross-tenant-connections
name: private-endpoint-manual-approval-and-cross-tenant-connections
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, private-link, connection-approval, cross-tenant-private-endpoint, manual-request, private-endpoint-connections, data-exfiltration]
level: practitioner
status: docs-checked
description: "Handle private endpoint connection approval: auto vs manual, approving/rejecting requests on the resource, cross-tenant PEs, and preventing exfiltration via foreign PEs."
sources: ["https://learn.microsoft.com/azure/private-link/manage-private-endpoint", "https://learn.microsoft.com/azure/private-link/private-endpoint-overview#access-to-a-private-link-resource-using-approval-workflow", "https://learn.microsoft.com/azure/private-link/private-endpoint-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private endpoint manual approval and cross-tenant connections

**Goal:** know who has private endpoints into your resources, approve deliberately, and let
partners or other tenants connect without opening public access.

## Approval model
- **Automatic**: the PE creator has `Microsoft.<Provider>/<type>/privateEndpointConnectionsApproval/action` on the target (e.g. Contributor) → Approved immediately.
- **Manual**: creator lacks that permission, or uses `--manual-request true` → connection *Pending* on the target until its owner approves.

## Approve / reject on the target resource
```bash
az network private-endpoint-connection list --id <storage-account-id> -o table
az network private-endpoint-connection approve --id <connection-id> --description "Approved CHG0042"
az network private-endpoint-connection reject  --id <connection-id> --description "Unknown tenant"
az network private-endpoint-connection delete  --id <connection-id>
```

## Cross-tenant
Consumer in tenant B creates a PE to your resource ID (or a PLS alias) with `--manual-request true`
and a request message; you approve in tenant A. DNS is the consumer's job (their own
privatelink zone with the record pointing to their PE IP).
Typical uses: managed service providers, SaaS vendors reaching a customer's storage, M&A.

## Exfiltration risk and controls
A PE in a **foreign** tenant approved on your resource gives that tenant a private path to it —
review approvals like access grants.
Conversely, insiders could create PEs from your VNets to **other tenants'** resources (exfiltration):
- Use Azure Policy (custom, on `Microsoft.Network/privateEndpoints`) to restrict which private-link targets your VNets may connect to.

## Inventory
List private endpoints with Azure Resource Graph (type `microsoft.network/privateendpoints`) and review each target and connection status.

## Gotchas
- Review Pending connections and reject or delete them so the list stays meaningful.

## Verify
- [ ] Monthly review of approved connections whose PE subscription isn't yours.
- [ ] Policy denies a test PE targeting a resource in a foreign tenant.

## Checked
2026-10-28. Confirmed on the private endpoint overview and manage pages: automatic approval needs the `Microsoft.<Provider>/<type>/privateEndpointConnectionsApproval/action` permission, manual requests appear as Pending until the provider approves, alias-based connections. The approve/reject/delete/list CLI commands passed the CLI reference check.
Removed (not confirmed): portal path, the policy property path and firewall FQDN advice, the Resource Graph query body, and the pending-expiry, rejected-state and firewall gotchas.

Method: documentation only; no commands were run.
