---
id: computing-software.systems-network-administration.windows-server.windows-firewall-netsh-export-import
name: windows-firewall-netsh-export-import
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-firewall, advfirewall-export-import, netsh, firewall-backup, wfw]
level: practitioner
status: docs-checked
description: "Back up, copy and restore Windows Firewall policy with netsh advfirewall export and import, plus reset and per-profile netsh commands for scripted fixes."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netsh-advfirewall
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/netsh-advfirewall-firewall-control-firewall-behavior
  - https://learn.microsoft.com/en-us/powershell/module/netsecurity/get-netfirewallrule
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# netsh advfirewall export and import

## Export / import the policy
```cmd
netsh advfirewall export "<BACKUP>\fw-srv01.wfw"
netsh advfirewall import "<BACKUP>\fw-srv01.wfw"
```
`export <path\filename>` writes the current firewall configuration to a `.wfw` file and
`import <path\filename>` loads one. Check the imported rules afterwards, since an import
changes the active configuration.

## Reset
```cmd
netsh advfirewall reset export "<BACKUP>\before-reset.wfw"
```
`reset [export <path\filename>]` restores the default policy and can export the current one first.

## Common netsh operations
```cmd
netsh advfirewall set allprofiles state on
netsh advfirewall set domainprofile firewallpolicy blockinbound,allowoutbound
netsh advfirewall firewall add rule name="Allow8080" dir=in action=allow protocol=TCP localport=8080
netsh advfirewall set currentprofile logging droppedconnections enable
```
Profile scopes are `currentprofile`, `domainprofile`, `privateprofile`, `publicprofile` and
`allprofiles`. The `netsh advfirewall firewall` context replaces the older `netsh firewall` context,
which may be deprecated. `netsh advfirewall firewall add rule ?` shows the inline help.

## Rules from a GPO
Query the rules of a GPO or other store with PowerShell:
`Get-NetFirewallRule -PolicyStore "<domain>\<GPO name>"` (the cmdlet has a `-PolicyStore` parameter).

## Verify
- [ ] Imported policy shows the expected rules (`Get-NetFirewallRule`) and the application still connects.

## Checked
2026-10-28. Confirmed against the Learn pages "netsh advfirewall" (export, import, reset [export], set allprofiles/firewallpolicy, add rule syntax), "Use netsh advfirewall firewall instead of netsh firewall" (add rule, logging droppedconnections, deprecation wording) and the `Get-NetFirewallRule` reference (`-PolicyStore`). Removed as unconfirmed: what the .wfw contains, the claim that import replaces and ignores GPO rules, the WinRE/Server Core note, the `remoteip` example and the rule-count check.
Method: documentation only; no commands were run.
