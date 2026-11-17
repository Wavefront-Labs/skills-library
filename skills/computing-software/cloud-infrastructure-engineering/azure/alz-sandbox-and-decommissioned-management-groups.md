---
id: computing-software.cloud-infrastructure-engineering.azure.alz-sandbox-and-decommissioned-management-groups
name: alz-sandbox-and-decommissioned-management-groups
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, landing-zone, sandbox-management-group, decommissioned-mg, sandbox-subscriptions, budgets]
level: practitioner
status: docs-checked
description: "Run ALZ sandbox and decommissioned management groups: isolate sandboxes with policy, budgets and expiry, then park retired subscriptions."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/considerations/sandbox-environments", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sandbox and decommissioned management groups

**Goal:** give engineers a place to experiment that cannot reach corporate networks or run up unbounded bills, and a holding group for subscriptions on their way out.

## Sandbox management group
- Place each sandbox subscription in the `sandbox` management group. Sandbox policies sit at that group and sandboxes also inherit from the hierarchy above. The group has a less restrictive policy set than corp and online, and is securely isolated from them.
- **Networking:** keep sandbox networks unpeered with anything outside the sandbox, using the "deny virtual network peering cross subscription" policy. Use the "deny ExpressRoute/VPN/Virtual WAN creation" policy to block those gateways and hubs.
- **Audit logging:** enable a diagnostic setting covering at least the administrative and security log categories for every sandbox subscription, sent to a central Log Analytics workspace or a SIEM such as Sentinel. The sandbox group should inherit the ALZ "Configure Azure activity logs to stream to specified Log Analytics workspace" policy.
- **Access:** the sandbox user has Owner on the sandbox subscription. When a sandbox is cancelled, remove Owner RBAC for its users.
- **Cost:** create a Cost Management budget per sandbox, or apply a default one with the `Deploy-Budget` policy at the sandbox group, set to the maximum cost the organisation approves. A budget alert is only a warning; decide whether to cancel or delete the subscription when it crosses 100%.
- **Expiry:** give each sandbox an expiration date (a tag on the subscription) and use automation to cancel or delete it on that date. After expiry, move it to the decommissioned group.
- **Service restriction:** if required, use the Azure service blocklist policy to deny specific services. Unrestricted sandboxes are the ideal.
- **Information protection:** tell users not to put sensitive data in sandboxes; Microsoft Purview can alert if labelled sensitive data appears.

## Decommissioned management group
The dedicated group for cancelled landing zones. Move them here; Azure then deletes them after 30 to 60 days.

## Verify
- [ ] A test peering from a sandbox to a hub network is denied.

## Checked
Method: docs-checked 2026-11-09 against the sandbox-environments and resource-org-management-groups Learn pages (downloaded with curl as Learn markdown; sandbox page read in full, management-group page searched for sandbox and decommissioned). Dropped the percentage alert tiers, auto-deallocate, decommissioned policy contents, retention figures, CLI command and the github library source.
