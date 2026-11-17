---
id: computing-software.cloud-infrastructure-engineering.azure.jit-vm-access-policies-requests-and-audit
name: jit-vm-access-policies-requests-and-audit
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, jit-access, jit-vm-access, jit-policy, jit-configure, jit-request, jit-audit, defender-for-servers]
level: practitioner
status: docs-checked
description: "Configure Defender for Cloud just-in-time VM access policies per VM, request access from portal or PowerShell with source IP and duration, and review requests in the activity log."
sources: ["https://learn.microsoft.com/azure/defender-for-cloud/just-in-time-access-usage", "https://learn.microsoft.com/azure/defender-for-cloud/just-in-time-access-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JIT VM access: policies, requests and audit

**Goal:** management ports (for example RDP 3389, SSH 22, WinRM 5985/5986) are closed by default and opened
only for a specific source IP, for a bounded time, with an audit trail.

## Requirements
- Microsoft Defender for Servers **Plan 2** enabled on the subscription.
- Azure Resource Manager VM with an NSG, or protected by Azure Firewall on the same VNet (JIT requires an NSG, a firewall configuration, or both). Classic-deployment VMs and VMs behind Azure Firewalls controlled by Azure Firewall Manager are not supported.
- Roles (summary of the docs table; a custom role is allowed):
  - Configure or edit a policy: `Microsoft.Security/locations/jitNetworkAccessPolicies/write` plus `Microsoft.Compute/virtualMachines/write`.
  - Request access: `Microsoft.Security/locations/jitNetworkAccessPolicies/initiate/action`, `.../jitNetworkAccessPolicies/*/read`, `Microsoft.Compute/virtualMachines/read`, `Microsoft.Network/networkInterfaces/*/read`, `Microsoft.Network/publicIPAddresses/read`. The docs point to the `Set-JitLeastPrivilegedRole` script for a least-privileged requester role.
  - View status: Reader and SecurityReader.

## Configure the policy (per VM)
Defender for Cloud -> Just-in-time VM access -> *Not configured* tab -> mark the VMs -> *Enable JIT on VMs* -> review ports. Right-click a VM on the *Configured* tab and choose *Edit* to change ports. Set a maximum request duration per port (the docs example uses `PT3H`; maximum allowed access is 3 hours).

PowerShell:
```powershell
Set-AzJitNetworkAccessPolicy -Kind "Basic" -Location "<LOCATION>" -Name "default" -ResourceGroupName "<RESOURCE_GROUP>" -VirtualMachine $JitPolicyArr
```
JIT adds deny-all-inbound rules for the selected ports in the NSG and Azure Firewall. Existing rules on those ports take priority over the new deny rules, so remove broader allow rules or JIT does nothing; with no existing rules the new rules take top priority. Established connections are not interrupted.

## Request access
Portal: VM -> Connect -> *Request access* (passes the requesting IP, time range and ports configured for the VM), or Defender for Cloud -> Just-in-time VM access -> Configured -> *Request access* (choose ports, source IPs and time window).
```powershell
Start-AzJitNetworkAccessPolicy -ResourceId "/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Security/locations/<LOCATION>/jitNetworkAccessPolicies/default" -VirtualMachine $JitPolicyArr
```
For a VM behind Azure Firewall, Defender for Cloud returns connection details including the port mapping from the DNAT table.

## Audit
Defender JIT blade -> VM -> *Activity Log* shows a filtered view of previous operations for that VM with time, date and subscription. Alert on requests outside business hours.

## Gotchas
- Behind NAT/proxy, "My IP" is the egress IP; corporate users share it. Prefer Bastion for routine user access and keep JIT for VMs that must keep a public IP.
- If JIT is enabled on both NSG and firewall, the portal shows only the firewall icon.

## Verify
- [ ] The VM appears on the *Configured* tab with the expected ports.
- [ ] Without a request, a connection to the port fails; after a request from the approved IP it succeeds; after expiry it fails again.

## Checked
Date: 2026-10-31. Confirmed against Defender for Cloud pages "Enable just-in-time access" (just-in-time-access-usage) and "Just-in-time machine access" (just-in-time-access-overview): Plan 2, supported/unsupported VMs, permissions table, 3 hour maximum and `PT3H`, `Set-AzJitNetworkAccessPolicy` and `Start-AzJitNetworkAccessPolicy` usage, deny-all rule and priority behaviour, DNAT mapping, activity log tab.
Removed as unconfirmed: the `az rest` PUT example and api-version (the REST reference page returned 404), the AzureActivity KQL query, and the claim that manual NSG edits are reverted.
Method: documentation only; no commands were run.
