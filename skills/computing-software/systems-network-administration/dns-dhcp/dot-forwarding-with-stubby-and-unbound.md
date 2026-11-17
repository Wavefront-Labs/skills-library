---
id: computing-software.systems-network-administration.dns-dhcp.dot-forwarding-with-stubby-and-unbound
name: dot-forwarding-with-stubby-and-unbound
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, stubby, dot-forwarder, dns-over-tls, unbound, encrypted-dns]
level: practitioner
status: docs-checked
description: "Forward local DNS over TLS to upstream resolvers with stubby or Unbound forward-tls-upstream, including certificate authentication and fallback behaviour."
sources:
  - https://github.com/getdnsapi/stubby
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://www.freedesktop.org/software/systemd/man/latest/resolved.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DoT forwarding with stubby/unbound

Encrypt the hop from a host or site to a public/central resolver (RFC 7858, TCP 853).

## stubby (getdns)
`/etc/stubby/stubby.yml`:
```yaml
resolution_type: GETDNS_RESOLUTION_STUB
dns_transport_list: [GETDNS_TRANSPORT_TLS]
tls_authentication: GETDNS_AUTHENTICATION_REQUIRED
tls_query_padding_blocksize: 128
round_robin_upstreams: 1
listen_addresses: [127.0.0.1, 0::1]
upstream_recursive_servers:
  - address_data: 9.9.9.9
    tls_auth_name: "dns.quad9.net"
  - address_data: 149.112.112.112
    tls_auth_name: "dns.quad9.net"
```
Point the system resolver at 127.0.0.1. In Strict mode (`GETDNS_AUTHENTICATION_REQUIRED`) every upstream needs a `tls_auth_name` or a `tls_pubkey_pinset`; Opportunistic mode needs only an address. The provider addresses above are the commented example entries in stubby's `stubby.yml.example`.

## Unbound
```
server:
    tls-cert-bundle: /etc/ssl/certs/ca-certificates.crt
forward-zone:
    name: "."
    forward-tls-upstream: yes
    forward-addr: 9.9.9.9@853#dns.quad9.net
    forward-addr: 149.112.112.112@853#dns.quad9.net
```
The `@port` comes first, then `#name`: the name is checked against the server's certificate (using `tls-cert-bundle`). If you leave out the `#` and name, any name is accepted.

## systemd-resolved
`DNSOverTLS=yes` and `DNS=9.9.9.9#dns.quad9.net` in `resolved.conf` (the `address#server_name` form validates the certificate and sets SNI). `yes` makes all lookups fail if the server lacks DoT support; `opportunistic` falls back to plain DNS if the server does not support TLS, which makes it vulnerable to downgrade attacks.

## Gotchas
- Strict mode fails closed if 853 is blocked (captive portals, some corporate networks).
- Forwarding everything bypasses internal zones: add forward/stub zones for internal domains to
  internal servers.
- Upstream sees all queries; choose the provider with that in mind.

## Verify
- [ ] A packet capture shows no outbound plain DNS to the upstream and TLS sessions on port 853.

## Checked

Date: 2026-10-26. NLnetLabs/unbound doc sources (unbound.conf.rst, unbound-control.rst, unbound-anchor.rst, repository pushed 2026-10-21), read on 2026-10-26. stubby.yml.example (getdnsapi/stubby, last commit 2025-07-15) and the systemd resolved.conf man page source, read 2026-10-26. Confirmed: stubby option names (resolution_type, dns_transport_list, tls_authentication, tls_query_padding_blocksize, round_robin_upstreams, listen_addresses, upstream_recursive_servers, address_data, tls_auth_name), Quad9 example entries, Strict versus Opportunistic requirements, Unbound forward-addr @port#name and forward-tls-upstream, tls-cert-bundle, resolved.conf DNSOverTLS yes/opportunistic semantics and address#name format. Removed the unconfirmed Cloudflare entry and dnsmasq pairing.

Method: documentation only; no commands were run.
