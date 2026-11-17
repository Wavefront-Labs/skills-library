---
id: computing-software.systems-network-administration.linux.dns-lookups-with-dig-and-nslookup
name: dns-lookups-with-dig-and-nslookup
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dns, dig, nslookup, host, dns-troubleshooting, dnssec, trace, resolvectl, getent-hosts, lpic-1, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Diagnose DNS with dig: query types and specific servers, +short/+trace/+norecurse, flags and TTLs, DNSSEC checks, nslookup/host, and why apps resolve differently."
sources:
  - https://manpages.debian.org/bookworm/bind9-dnsutils/dig.1.en.html
  - https://manpages.debian.org/bookworm/bind9-dnsutils/nslookup.1.en.html
  - https://manpages.debian.org/bookworm/bind9-host/host.1.en.html
  - https://man7.org/linux/man-pages/man5/resolv.conf.5.html
  - https://www.freedesktop.org/software/systemd/man/latest/resolvectl.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dig and nslookup

**Goal:** prove where a DNS answer comes from, whether it's correct at the authoritative
source, and why an application resolves something different from what you expect.

## 1. Everyday queries
```bash
dig www.example.com                   # A record via resolv.conf's server
dig +short www.example.com AAAA
dig example.com MX +short; dig example.com TXT; dig example.com NS; dig example.com SOA
dig -x 192.0.2.10 +short              # reverse (PTR)
dig @192.0.2.53 www.example.com       # ask a specific server
dig @ns1.example.com www.example.com +norecurse   # authoritative answer only (flag "aa")
```
Read the header: `status: NOERROR | NXDOMAIN | SERVFAIL | REFUSED`; flags `qr rd ra aa ad`;
ANSWER section TTLs count down on caching resolvers (time until refresh). `Query time` and
`SERVER:` show who answered.

## 2. Follow the delegation
```bash
dig +trace www.example.com            # root → TLD → authoritative, bypassing caches
dig +nssearch example.com             # SOA serial from each NS — spots unsynced secondaries
dig example.com DS +short; dig +dnssec www.example.com   # DNSSEC: "ad" flag from validating resolver
delv www.example.com                  # DNS lookup and validation utility
```
SERVFAIL from a validating resolver but answer with `+cd` (checking disabled) → DNSSEC broken.

## 3. nslookup and host
```bash
nslookup www.example.com 192.0.2.53
nslookup -type=mx example.com
host -t txt example.com; host 192.0.2.10
```
Fine for quick checks and on Windows; dig shows more (flags, TTLs, sections).

## 4. Why the app sees something else
dig talks DNS directly; applications use the **NSS** path (`/etc/nsswitch.conf`: files → `/etc/hosts`,
then dns/resolve, mdns, sssd). Compare:
```bash
getent ahosts www.example.com         # what glibc apps get
resolvectl query www.example.com      # systemd-resolved view (per-link DNS, split DNS)
resolvectl status
grep -v '^#' /etc/resolv.conf         # nameserver 127.0.0.53 = resolved stub
```
Also: resolver caches and search domains (`ndots`) turning `api` into `api.corp.example.com`.

## Gotchas
- `dig` ignores `/etc/hosts` — a hosts entry explains "dig is right but the app is wrong".
- Testing a change: query the authoritative server; caches keep old answers until TTL expiry.

## Verify
- [ ] Authoritative (`+norecurse @ns`) and recursive answers agree after TTL expiry.
- [ ] `getent ahosts` matches dig for the name the application uses.

## Checked

Documentation check. Checked 2026-10-27 against the BIND 9 dig, nslookup, delv and host man pages (manpages.debian.org, bookworm, BIND 9.18) and systemd's resolvectl and systemd-resolved sources: `+short`, `+trace` (disables recursion), `+nssearch`, `+norecurse`, `+dnssec`, `+cd`, `+ndots`, `-x`, `@server`, `nslookup -type=`, `host -t`, `delv`, the systemd-resolved stub on 127.0.0.53 and `resolvectl query`. Removed the JVM/Go/nscd cache remark, the negative-caching rule and the package names. Also confirmed the AD, RA and AA header bits as dig options and `getent ahosts` in getent(1).
Run 2026-11-01: `nslookup example.com 1.1.1.1`, `nslookup -type=mx|ns|soa|txt example.com 1.1.1.1` and reverse `nslookup 1.1.1.1 1.1.1.1` worked on Windows (example.com has a null MX, shown as `(root)`; the SOA output lists serial, refresh, retry, expire and default TTL).
Method: documentation only for dig, host, delv and the Linux resolver commands (not installed here); the `nslookup` forms were run on Windows against 1.1.1.1 for example.com.
