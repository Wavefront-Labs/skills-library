---
id: computing-software.systems-network-administration.windows-server.firewall-connection-security-and-domain-isolation
name: firewall-connection-security-and-domain-isolation
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-firewall, connection-security-rules, domain-isolation, ipsec, new-netipsecrule, server-isolation, authenticated-bypass]
level: advanced
status: docs-checked
description: "Implement IPsec domain and server isolation with connection security rules: request vs require, New-NetIPsecRule and authenticated firewall rules."
sources:
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/domain-isolation-policy-design
  - https://learn.microsoft.com/en-us/powershell/module/netsecurity/new-netipsecrule
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection security rules and domain isolation

Domain isolation: domain members require IPsec-authenticated (Kerberos) traffic between
each other, so unmanaged devices cannot talk to servers. Server isolation adds "only
these computer groups may connect".

## Rules
```powershell
New-NetIPsecRule -DisplayName 'Domain isolation' -InboundSecurity Request -OutboundSecurity Request `
  -Phase1AuthSet <AUTHSET_NAME>
```

## Server isolation
On the protected server, an inbound firewall rule with `-Authentication Required` and
remote computer restriction:
```powershell
New-NetFirewallRule -DisplayName 'SQL from app servers only' -Direction Inbound -Protocol TCP -LocalPort 1433 `
  -Authentication Required -RemoteMachine 'D:(A;;CC;;;<SID of AppServers group>)' -Action Allow
```
Authenticated bypass (`-OverrideBlockRules $true` with `-Authentication Required`) lets authenticated peers through block
rules (see the New-NetFirewallRule examples).

## Gotchas
- Require mode before every client can authenticate = outage. Request mode first, always.

## Verify
- [ ] Main Mode SAs exist between members; non-domain device cannot reach isolated server.

## Checked

2026-10-28. Confirmed against: New-NetIPsecRule reference (InboundSecurity/OutboundSecurity Request and Require, Phase1AuthSet) and New-NetFirewallRule reference (Authentication Required, RemoteMachine, OverrideBlockRules). Removed (not confirmable from the cited pages): rollout order and exemption list, IPsec auth-set cmdlets and -Profile, GPO path, monitoring cmdlets and event IDs, NAT-T note, example addresses.

Method: documentation only; no commands were run.
