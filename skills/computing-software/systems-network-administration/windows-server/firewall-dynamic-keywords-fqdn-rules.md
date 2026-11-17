---
id: computing-software.systems-network-administration.windows-server.firewall-dynamic-keywords-fqdn-rules
name: firewall-dynamic-keywords-fqdn-rules
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-firewall, firewall-dynamic-keywords, netsecurity-module, fqdn-rules, defender-for-endpoint]
level: advanced
status: docs-checked
description: "Use Windows Firewall dynamic keywords for FQDN and auto-resolved address rules: New-NetFirewallDynamicKeywordAddress, Network Protection dependency and limits."
sources:
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/dynamic-keywords
  - https://learn.microsoft.com/en-us/powershell/module/netsecurity/new-netfirewalldynamickeywordaddress
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall dynamic keywords (FQDN rules)

Classic rules need IPs. Dynamic keyword addresses let a rule reference a named object whose IP list can change
without editing the rule, and with AutoResolve, an FQDN.

## Manually maintained address object
```powershell
$id = '{' + [guid]::NewGuid() + '}'
New-NetFirewallDynamicKeywordAddress -Id $id -Keyword 'BackupTargets' -Addresses '10.20.1.10','10.20.1.11'
New-NetFirewallRule -DisplayName 'Allow backup out' -Direction Outbound -Action Allow -RemoteDynamicKeywordAddresses $id -Protocol TCP -RemotePort 443
# later: update the IP list, rule stays the same
Update-NetFirewallDynamicKeywordAddress -Id $id -Addresses '10.20.1.10','10.20.1.12'
```

## FQDN auto-resolve
```powershell
New-NetFirewallDynamicKeywordAddress -Id $id2 -Keyword 'login.microsoftonline.com' -AutoResolve $true
```
AutoResolve uses the Network Protection external callout driver to inspect DNS responses whose query matches an
FQDN rule. Network Protection must be in block or audit mode, and it does not run DNS queries itself: an
application must make the query. A rule whose only remote addresses are unresolved AutoResolve objects has no
remote addresses and is not enforced.

## Typical use: default-deny outbound with FQDN allows
1. Outbound default block on a hardened server profile.
2. Allow rules for DNS, WSUS, Defender, monitoring by FQDN keywords.
3. Test thoroughly: addresses are only learned from DNS responses seen on the host.

## Limits
- Partially qualified names are allowed but FQDNs are preferred; wildcards are supported for hosts (for example `*.contoso.com`).
- `Get-NetFirewallDynamicKeywordAddress -AllAutoResolve` lists AutoResolve keywords with their resolved addresses.
- Related cmdlets: `New-`, `Get-`, `Update-` and `Remove-NetFirewallDynamicKeywordAddress`.

## Verify
- [ ] Rule effective: `Get-NetFirewallDynamicKeywordAddress -AllAutoResolve` shows resolved addresses; traffic passes and other destinations are blocked.

## Checked
2026-10-28. Confirmed against the Learn page "Dynamic keywords" in Windows Firewall and the `New-NetFirewallDynamicKeywordAddress` reference: `-Id`, `-Keyword`, `-Addresses`, `-AutoResolve`, `-RemoteDynamicKeywordAddresses`, `-AllAutoResolve`, Network Protection block/audit requirement, wildcard support, unenforced rule with no resolved addresses. Removed as unconfirmed: `AllowDatagramProcessingOnWinServer`, Defender AV requirement, build-dependent wildcard claim, Intune CSP note, and the nonexistent `Get-NetFirewallDynamicKeywordAddressFilter` check.
Method: documentation only; no commands were run.
