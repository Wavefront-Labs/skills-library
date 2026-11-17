---
id: computing-software.systems-network-administration.dns-dhcp.unbound-resolver-configuration
name: unbound-resolver-configuration
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, recursive-resolver, dns-resolver, unbound, unbound-conf, access-control, qname-minimization, prefetch, cache-flush, unbound-control, forward-zone, stub-zone, local-zone, dnssec-validation, auto-trust-anchor-file]
level: practitioner
status: verified
description: "Configure Unbound as a validating resolver: access-control, QNAME minimisation, prefetch and cache sizing, forward/stub zones, local data, unbound-control cache ops."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
  - https://datatracker.ietf.org/doc/html/rfc9156
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Unbound resolver configuration

Unbound (NLnet Labs) is a lean validating recursive resolver: a good choice for site resolvers,
pfSense/OPNsense, and Pi-hole upstreams.

## Baseline `/etc/unbound/unbound.conf`
```
server:
    interface: 0.0.0.0
    interface: ::0
    access-control: 0.0.0.0/0 refuse
    access-control: 10.0.0.0/8 allow
    access-control: 127.0.0.0/8 allow
    access-control: 2001:db8::/32 allow
    auto-trust-anchor-file: "/var/lib/unbound/root.key"   # DNSSEC validation (RFC 5011 updates)
    qname-minimisation: yes            # default yes: sends only the needed labels upstream (RFC 9156)
    harden-glue: yes
    harden-dnssec-stripped: yes
    use-caps-for-id: no
    prefetch: yes                      # default no: refresh popular records before expiry
    serve-expired: yes                 # default no: serve expired answers if resolution fails or is slow
    msg-cache-size: 128m               # default 4m
    rrset-cache-size: 256m             # default 4m
    num-threads: 4                     # default 1; msg/rrset-cache-slabs must be powers of 2, close to the CPU count
    hide-identity: yes
    hide-version: yes
    private-address: 10.0.0.0/8        # removes such addresses from answers for public names (DNS rebinding protection)
    private-domain: "corp.example"     # ...except for this domain
    local-zone: "lab.example." static
    local-data: "nas.lab.example. 300 IN A 10.9.0.20"

forward-zone:
    name: "corp.example."
    forward-addr: 10.1.1.10
    forward-addr: 10.1.1.11
stub-zone:                              # to an authoritative server (non-recursive queries)
    name: "partner.example."
    stub-addr: 192.0.2.53
remote-control:
    control-enable: yes
    control-interface: /run/unbound.ctl
```
`unbound-checkconf` before restart; `unbound-anchor` creates or updates the root key file.

## Operations
```
unbound-control status
unbound-control stats_noreset               # statistics without resetting counters
unbound-control lookup example.com          # shows the servers used for the name
unbound-control flush www.example.com       # one name
unbound-control flush_zone example.com      # everything at and below a name
unbound-control flush_bogus                 # remove entries that failed DNSSEC validation
unbound-control dump_cache > cache.txt
```

## Gotchas
- Forward zones to unsigned internal zones under a signed public parent can fail validation (an external DS record can make the internal domain bogus): add `domain-insecure: "corp.example"` (a `stub-zone` or forward to any other unsigned name needs it too: such a query returned SERVFAIL until `domain-insecure` was set).
- A `forward-zone` named `"."` sends everything to the upstream forwarders (add `forward-tls-upstream: yes` for DoT, and `forward-addr: <ip>@853#<auth-name>` to authenticate).
- Clock skew breaks DNSSEC validation (signature validity windows).
- `auto-trust-anchor-file` must be writable by the Unbound user and its directory. On Debian 13 the file does not exist until `unbound-anchor` (package `unbound-anchor`) has run, and the packaged `conf.d/root-auto-trust-anchor-file.conf` already sets it: repeating it makes `unbound-checkconf` fail with `trust anchor for '.' presented twice`.

## Verify
- [ ] A name with a deliberately broken DNSSEC chain returns SERVFAIL and a signed name shows the `ad` flag.
- [ ] Queries from non-allowed networks are refused.
- [ ] Cache statistics look healthy after warm-up.

## Checked

Date: 2026-10-26. NLnetLabs/unbound doc sources (unbound.conf.rst, unbound-control.rst, unbound-anchor.rst, repository pushed 2026-10-21), read on 2026-10-26. Confirmed: defaults for qname-minimisation (yes), use-caps-for-id (no), prefetch (no), serve-expired (no), msg-cache-size and rrset-cache-size (4m), num-threads (1), slabs power-of-2 rule, interface default, private-address and private-domain semantics, hide-identity/hide-version, auto-trust-anchor-file write permission requirement, forward-addr @port#name syntax, forward-tls-upstream, stub-addr, control-enable/control-interface, domain-insecure rationale, unbound-control stats_noreset/lookup/flush/flush_zone/flush_bogus/dump_cache. Removed the unconfirmed thread-equals-cores rule, rrset 2x rule and statistic-name pipeline.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (Unbound 1.26.2): unbound-checkconf -o for the documented defaults (qname-minimisation yes, use-caps-for-id no, prefetch no, serve-expired no, msg-cache-size and rrset-cache-size 4194304, num-threads 1, harden-glue and harden-dnssec-stripped yes, hide-identity no), the power-of-2 slabs error and unknown-keyword errors, the baseline config running with a forward-zone, stub-zone, local-zone/local-data and remote-control; most-specific access-control refuse winning over a broader allow (REFUSED), hide-identity/hide-version (version.bind and id.server REFUSED), unbound-control status, lookup (shows the forwarder), stats_noreset, dump_cache, flush, flush_zone, flush_bogus; an unsigned forwarded name failing validation unless domain-insecure was set. Not run: prefetch, serve-expired, private-address rebinding protection, DoT forwarding, unbound-anchor against the network.
