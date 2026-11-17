---
id: computing-software.networking-hardware-and-wireless.unbound.hardening-options
name: hardening-options
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, harden-glue, harden-below-nxdomain, harden-referral-path, harden-large-queries, security]
level: advanced
status: docs-checked
description: "Understand each harden-* option in Unbound, its default and its cost: glue, short buffers, large queries, stripped DNSSEC, below-nxdomain, referral path and more."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hardening options
The manual says `harden-cname-follow` is on by default to protect cache integrity. Defaults on:
- `harden-short-bufsize`: very small EDNS buffer sizes are ignored and replaced by the normal 512 byte UDP size (per RFC 6891).
- `harden-cname-follow`: follow CNAME and DNAME redirections instead of trusting them unchecked; disable only on localhost or encrypted links.
- `harden-glue`: trust glue only within the server's authority.
- `harden-dnssec-stripped`: require DNSSEC data for trust-anchored zones, else bogus; disabling may allow downgrade.
- `harden-below-nxdomain`: return NXDOMAIN below a secure NXDOMAIN (RFC 8020); NSEC3 opt-out is insufficient.

Defaults off:
- `harden-large-queries`: ignore very large queries (cutoff 512 bytes; off because they are legal and may be needed for TSIG or large EDNS payloads).
- `harden-unverified-glue`: trust only in-zone glue and try to resolve out-of-zone glue, falling back to the original if that fails.
- `harden-referral-path`: extra queries to validate the referral path; experimental, adds load on authoritative servers.
- `harden-algo-downgrade`: troubleshooting only; violates RFC 6840.
- `harden-unknown-additional`: harden against unknown records in the authority and additional sections; when off they are passed to the client, when on it could hamper future protocol additions.

Several can be changed at runtime with `unbound-control set_option` (short-bufsize, large-queries, glue, dnssec-stripped, below-nxdomain, referral-path).

## Checked

2026-11-08. Read the harden-* entries and use-caps-for-id context of unbound.conf (not the whole page). Added harden-cname-follow, the 512 byte cutoffs and corrected the harden-unknown-additional and harden-unverified-glue descriptions.

Method: documentation only; no commands were run.
