---
id: computing-software.systems-network-administration.dns-dhcp.bind-options-listen-on-and-named-checkconf
name: bind-options-listen-on-and-named-checkconf
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [bind, named-conf, options-block, listen-on, named-checkconf, directory, recursion]
level: practitioner
status: verified
description: "Structure named.conf for BIND 9: options block (directory, listen-on, recursion, version), includes, and validating every change with named-checkconf before reload."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/manpages.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# BIND options, listen-on and named-checkconf

## A clean authoritative-only options block
```
options {
    directory "/var/cache/bind";          // relative zone file paths resolve here
    listen-on port 53 { 192.0.2.53; 127.0.0.1; };
    listen-on-v6 port 53 { 2001:db8::53; ::1; };
    recursion no;                         // authoritative only
    allow-query { any; };
    allow-transfer { none; };             // open per zone with TSIG
    notify explicit;
    version "not disclosed";
    hostname none;
    server-id none;
    minimal-responses yes;
    dnssec-validation no;                 // auth-only; resolvers validate
    querylog no;
};
include "/etc/bind/keys.conf";
include "/etc/bind/zones.conf";
```
For a resolver: `recursion yes; allow-recursion { internal-nets; }; dnssec-validation auto;`. Never
mix authoritative-for-the-internet and open recursive on the same listener.

## listen-on details
- With no `listen-on`, named listens on port 53 of all IPv4 interfaces; with no `listen-on-v6`, on port 53 of all IPv6 interfaces.
- With an explicit list, named listens only on matching interfaces. It rescans interfaces every `interface-interval` (default 60 minutes, `0` = only at config load unless `automatic-interface-scan` applies).
- DoT/DoH listeners: `listen-on port 853 tls mytls { ... };`.

## Validate before every reload
```
named-checkconf                         # syntax of /etc/bind/named.conf (path varies by distro)
named-checkconf -z                      # also test-load all zones of type primary
named-checkconf -p | less               # print named.conf and includes in canonical form
named-checkconf -t /var/named/chroot    # chrooted installs
rndc reconfig                           # reread config and load new zones
rndc reload                             # also reload changed zones
```
named-checkconf returns non-zero on errors; wire it into CI and into your deployment script so a
typo never reaches the server.

## Gotchas
- Config file locations differ by distribution; `named-checkconf` defaults to the compiled-in `named.conf` path when no file is given.
- File permissions/SELinux: zone files must be readable by `named`; dynamic zones and journals need write access to their directory.
- `rndc reconfig` does not reload existing zones; a forgotten `rndc reload zone` leaves old data.

## Verify
- [ ] `named-checkconf -z` returns 0 and the server listens only on the intended addresses.

## Checked

Date: 2026-10-26. BIND 9 ARM sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus the bind-9.20 branch grammar), read on 2026-10-26. Confirmed: listen-on / listen-on-v6 defaults and grammar (port, tls, http, proxy), interface-interval default 60 minutes and max 28 days, named-checkconf options -p, -t, -z (primary zones only), exit status 1 on errors. Removed unconfirmed distro path claims.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (BIND 9.20.30): the options block parsed by named-checkconf, -z loading all primary zones, -p printing canonical form, a bad option giving exit 1, no-argument default path; named started with the block: version.bind answered "not disclosed", AXFR REFUSED with allow-transfer none, recursion no answered REFUSED for an outside name. Not run: -t chroot with a populated root, rndc reconfig versus reload, DoT/DoH listeners, interface-interval.
