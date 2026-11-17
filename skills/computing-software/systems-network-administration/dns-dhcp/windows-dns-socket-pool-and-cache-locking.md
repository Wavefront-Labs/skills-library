---
id: computing-software.systems-network-administration.dns-dhcp.windows-dns-socket-pool-and-cache-locking
name: windows-dns-socket-pool-and-cache-locking
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, windows-dns, socket-pool, cache-locking, cache-poisoning, dnscmd]
level: practitioner
status: docs-checked
description: "Harden Windows DNS against cache poisoning with cache locking percentage and pollution protection, and check the settings across domain controllers."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/set-dnsservercache
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dnscmd
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cache locking on Windows DNS

## Cache locking
`-LockingPercent` is a percentage of the original TTL during which the DNS server will not
overwrite a cached entry. At 50, a cached entry is not overwritten for half of its TTL. The
default is 100, meaning entries are not overwritten for the whole TTL. Lowering it lets changed
records refresh sooner but weakens the protection; keep the default unless you have a reason.
```powershell
Get-DnsServerCache | Select LockingPercent, MaxTTL, MaxNegativeTtl
Set-DnsServerCache -LockingPercent 100
```

## Related Set-DnsServerCache parameters
`-PollutionProtection <Boolean>` (cache pollution protection, see the "Securing the DNS Server
Service" article the cmdlet page links), `-MaxTtl <TimeSpan>` and `-MaxNegativeTtl <TimeSpan>`,
for example `Set-DnsServerCache -MaxTTL 02.00:00:00 -MaxNegativeTtl 00.00:20:00`.

## Check across DCs
```powershell
Get-ADDomainController -Filter * | ForEach-Object {
  [pscustomobject]@{DC=$_.Name; Lock=(Get-DnsServerCache -ComputerName $_.Name).LockingPercent}
}
```

## Socket pool
The socket pool (randomised source ports for outbound queries) is set with `dnscmd`, but the
current `dnscmd` page does not document the socket pool options. Look up the exact switches,
defaults and limits for your Windows Server version in its DNS server documentation before
changing them; this skill gives no figures.

## Verify
- [ ] Every DNS server reports the intended LockingPercent.

## Checked
2026-11-01. Confirmed on the Set-DnsServerCache cmdlet page: -LockingPercent semantics and default
100, -PollutionProtection, -MaxTtl, -MaxNegativeTtl and the example. Removed (not on the cmdlet or
dnscmd pages): the socket pool default and maximum, dnscmd socket pool switches, the
Set-DnsServerRecursion and response rate limiting lines, the "default on" claim and the external
port test.
Method: documentation only; no commands were run.
