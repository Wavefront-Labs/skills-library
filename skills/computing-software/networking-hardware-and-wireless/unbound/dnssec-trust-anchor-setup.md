---
id: computing-software.networking-hardware-and-wireless.unbound.dnssec-trust-anchor-setup
name: dnssec-trust-anchor-setup
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, dnssec, trust-anchor, auto-trust-anchor-file, root-key, rfc5011]
level: practitioner
status: docs-checked
description: "Turn on DNSSEC validation in Unbound by creating and configuring a root trust anchor, and choose between the trust-anchor option types."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/getting-started/configuration.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnssec trust anchor setup
Run `unbound-anchor` to create the initial trust anchor. Unbound must be able to read and write the file to keep it updated. Some packages create it already (the guide cites `/var/lib/unbound/root.key` on Ubuntu 22.04); `unbound-anchor -vvv` shows the default location. If it fails on permissions, run `sudo -u unbound unbound-anchor`.

```
server:
    auto-trust-anchor-file: "<anchor-dir>/root.key"
```

Validation only happens once a trust anchor is configured; the default `module-config` just loads the validator module. The location depends on the install: the guide names `/usr/local/etc/unbound/` as the usual default and `/var/lib/unbound/` for some distribution packages.

Option types:
- `auto-trust-anchor-file`: anchor for one zone, tracked with RFC 5011 probes run several times a month, so the machine must be online often. The Unbound user needs write permission on the file and its directory (a temporary file is created), and it must be inside any chroot. The initial file can use the `trust-anchor-file` format.
- `trust-anchor-file`: static DS or DNSKEY entries in zone-file format.
- `trust-anchor`: one DS or DNSKEY record on one line in quotes, repeatable, in addition to the file; TTL ignored, class defaults to IN.
- `trusted-keys-file`: BIND-style `trusted-keys { ... };` clauses; wildcards expand at start and reload, and a wildcard matching no files is not an error.

`trust-anchor-signaling` (default yes) sends an RFC 8145 key-tag query after priming; `root-key-sentinel` defaults yes. `hide-trustanchor: yes` refuses `trustanchor.unbound` queries.

The default `module-config` is `"validator iterator"`; `"iterator"` alone gives a non-validating server.

## Checked

2026-11-08. Read the trust-anchor options and signaling options in the unbound.conf manual and the Trust Anchor part of the getting-started guide. Expanded the auto-trust-anchor-file permission and probing details, added the trusted-keys-file wildcard rule, and replaced the hard-coded key path in the example with a placeholder.

Method: documentation only; no commands were run.
