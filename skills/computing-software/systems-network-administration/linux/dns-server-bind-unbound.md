---
id: computing-software.systems-network-administration.linux.dns-server-bind-unbound
name: dns-server-bind-unbound
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, bind, bind9, named, unbound, dns-server, authoritative-dns, recursive-resolver, zone-file, soa, serial, axfr, zone-transfer, tsig, dnssec, rndc, named-checkconf, named-checkzone, forwarders, views, split-horizon, lpic-2, networking, sysadmin, unbound-conf, local-zone, allow-query]
level: advanced
status: docs-checked
description: "Run DNS on Linux: Unbound as validating recursive resolver, BIND 9 as authoritative primary/secondary with zone files, serials, TSIG transfers, rndc, and pre-serve zone checks."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://datatracker.ietf.org/doc/html/rfc1035
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# DNS server: BIND 9 and Unbound — authoritative and recursive done separately

**Goal:** a recursive resolver for your clients (Unbound) and an authoritative pair for
your zones (BIND), never one server doing both for the internet.

## 1. Unbound — caching, validating resolver for a site
```bash
# install unbound with your distro's package manager
```
`/etc/unbound/unbound.conf.d/site.conf`:
```
server:
    interface: 0.0.0.0
    interface: ::0
    access-control: 10.0.0.0/8 allow
    access-control: 0.0.0.0/0 refuse
    prefetch: yes
    cache-min-ttl: 0
    num-threads: 4
    msg-cache-size: 64m
    rrset-cache-size: 128m
    hide-identity: yes
    hide-version: yes
    private-address: 10.0.0.0/8          # rebind protection; add RFC1918 you use
    domain-insecure: "corp.example"      # internal zone without DNSSEC chain
    local-zone: "corp.example." transparent
stub-zone:                                # send internal zone to your authoritative servers
    name: "corp.example"
    stub-addr: 10.0.0.53
forward-zone:                             # optional: forward everything else to an upstream (DoT)
    name: "."
    forward-tls-upstream: yes                 # also set tls-cert-bundle in server:, or the upstream cannot be authenticated
    forward-addr: <upstream-ip>@853#<tls-auth-name>
```
```bash
unbound-checkconf && systemctl enable --now unbound
unbound-control status; unbound-control stats_noreset | grep -E 'total.num|cachehits'
unbound-control flush_zone corp.example   # after an internal change
dig @127.0.0.1 example.com +dnssec        # look for the "ad" flag (needs a trust anchor, see below)
```
- DNSSEC validation needs a trust anchor: `auto-trust-anchor-file` (RFC 5011 tracking) defaults to empty, so set it (packaged configs usually do). Without
  a `forward-zone`, Unbound recurses itself instead of asking an upstream resolver.
- `domain-insecure` is required for internal zones you don't sign, or validation
  returns SERVFAIL for them.
- If another resolver (for example a systemd-resolved stub) already listens on port 53 of an address Unbound is configured on, one of them fails to bind; check with `ss -lntup`.

## 2. BIND 9 — authoritative
```bash
# install BIND 9 and its utilities with your distro's package manager; the config path is distro-specific
```
`named.conf` (primary):
```
options {
    directory "/var/named";
    listen-on port 53 { any; };
    recursion no;                        # authoritative only
    allow-query { any; };
    allow-transfer { none; };            # per zone below
};
key "xfer-key" { algorithm hmac-sha256; secret "<tsig-keygen output>"; };
zone "corp.example" IN {
    type primary;                        # older releases spell this "master"
    file "corp.example.zone";
    allow-transfer { key xfer-key; };
    also-notify { 10.0.0.54; };
};
zone "0.0.10.in-addr.arpa" IN { type primary; file "10.0.0.rev"; allow-transfer { key xfer-key; }; };
```
Secondary: `type secondary; primaries { 10.0.0.53 key xfer-key; }; file "slaves/corp.example.zone";`
plus the same `key` block (generate with `tsig-keygen xfer-key`).

