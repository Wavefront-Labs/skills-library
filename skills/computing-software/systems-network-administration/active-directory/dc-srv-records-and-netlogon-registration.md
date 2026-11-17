---
id: computing-software.systems-network-administration.active-directory.dc-srv-records-and-netlogon-registration
name: dc-srv-records-and-netlogon-registration
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, dc-health, dcdiag, dc-srv-records, nltest-dsgetdc, netlogon-dns, msdcs, dc-locator]
level: practitioner
status: docs-checked
description: "Verify and repair domain controller DNS SRV records: _msdcs zone checks, netlogon.dns, nltest /dsgetdc, forcing re-registration and stale DC record cleanup."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/verify-srv-dns-records-have-been-created
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/dc-locator
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dcdiag
  - https://learn.microsoft.com/en-us/powershell/module/dnsclient/resolve-dnsname
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verify DC SRV records and Netlogon registration

Clients find DCs through DNS SRV and A records that the Netlogon service registers (the DC locator reads
`_ldap._tcp.<DnsDomainName>`-style records through `DsGetDcName`). Missing or stale records mean logons hit far or dead
DCs and domain joins fail.

## Check what clients see
```powershell
Resolve-DnsName -Type SRV _ldap._tcp.dc._msdcs.corp.example.com
Resolve-DnsName -Type SRV _kerberos._tcp.Default-First-Site-Name._sites.dc._msdcs.corp.example.com
Resolve-DnsName -Type SRV _gc._tcp.corp.example.com
nltest /dsgetdc:corp.example.com            # which DC the locator returns, flags, site
nltest /dsgetdc:corp.example.com /force /gc /kdc
nltest /dsgetsite
```
`/force` bypasses the cache and queries DNS; `/gc` and `/kdc` return only global catalogs or Kerberos KDCs.
In the DNS console the locator records sit under `_msdcs\dc\_tcp` and `_msdcs\dc\_sites\<site>\_tcp` in the domain zone.

## What should be registered
`%SystemRoot%\System32\Config\netlogon.dns` on each DC lists the SRV locator records it must register (and is what you
compare against on non-Microsoft DNS servers). Compare it against DNS.

## Force re-registration
```cmd
nltest /dsregdns
ipconfig /registerdns
dcdiag /test:dns /DnsRecordRegistration
```
`nltest /dsregdns` re-registers the DC's DNS records. `dcdiag /test:dns /DnsRecordRegistration` checks that the A, CNAME
and SRV records are registered and builds an inventory report. Review the DNS client settings on DCs so they point at DNS
servers that host the AD zones.

## Stale records
Records for demoted or dead DCs point clients at nothing. After metadata cleanup remove leftover records from the
`_msdcs` zone and from the domain zone (DNS Manager, or `Remove-DnsServerResourceRecord`), including the DC's host
records.

## Site coverage
`nltest /dsgetsite` run on a client shows the AD site it resolves to (subnet objects must be defined), and
`nltest /dsgetsitecov` on a DC lists the sites it covers.

## Verify
- [ ] netlogon.dns entries all resolve; `nltest /dsgetdc` returns a local-site DC.

## Checked

Date: 2026-10-27. Documentation: Microsoft Support "verify SRV DNS records", Locating domain controllers in Windows and
Windows Server, dcdiag reference, nltest reference (Windows Server 2008 R2 archive page), Resolve-DnsName and
Remove-DnsServerResourceRecord module pages.
Confirmed: SRV record names and zone locations, netlogon.dns path and purpose, `nltest /dsgetdc /force /gc /kdc`,
`/dsgetsite`, `/dsgetsitecov`, `/dsregdns`, `dcdiag /test:dns /DnsRecordRegistration`.
Removed unconfirmed claims: the GUID CNAME query (it used the invocation ID), the `RegisterInDNS /DnsDomain` form, the
24-hour Netlogon refresh and scavenging statements, the automatic-site-coverage wording, and the loopback-last DNS rule.

Method: documentation only; no commands were run.
