---
id: computing-software.digital-privacy-hygiene.vpn-tools.systemd-resolved-dns-over-tls
name: systemd-resolved-dns-over-tls
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, systemd-resolved, encrypted-dns, linux-desktop-security]
level: practitioner
status: docs-checked
description: "Configure systemd-resolved on Linux for DNS over TLS with strict mode, stop NetworkManager overriding it, and verify with resolvectl."
sources:
  - "https://www.freedesktop.org/software/systemd/man/latest/resolved.conf.html"
  - "https://www.privacyguides.org/en/advanced/dns-overview/"
  - "https://docs.quad9.net/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# systemd-resolved DNS over TLS

**Goal:** a Linux desktop sends DNS encrypted to a chosen resolver, and fails rather than falling back to plaintext.

## Configure
Local overrides belong in a drop-in such as `/etc/systemd/resolved.conf.d/10-dot.conf` (the man page recommends
drop-ins over editing the main file, and a two-digit prefix; files in `/etc/` are for the local administrator):
```
[Resolve]
DNS=<resolver-ip>#<resolver-hostname>
DNSOverTLS=yes
Domains=~.
```
- `DNS=` takes space-separated IPv4/IPv6 addresses; the optional `#name` suffix is the Server Name Indication, used to
  validate the certificate (otherwise the certificate is checked against the server IP). Take the address and hostname
  from your resolver's documentation, for example Quad9's docs list DoT among its supported protocols (secure service
  9.9.9.9).
- `DNSOverTLS=yes` encrypts all connections to the server; it needs a server that supports DoT with a valid
  certificate, and if the server does not support it, all DNS requests fail. `opportunistic` falls back to unencrypted
  and does not authenticate the server, so it is open to downgrade and man-in-the-middle attacks. Default is `no`.
- `Domains=~.` (route-only root domain) prefers these DNS servers for all domains.
- `FallbackDNS=` is used only when no other DNS server information is known; if the option is not given, a
  compiled-in list is used. Check how your distribution sets it.
- Restart the service afterwards: `sudo systemctl restart systemd-resolved`.

## Per-link servers
DNS requests also go to suitable per-link DNS servers learned from systemd-networkd or set at runtime by other
applications. For the system DNS servers only the global `DNSOverTLS=` applies; for per-link servers the per-link
setting applies unless it is unset, then the global one. So a DHCP-supplied server on a link can still be used: review
the per-link settings in your network manager and turn off automatic DNS for the connection if you need only your
resolver.

## Stub listener
`DNSStubListener=` defaults to `yes`: the stub on 127.0.0.53 offers the full local resolver, and the stub on 127.0.0.54
runs in proxy mode (it translates to DNS-over-TLS if needed). Applications that use the system resolver go through
these.

## Verify
Use your resolver provider's "am I using it" check page or documentation, and inspect resolved's status with its own
tooling (see systemd-resolved.service(8)). Test from the same machine and on every network you use.

## Gotchas
- Strict DoT breaks captive portals; use the portal on another device or switch temporarily.
- Port 853, DoT's dedicated port, can be blocked by restrictive firewalls (Privacy Guides notes this).
- A VPN client may set its own DNS on its link; that is usually what you want while connected.
- Privacy Guides notes the industry has been moving from DoT to DoH; resolved supports DoT.

## Checked
Confirmed 2026-11-08 against resolved.conf(5) (DNS, DNSOverTLS, Domains, FallbackDNS, DNSStubListener, drop-in
guidance, per-link behaviour), Privacy Guides' DNS overview (port 853, DoT vs DoH trend) and the Quad9 docs home (DoT
support, 9.9.9.9). Removed: the Quad9 secondary and IPv6 addresses and hostname, the `nmcli` commands, the
`/etc/resolv.conf` symlink check, the `resolvectl status` and `proto.on.quad9.net` verification, and the empty
`FallbackDNS=` line, none of which the cited pages state.
Method: docs-only read of cited pages, 2026-11-08