Zone file `/var/named/corp.example.zone`:
```
$TTL 3600
$ORIGIN corp.example.
@   IN SOA ns1.corp.example. hostmaster.corp.example. (
        2026101501 ; serial YYYYMMDDnn — MUST increase on every change
        3600       ; refresh
        900        ; retry
        1209600    ; expire (2 weeks)
        300 )      ; negative-cache TTL
    IN NS   ns1.corp.example.
    IN NS   ns2.corp.example.
    IN MX 10 mail.corp.example.
ns1  IN A  10.0.0.53
ns2  IN A  10.0.0.54
mail IN A  10.0.0.25
www  IN CNAME web01
web01 IN A 10.0.0.80
_acme-challenge IN TXT "..."
```
```bash
named-checkconf -z                       # config + test-loads all zones of type primary
named-checkzone corp.example /var/named/corp.example.zone
systemctl enable --now named; rndc reload corp.example; rndc status
dig @10.0.0.54 corp.example SOA +short   # secondary serial must match primary
rndc retransfer corp.example             # force on the secondary
```
- Forgetting the serial bump is the #1 "secondary never updates" cause; the
  secondary only transfers if the primary's serial is higher. Check
  `journalctl -u named | grep -i 'transfer\|serial'`.
- A CNAME at the zone apex is not allowed (other record types such as SOA and NS live there); use A/AAAA records. Trailing dots matter —
  `mail.corp.example` without the dot becomes `mail.corp.example.corp.example.`.
- Dynamic updates (DHCP/`nsupdate`): `allow-update { key ddns-key; };` and never
  hand-edit the zone file afterwards (`rndc freeze zone; edit; rndc thaw zone`).
- DNSSEC: `dnssec-policy default;` in the zone block (built-in policies are `default`, `insecure` and `none`) handles keys, signing and rollovers; `inline-signing` is the default for DNSSEC zones. The default policy uses one ECDSAP256SHA256 CSK and may change in future releases. Publish the DS at the parent (`dnssec-dsfromkey`); `rndc dnssec -status <zone>` shows signing state.
- Split-horizon: `view "internal" { match-clients { 10.0.0.0/8; }; zone …; }; view "external" { … }`
  (the `view` statement in the ARM; a client matches a view by source and destination address or TSIG key).
- Distro packaging differs (chroot variants, SELinux labels and booleans): follow your distro's BIND documentation.
- Firewall 53/udp **and** 53/tcp (TCP for transfers and large answers).

## 3. Operations
`rndc dumpdb -all` (caches and zones to the `dump-file`), `rndc querylog` (toggles query logging —
noisy), `rndc flush` on a recursive BIND. Watch `dig +norecurse` vs `+recurse` behaviour
to confirm `recursion no` works from the outside (open resolvers get abused for amplification).

## Verify
- [ ] `named-checkconf -z` clean; `dig @primary` and `dig @secondary` return the same SOA serial.
- [ ] From an external IP, `dig @ns1 google.com` returns REFUSED (no open recursion).
- [ ] Unbound: `dig @resolver example.com +dnssec` shows `ad`; a deliberately mis-signed test name returns SERVFAIL.

## Checked
Checked 2026-10-27 against the BIND 9 Administrator Reference and rndc/named-checkconf manuals (github.com/isc-projects/bind9 main) and the unbound.conf and unbound-control sources (github.com/NLnetLabs/unbound).
- `named-checkconf -z` test-loads only zones of type `primary` (earlier text said every zone); `rndc freeze`, `retransfer`, `dumpdb -all` and `dnssec -status` exist.
- `dnssec-policy` built-ins are `default`, `insecure` and `none`; `inline-signing` is on by default for DNSSEC zones.
- Unbound: `auto-trust-anchor-file` defaults to empty, so validation needs it set; `forward-addr` takes `IP@port#auth-name`; `forward-tls-upstream` needs a `tls-cert-bundle`; `domain-insecure`, `private-address`, `hide-identity`, `hide-version`, `cache-min-ttl`, `unbound-control flush_zone`/`stats_noreset` exist.
- `view` blocks use `match-clients`.
- Removed unconfirmed claims: version gates (`master` before 9.16, DNSSEC 9.16+), distro package and SELinux details, the 1232-byte figure, third-party DNSSEC test domain, view membership rule.
Method: documentation only; no commands were run.
