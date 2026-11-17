---
id: computing-software.systems-network-administration.windows-server.firewall-remote-address-scoping
name: firewall-remote-address-scoping
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-firewall, firewall-remote-address-scope, new-netfirewallrule, rdp, winrm]
level: practitioner
status: gated
description: "Restrict management ports (RDP, WinRM, SMB admin shares, WMI) to admin subnets and jump hosts with RemoteAddress scopes, by PowerShell and GPO."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/netsecurity/set-netfirewallrule
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/best-practices-configuring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scoping management ports by remote address

Lateral movement uses RDP, WinRM, SMB and RPC between servers. Most servers only need those from a few admin
systems.

## Tighten existing rules
```powershell
$admin = '10.0.10.0/24','10.0.11.15'          # PAW subnet and jump host
Get-NetFirewallRule -DisplayGroup 'Remote Desktop' | Set-NetFirewallRule -RemoteAddress $admin
Get-NetFirewallRule -Name 'WINRM-HTTP-In-TCP*'   | Set-NetFirewallRule -RemoteAddress $admin
Get-NetFirewallRule -DisplayGroup 'Windows Management Instrumentation (WMI)' | Set-NetFirewallRule -RemoteAddress $admin
Get-NetFirewallRule | Where-Object { $_.Enabled -eq 'True' -and $_.Direction -eq 'Inbound' } |
  Get-NetFirewallAddressFilter | Where-Object RemoteAddress -eq 'Any' | Measure-Object
```
`RemoteAddress` accepts single IPs, subnets, ranges and keywords such as `LocalSubnet`, `DefaultGateway`, `Internet`
and `Intranet` (Set-NetFirewallRule reference).

## GPO
In a GPO, create the inbound rules with Scope > Remote IP addresses set to the admin ranges. Whether local rules merge
with GPO rules is a profile setting (see Microsoft's Windows Firewall best-practices page); pilot any change, because
turning off local rule merge blocks rules created by installers.

## Keep working
- Monitoring and backup servers need their ports too (WMI, SMB, agents); add their IPs to the scope.
- Domain controllers need broad client access for directory services; scope only RDP/WinRM there.
- Cluster nodes need each other unrestricted on cluster networks.

## Verify
```powershell
Test-NetConnection srv01 -Port 3389        # from a normal workstation: should fail
Test-NetConnection srv01 -Port 3389        # from the jump host: should succeed
```
- [ ] The firewall log (if enabled) shows drops from non-admin sources to the management ports.

## Checked
2026-10-28. Confirmed on the Learn Set-NetFirewallRule page: `-RemoteAddress` formats and keywords, `-DisplayGroup` parameter set and
piping Get-NetFirewallRule into it. Removed as unconfirmed: the "Apply local firewall rules = No" setting name, port
numbers for domain controllers, 3389/5985 log-drop wording. The display-group names ('Remote Desktop', WMI group) and the
rule name pattern `WINRM-HTTP-In-TCP*` were not checked on a fetched page
(gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
