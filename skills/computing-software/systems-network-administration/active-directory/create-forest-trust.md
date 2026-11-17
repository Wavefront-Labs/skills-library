---
id: computing-software.systems-network-administration.active-directory.create-forest-trust
name: create-forest-trust
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-trusts, forest-trust, new-forest-trust, trust-dns-forwarders, conditional-forwarder, netdom-trust, mergers-acquisitions, two-way-trust, transitive-trust]
level: practitioner
status: gated
description: "Create a two-way forest trust: conditional forwarders both ways, firewall ports, New Trust wizard or netdom, then validation and least-access scoping."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netdom-trust
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/config-firewall-for-ad-domains-and-trusts
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/add-dnsserverconditionalforwarderzone
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a forest trust

**Goal:** let users in forest A access resources in forest B (and/or vice versa), e.g. during
an acquisition, without merging directories.

## 1. Name resolution both ways
Each forest must resolve the other's DC SRV records. On a DC in each forest:
```powershell
Add-DnsServerConditionalForwarderZone -Name 'fabrikam.example' -MasterServers 10.50.0.10,10.50.0.11 `
  -ReplicationScope Forest
```
Test with `Resolve-DnsName _ldap._tcp.dc._msdcs.fabrikam.example -Type SRV` and `nltest /dsgetdc:fabrikam.example` (gated: unconfirmed, source is paywalled or blocked).

## 2. Network
Ports from the Microsoft firewall article for DCs on Windows Server 2008 and later (not every port is needed in every scenario; check the article): 135/TCP RPC endpoint mapper; RPC dynamic range 49152-65535/TCP; 389 TCP/UDP LDAP; 636/TCP LDAPS; 3268/TCP and 3269/TCP global catalog; 53 TCP/UDP DNS; 88 TCP/UDP Kerberos; 464 TCP/UDP Kerberos password change; 445/TCP SMB; 123/UDP W32Time. RPC for LSA, SAM and Netlogon can be pinned to fixed ports.

## 3. Create the trust
GUI: the New Trust Wizard in Active Directory Domains and Trusts creates one or both sides of the trust; creating both sides needs administrative credentials for each domain, and a strong trust password is generated automatically. Forest trusts need forest functional level 2003 or later (gated: unconfirmed, source is paywalled or blocked).

netdom (from the forest A root domain; `/usero` and `/passwordo` are the account for the first-named trusting domain, `/userd` and `/passwordd` the account for the `/domain:` domain):
```cmd
netdom trust ad.example.com /domain:fabrikam.example /add /twoway /usero:AD\admin /passwordo:* /userd:FABRIKAM\admin /passwordd:*
netdom trust ad.example.com /domain:fabrikam.example /ForestTransitive:yes
```
`/ForestTransitive:yes` marks the trust forest transitive (root domain only); run it without a value to display the current state.

## 4. Scope access
- Prefer **selective authentication** for acquisitions (`netdom trust ... /selectiveauth:yes`, valid on outbound forest and external trusts): users from B can then only authenticate to computers where they have *Allowed to Authenticate* (gated: unconfirmed, source is paywalled or blocked) (see the trust-selective-authentication skill).
- Grant access via domain local groups in the resource forest containing users or global groups from the other forest.

## Verify
```powershell
Get-ADTrust -Filter *
```
```cmd
netdom trust ad.example.com /domain:fabrikam.example /verify
netdom trust ad.example.com /domain:fabrikam.example /selectiveauth
```
- [ ] Trust verifies from both forests.
- [ ] A test user from B can access the intended share in A, and nothing else if selective.

## Checked
Checked 2026-10-27 against Microsoft Learn (netdom trust reference; Configure a firewall for Active Directory domains and trusts; Trust types, Windows Server 2003 documentation; Add-DnsServerConditionalForwarderZone and Get-ADTrust references, Windows Server 2025).
- Confirmed: Add-DnsServerConditionalForwarderZone -MasterServers and -ReplicationScope Forest; netdom trust /add /twoway /usero /passwordo /userd /passwordd /ForestTransitive /verify /selectiveauth syntax and meanings; the firewall port table including 49152-65535 dynamic range, 464 and 123.
- Wrong in the earlier text: the netdom example swapped the /usero and /userd accounts and used an invalid `/realm:no`; both are corrected.
- Gated: the nltest check, the forest functional level requirement and Allowed to Authenticate behaviour.
- Removed: Get-ADTrust property names, which the readable cmdlet page does not list.

Method: documentation only; no commands were run.
