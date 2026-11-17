---
id: computing-software.systems-network-administration.dns-dhcp.windows-dhcp-name-protection
name: windows-dhcp-name-protection
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, windows-dhcp, name-protection, dhcid, dynamic-dns, name-squatting]
level: practitioner
status: docs-checked
description: "Enable Windows DHCP name protection with Set-DhcpServerv4DnsSetting, and understand DHCID records (RFC 4701) that tie a DNS name to its client."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/set-dhcpserverv4dnssetting
  - https://www.rfc-editor.org/rfc/rfc4701
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Name protection

Without protection, a client can register a name already used by another device and overwrite its DNS record. With name protection enabled and an existing record matching the name, the DNS update for the client fails instead of overwriting (Set-DhcpServerv4DnsSetting docs).

## Enable
```powershell
Set-DhcpServerv4DnsSetting -ComputerName dhcp1 -NameProtection $true                      # server level
Set-DhcpServerv4DnsSetting -ComputerName dhcp1 -ScopeId 10.30.0.0 -NameProtection $true   # one scope
```
- With no `-ScopeId`, `-IPAddress` or `-PolicyName`, the setting applies at server level; `-ScopeId` targets a scope; `-IPAddress` a reservation.
- The MS example enables it on a scope with `-DynamicUpdates OnClientRequest`, so it is not tied to `Always`. The same page says name protection works by creating DHCID resource records.
- `-DeleteDnsRROnLeaseExpiry` can only be set when `-DynamicUpdates` is `Always` or `OnClientRequest`.

## What a DHCID record is (RFC 4701)
- DNS type 49, class IN only. Its RDATA is a 2-octet identifier type, a 1-octet digest type (1 = SHA-256) and the digest of the client identifier plus the FQDN.
- An updater compares its own hash with DHCID RRs on the name; a mismatch means a different client owns the name. The RFC leaves the response to site policy.
- Identifier types: 0x0000 htype+chaddr, 0x0001 DHCPv4 client-identifier option, 0x0002 DUID.
- DNS updates must use authentication such as TSIG. The hash can be brute-forced given common MAC addresses.

## Checked
Method: 2026-11-08 read the cmdlet page and RFC 4701. The older Microsoft name-protection page returned 404 and was dropped. Removed as unsupported: that name protection requires `DynamicUpdates Always`, the event-log behaviour, "second client gets address but no record", failover credential sharing, and the claim that pre-existing records without DHCID are never overwritten (the cmdlet page says only that an existing matching record makes the update fail). Test in a lab before enabling over legacy records.

## Verify
- [ ] `Get-DhcpServerv4DnsSetting` shows NameProtection true at the intended level, and a test client reusing an existing name does not replace its A record.
