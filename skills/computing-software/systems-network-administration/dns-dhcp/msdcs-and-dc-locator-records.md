---
id: computing-software.systems-network-administration.dns-dhcp.msdcs-and-dc-locator-records
name: msdcs-and-dc-locator-records
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [windows-dns, msdcs, dc-locator, srv, active-directory, netlogon, dcdiag, sites]
level: practitioner
status: docs-checked
description: "Troubleshoot AD domain controller location via DNS: the _msdcs SRV records, site-specific records, Netlogon.dns and how the locator queries DNS."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/verify-srv-dns-records-have-been-created
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/dc-locator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# _msdcs and DC locator records

Domain controllers register SRV records in DNS, including records for key capabilities such as
the Key Distribution Center or Global Catalog and records describing locality, such as AD site
records. Clients query DNS for the SRV records and then ping those servers with UDP-based LDAP
pings. If the records are missing or wrong, locating a DC fails or lands on a poor choice.

## How the locator works
- The client's locator call goes to the local Netlogon service, which implements `DsGetDcName`,
  the primary DC location API; Microsoft recommends DNS-based discovery over NetBIOS-based.
- Netlogon reads SRV and A records from DNS in the form `_<service>._<protocol>.<DnsDomainName>`,
  for example `_ldap._tcp.<DnsDomainName>`.

## Where the records live
Active Directory creates its SRV records under the domain's forward lookup zone, for example
`_msdcs/dc/_sites/Default-First-Site-Name/_tcp`. A record should appear there for `_kerberos` and
`_ldap`.

## Query them
```
nslookup -type=SRV _ldap._tcp.dc._msdcs.<domain>
Resolve-DnsName _ldap._tcp.<Site>._sites.dc._msdcs.<domain> -Type SRV
```
The Microsoft troubleshooting article uses `_ldap._tcp.dc._msdcs.<Domain_Name>` in nslookup to
verify the records.

## With non-Microsoft DNS servers
View `Netlogon.dns` in the `%systemroot%\System32\Config` folder: it lists the records the DC
tries to register. The first record is the DC's LDAP SRV record `_ldap._tcp.<Domain_Name>`.

## Verify
- [ ] SRV queries return every live DC, and only live DCs; site queries return the local site's DCs.

## Checked
2026-11-01. Confirmed on the Microsoft troubleshooting article (SRV record folders, _kerberos and
_ldap, nslookup query, Netlogon.dns location and first record) and the DC Locator article
(Netlogon and DsGetDcName, DNS-based discovery, SRV and A lookups, UDP LDAP pings). Removed (not on
those pages): the table of PDC, GC and per-DC GUID names, the `nltest` and `dcdiag` commands,
net stop/start netlogon, causes list, and the BIND/Infoblox delegation advice.
Method: documentation only; no commands were run.
