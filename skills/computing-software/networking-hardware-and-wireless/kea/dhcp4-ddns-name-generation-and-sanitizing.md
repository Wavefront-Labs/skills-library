---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-ddns-name-generation-and-sanitizing
name: dhcp4-ddns-name-generation-and-sanitizing
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, ddns, ddns-replace-client-name, ddns-qualifying-suffix, hostname-char-set]
level: practitioner
status: docs-checked
description: "Control host names in kea-dhcp4 DDNS: ddns-replace-client-name modes, generated prefix, qualifying suffix, and hostname-char-set sanitizing."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DDNS name generation and sanitizing in kea-dhcp4
`ddns-replace-client-name` modes:
- `never` (default): use the client's name; generate none if absent.
- `always`: replace the client's name; generate one if absent.
- `when-present`: replace the client's name; generate none if absent.
- `when-not-present`: keep the client's name; generate one if absent.

Boolean values are no longer accepted; true maps to `when-present` and false to `never`.

Name format:
- Partial names become `[candidate-name].[ddns-qualifying-suffix].`, e.g. `some-computer.example.com.`
- Generated names are `[ddns-generated-prefix]-[address-text].[ddns-qualifying-suffix].`; `ddns-generated-prefix` defaults to "myhost", so 172.16.1.10 gives `myhost-172-16-1-10.example.com.`
- The docs strongly recommend setting `ddns-qualifying-suffix` when DDNS is on; there is no meaningful default.

Sanitizing, applied only to the client-supplied part and before the suffix:
- `hostname-char-set`: POSIX extended regex of invalid characters, default `[^A-Za-z0-9.-]`; do not set it empty, since that permits non-printable characters.
- `hostname-char-replacement`: default empty, which omits invalid characters.

With replacement "x", `myhost-$[123.org` becomes `myhost-xx123.org`.

The returned Host Name option never gets a trailing dot added; a returned FQDN option always ends with a dot.

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (DHCPv4 chapter DDNS name generation and sanitizing sections). Removed: nothing.
Method: documentation only; no commands were run.
