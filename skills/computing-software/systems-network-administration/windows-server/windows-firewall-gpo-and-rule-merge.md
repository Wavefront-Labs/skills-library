---
id: computing-software.systems-network-administration.windows-server.windows-firewall-gpo-and-rule-merge
name: windows-firewall-gpo-and-rule-merge
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-firewall, firewall-gpo, local-rule-merge, group-policy, policystore, gpo-firewall-rules, netsh-advfirewall]
level: practitioner
status: docs-checked
description: "Manage Windows Firewall by Group Policy: GPO rule stores, disabling local rule merge, PolicyStore cmdlets, inheritance and troubleshooting which rule wins."
sources:
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/configure
  - https://learn.microsoft.com/en-us/powershell/module/netsecurity/open-netgpo
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall policy by GPO and rule merging

## Edit a GPO's firewall from PowerShell
```powershell
$gpo = Open-NetGPO -PolicyStore 'corp.example.com\Servers-Firewall'
New-NetFirewallRule -GPOSession $gpo -DisplayName 'Allow WinRM from mgmt' -Direction Inbound -Protocol TCP `
  -LocalPort 5985,5986 -RemoteAddress 10.0.10.0/24 -Profile Domain -Action Allow
Set-NetFirewallProfile -GPOSession $gpo -Profile Domain -Enabled True -DefaultInboundAction Block -AllowLocalFirewallRules False
Save-NetGPO -GPOSession $gpo
```
Read-only view: `Get-NetFirewallRule -PolicyStore 'corp.example.com\Servers-Firewall'`.

## Rule merge settings (per profile, Customize > Rule merging)
| Setting | Effect when No |
|---|---|
| Apply local firewall rules | only GPO rules apply; local admin and app-installer rules ignored |

## Effective state
- `Get-NetFirewallRule -PolicyStore ActiveStore` and `Get-NetFirewallProfile -PolicyStore ActiveStore` show the effective policy; PersistentStore holds the local policy.

## Verify
- [ ] ActiveStore shows the GPO rules.
- [ ] Local rules ignored where merge disabled (`AllowLocalFirewallRules False`).

## Checked
2026-10-28: Confirmed on Learn pages open-netgpo, save-netgpo, new-netfirewallrule and set-netfirewallprofile: Open-NetGPO/GPOSession workflow, Save-NetGPO, -AllowLocalFirewallRules (merge of local rules), PolicyStore values ActiveStore and PersistentStore. Removed: GPO console path, connection-security merge row, application-breakage claim, precedence statements (block wins, no last writer), gpresult troubleshooting.
Method: documentation only; no commands were run.
