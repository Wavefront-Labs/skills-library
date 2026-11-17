---
id: computing-software.networking-hardware-and-wireless.unbound.tls-upstream-and-padding
name: tls-upstream-and-padding
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, tls-upstream, tls-cert-bundle, padding, sni, forward-tls-upstream]
level: advanced
status: docs-checked
description: "Send Unbound upstream queries over TLS with certificate authentication, and control SNI and response and query padding."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tls upstream and padding
- `tls-upstream: yes` (alias `ssl-upstream`, default no) uses TLS for all forward and stub queries (plain DNS in TCP wireformat; the other server must support it). Configure a CA bundle or system certificates.
- `tls-cert-bundle` (default `""`) is the CA file used to authenticate outbound peers, read at startup before chroot.
- `tls-system-cert` / `tls-win-cert: yes` adds system certificates (Windows uses its cert store).
- Per zone: `forward-tls-upstream` or `stub-tls-upstream`, with addresses written `ip@port#auth-name`. Without `#auth-name`, any certificate name is accepted but it must still chain to a CA in the bundle; high verbosity logs the certificate.
- `tls-use-sni` (default yes) sends SNI; restart required.
- `pad-responses` (yes) pads TLS responses to queries carrying an EDNS padding option, block size `pad-responses-block-size` (468).
- `pad-queries` (yes) pads queries sent over TLS upstreams, block size `pad-queries-block-size` (128).

## Checked

2026-11-08. Read tls-upstream, ssl-upstream, tls-cert-bundle, tls-win-cert, tls-system-cert, tls-use-sni and the pad-* options in the unbound.conf manual. Defaults confirmed; added the transport detail for tls-upstream.

Method: documentation only; no commands were run.
