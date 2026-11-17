---
id: computing-software.systems-network-administration.dns-dhcp.dns-records-and-resolution-troubleshooting
name: dns-records-and-resolution-troubleshooting
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dhcp, dig, nslookup, resolvectl, dig-trace, a-record, aaaa, cname, mx, txt, srv, ptr, ns, soa, caa, ttl, soa-serial, delegation, glue-records, split-horizon, split-brain-dns, negative-caching, dora, dhcp-scope, dhcp-reservation, dhcp-options, ip-helper-address, dhcp-relay, bind, windows-dns, kea, dnsmasq]
level: practitioner
status: docs-checked
description: "DNS records, TTLs, SOA serials, delegation and glue, dig +trace troubleshooting, split-horizon, plus DHCP scopes, reservations, options 3/6/15, DORA and relay."
sources:
  - https://www.rfc-editor.org/rfc/rfc1034
  - https://www.rfc-editor.org/rfc/rfc2181
  - https://www.rfc-editor.org/rfc/rfc2308
  - https://www.rfc-editor.org/rfc/rfc1912
  - https://www.rfc-editor.org/rfc/rfc2131
  - https://www.rfc-editor.org/rfc/rfc2132
  - https://www.rfc-editor.org/rfc/rfc3397
  - https://www.rfc-editor.org/rfc/rfc3927
  - https://www.rfc-editor.org/rfc/rfc8659
  - https://bind9.readthedocs.io/en/latest/manpages.html
  - https://www.freedesktop.org/software/systemd/man/latest/resolvectl.html
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DNS records and resolution troubleshooting (with DHCP) — follow the answer, not the symptom

**Goal:** make DNS changes that take effect when you expect, find which server is giving
the wrong answer in minutes, and keep DHCP handing out working settings.

## 1. Record types you will touch
| Type | Use | Gotcha |
|---|---|---|
| A / AAAA | name → IPv4 / IPv6 | |
| CNAME | alias → another name | A node with a CNAME must hold no other data (RFC 1034), so not at the zone apex |
| MX | mail server (priority + host) | The target must not be an alias (RFC 2181 10.3) |
| TXT | SPF, DKIM, DMARC, verification | |
| SRV | service location (`_ldap._tcp.<DOMAIN>`) | |
| PTR | IP → name (reverse zone) | |
| NS / SOA | delegation / zone metadata | NS targets must not be aliases (RFC 2181) |
| CAA | which CAs may issue certificates | Restricts issuance (RFC 8659) |

## 2. Change safely: TTL and serial
1. **Lower the TTL in advance.** At least one old-TTL period before the change (e.g. 24 h
   ahead if TTL is 86400), drop it to a short value such as 300. Resolvers hold the old value
   for the old TTL.
2. Make the change; verify; raise the TTL again afterwards.
3. **Bump the SOA serial** on primary zones (RFC 1912 recommends `YYYYMMDDnn`: year, month, day,
   revision number), or secondaries will not see the change. Then reload the zone and compare
   `dig @<SECONDARY> <zone> SOA +short` with the primary.
4. **Negative caching:** an NXDOMAIN is cached (RFC 2308), with the lifetime taken from the SOA
   negative-caching TTL. Querying a name before you create it can make it "not exist" for that long.

## 3. Delegation and glue
The parent zone's NS records point to the child's name servers. If those servers are
*inside* the child zone (`ns1.example.com` for `example.com`), the parent must also hold
**glue** A/AAAA records, or resolution loops. NS sets at parent and child should match;
a "lame delegation" (a listed server that does not answer authoritatively, RFC 1912)
causes intermittent failures.

## 4. Troubleshooting ladder
```bash
dig example.com A                         # what my resolver says
dig @192.0.2.53 example.com A             # ask a specific server
dig example.com A +trace                  # walk root → TLD → authoritative, with recursion off
dig example.com NS +short ; dig example.com SOA +short   # who is authoritative, serial
dig -x 192.0.2.25                         # reverse lookup
dig example.com A +norecurse @<AUTH_NS>   # no recursion: ask that server only
resolvectl query example.com              # systemd-resolved hosts; resolvectl status shows per-link servers
```
Windows: `nslookup example.com 192.0.2.53`, `Resolve-DnsName example.com -Server 192.0.2.53`,
`ipconfig /displaydns` (shows the resolver cache including hosts-file entries), `ipconfig /flushdns`
(discards negative and other dynamically added entries).

Read the `status:` field: `NXDOMAIN` = name does not exist; `NOERROR` with zero answers =
name exists but has no data of that type; `SERVFAIL` = the server could not process the query.

## 5. Split-horizon
Same name, different answers inside vs outside (e.g. `app.example.com` → private IP
internally). A frequent cause of "works inside, fails outside" is a record updated in one view
only. Use a subdomain you own for an internal AD domain (e.g. `ad.example.com`).

## 6. DHCP essentials
**DORA:** Discover (broadcast) → Offer → Request (broadcast) → Ack (RFC 2131). A client on a
`169.254.x.x` address (169.254/16 is the IPv4 link-local range, RFC 3927) has not obtained a lease.
- **Scope:** address range, exclusions for statics, lease time.
- **Reservations:** MAC (or client ID) → fixed IP; keeps addressing central.
- **Options:** 3 router (gateway), 6 DNS servers, 15 domain name, 42 NTP servers, 119 domain search list
  (RFC 3397), 66/67 TFTP server name and bootfile name (RFC 2132).
- **Relay:** broadcasts do not cross routers, so each VLAN gateway needs a DHCP relay agent
  pointing at the server. The relay fills in `giaddr` (the relay's address), which the server uses to choose
  the subnet to allocate from (RFC 2131).

## Verify
- [ ] TTL lowered before and restored after the change window.
- [ ] Every authoritative server returns the same SOA serial.
- [ ] `dig +trace` resolves the name from the root without errors.
- [ ] Internal and external views both return the intended answers.
- [ ] A client on each VLAN gets an address, gateway (3), DNS (6) and domain (15) via DHCP.

## Checked
Date: 2026-10-28.
Confirmed: RFC 1034 (CNAME exclusivity, glue and delegation), RFC 2181 (MX and NS targets must not be aliases),
RFC 2308 (negative caching), RFC 1912 (`YYYYMMDDnn`, lame delegation), RFC 2131 (DORA, giaddr), RFC 2132
(options 3, 6, 15, 42, 66, 67), RFC 3397 (option 119), RFC 3927 (169.254/16), the BIND 9 dig man page (+trace,
+norecurse, -x, status) and the Learn ipconfig page (/displaydns, /flushdns).
Removed (not confirmed on fetched pages): stale-AAAA remark, one-SPF-record and 255-character TXT rules, "AD logon
depends on SRV", PTR ownership remark, Windows 8-day default lease and Wi-Fi lease advice, MAC randomisation,
`+cd`/DNSSEC diagnosis tip, browser DoH and VPN resolver remark, `.local` and mDNS remark, nslookup behaviour notes,
AD-integrated zone serial handling, `rndc reload` syntax, Cisco `ip helper-address`, DHCP failover/split-scope figures,
the 80% utilisation target and the DHCP snooping remark.
Run 2026-11-01: `nslookup example.com <server>` and `Resolve-DnsName example.com -Server 1.1.1.1` worked on Windows. `ipconfig /displaydns` was not run, and dig and resolvectl are not installed here, so the ladder stays documentation only.
Method: documentation only except the Windows nslookup and Resolve-DnsName forms.
