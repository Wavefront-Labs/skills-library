---
id: computing-software.systems-network-administration.dns-dhcp.response-policy-zones-rpz
name: response-policy-zones-rpz
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, recursive-resolver, rpz, response-policy-zone, dns-firewall, dns-blocklist, nxdomain-rewrite, walled-garden, threat-intelligence-feed, rpz-ip, rpz-nsdname, unbound-rpz, dns-security]
level: practitioner
status: verified
description: "Build a DNS firewall with Response Policy Zones on BIND: zone format and actions, local overrides, subscribing to threat feeds over IXFR, logging hits and passthru exceptions."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/chapter6.html
  - https://datatracker.ietf.org/doc/html/draft-vixie-dnsop-dns-rpz-00
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Response Policy Zones (RPZ)

RPZ lets a recursive resolver rewrite answers for names, answer IPs, or nameservers listed in
special zones: block malware domains, redirect to a walled garden, or override names locally.

## Configure
```
options {
    response-policy {
        zone "rpz.local" policy given;           // our overrides first: first match wins
        zone "rpz.threatfeed" policy given;
    } qname-wait-recurse no;                     // optional: apply QNAME rules without recursing first (see below)
};
zone "rpz.local"      { type primary;   file "/etc/bind/db.rpz.local"; allow-query { none; }; };
zone "rpz.threatfeed" { type secondary; primaries { 203.0.113.10 key feed-tsig; }; file "rpz.feed.db"; allow-query { none; }; };
```
Policy zones are ordinary DNS zones, so feeds can be transferred like any secondary zone (TSIG recommended). Up to 64 policy zones can be listed in one `response-policy`. Restrict queries to the policy zones (`allow-query`).

## Zone format (owner name = trigger, RDATA = action)
```
$TTL 300
@ SOA localhost. hostmaster.localhost. 2026101601 3600 600 86400 300
@ NS  localhost.
bad.example.com          CNAME .                 ; NXDOMAIN
*.bad.example.com        CNAME .                 ; and all subdomains
tracker.example.net      CNAME *.                ; NODATA
phish.example.org        A     10.0.0.80         ; redirect to walled-garden page
allowed.example.com      CNAME rpz-passthru.     ; exception, never rewritten
drop.example.biz         CNAME rpz-drop.         ; response discarded, nothing sent
force-tcp.example.biz    CNAME rpz-tcp-only.     ; truncated UDP answer forces TCP retry
32.10.113.0.203.rpz-ip   CNAME .                 ; any answer containing 203.0.113.10 (prefixlength.B4.B3.B2.B1)
ns.evil.example.rpz-nsdname CNAME .              ; anything served by that nameserver
```
Put exceptions (passthru) in the first-listed local zone: the triggered record in the zone listed first in `response-policy` wins, and within a zone the order of preference is CLIENT-IP, QNAME, IP, NSDNAME, NSIP. Per-zone `policy` overrides are GIVEN (use the record's action), DISABLED (log only), PASSTHRU, DROP, TCP-Only, NXDOMAIN, NODATA, or `CNAME domain`.

By default BIND recurses before considering triggers, so a listed name's operators cannot tell RPZ is in use; `qname-wait-recurse no` skips that for speed, and the ARM warns it can make errors such as SERVFAIL appear rewritten. `nsdname-wait-recurse no` and `nsip-wait-recurse no` similarly skip lookups for NSDNAME and NSIP rules (default `yes`).

## Logging and operations
```
logging { channel rpz_log { file "/var/log/named/rpz.log" versions 5 size 50m; print-time yes; };
          category rpz { rpz_log; }; };
```
The `rpz` category logs errors in policy zone files and rewritten responses (rewriting attempts only at the highest debug levels): feed it to the SIEM. `rndc reload rpz.local` after edits (bump serial).

## Gotchas
- Clients using DoH/DoT to external resolvers bypass RPZ; control that at the network or endpoint policy level.
- IP and NSIP/NSDNAME triggers can affect many unrelated names (shared hosting or CDN addresses); prefer QNAME triggers where possible. The ARM calls NSDNAME and NSIP rules unreliable in some cases.
- DNSSEC: by default RPZ actions are not applied to queries with DO=1 when DNSSEC records exist for the name in the original zone; `break-dnssec yes` applies them anyway, and the rewritten results cannot validate.
- RPZ rules are applied after the access-control checks; clients not permitted to use the resolver get REFUSED regardless of RPZ.
- `servfail-until-ready yes` makes the server answer SERVFAIL until all policy zones are loaded (by default it may answer earlier).

## Verify
- [ ] `dig bad.example.com @resolver` returns NXDOMAIN; passthru names resolve.
- [ ] RPZ log lines appear for rewritten responses; feed zone serial updates (`rndc zonestatus rpz.threatfeed`).

## Checked

Date: 2026-10-26. BIND 9 ARM and man-page sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27; grammar cross-checked on bind-9.20), read on 2026-10-26. Confirmed in reference.rst and rpz.inc.rst: response-policy grammar and 64-zone limit, trigger and action types, rpz-ip/rpz-nsdname owner encoding, rpz-passthru/rpz-drop/rpz-tcp-only, policy override list, precedence rules, break-dnssec and DO=1 default, recursive-only default, servfail-until-ready, qname-wait-recurse semantics, rpz logging category. Removed the unconfirmed feed-vendor list and CDN claim wording, and corrected the DNSSEC note.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (BIND 9.20.30, resolver forwarding to an authoritative instance): response-policy with `qname-wait-recurse no` and two policy zones (primary and secondary over TSIG) parsed and loaded with allow-query none; QNAME rules for NXDOMAIN, wildcard NXDOMAIN, NODATA (`CNAME *.`), local-data A, rpz-passthru, rpz-drop (query timed out), rpz-tcp-only (UDP answer had the TC flag set, TCP retry answered); an rpz-ip rule on 203.0.113.10 (log line `rpz IP NXDOMAIN rewrite`); the first-listed zone winning over the feed's passthru for the same name; the rpz log category lines; a client outside the ACL getting REFUSED; edit plus `rndc reload rpz.local` taking effect. Not run: NSDNAME and NSIP rules, per-zone policy overrides, break-dnssec, servfail-until-ready, nsdname-wait-recurse, the 64-zone limit.
