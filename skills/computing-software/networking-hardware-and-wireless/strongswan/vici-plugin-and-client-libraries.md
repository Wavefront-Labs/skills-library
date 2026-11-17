---
id: computing-software.networking-hardware-and-wireless.strongswan.vici-plugin-and-client-libraries
name: vici-plugin-and-client-libraries
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, vici, automation, davici, python-wheel]
level: advanced
status: docs-checked
description: "Automate strongSwan charon with the VICI plugin: socket option, security of the transport, and available client libraries (libvici, davici, govici, Python, Ruby, Perl)."
sources:
  - https://docs.strongswan.org/docs/latest/plugins/vici.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vici plugin and client libraries
VICI (Versatile IKE Control Interface) lets external applications configure, control and monitor charon. It replaces the starter, ipsec.conf and stroke interfaces, which were never designed for automation. swanctl is its main user and drives its development. The plugin is enabled by default; `--disable-vici` removes it.

**Configuration.** One option under `charon.plugins.vici`: `socket`, the URI where the plugin listens, default `unix://${piddir}/charon.vici` (on Windows `tcp://127.0.0.1:4502`).

**Security.** The protocol has no security or authentication of its own, so run it over a UNIX socket with appropriate permissions. High and low level protocol details are in the VICI README.

**Client libraries** (any language can speak the protocol):
- libvici: low-level C API, header `libvici.h` is MIT licensed, but the library depends on libstrongswan (GPLv2). Mostly for internal use.
- davici: C client that does not use libstrongswan, asynchronous, LGPLv2+. Usually the better choice when embedding a client.
- govici: Go implementation on GitHub.
- Ruby gem, Python wheel (PyPI) and Perl CPAN module wrap the protocol for scripting.

The VICI README, linked from the page, documents the operations with simple examples in C, Python, Perl and Ruby. Related: the swanctl tool, and the updown plugin which fires a vici `child-updown` event.

## Checked
2026-11-04. Confirmed against the strongSwan vici plugin page (purpose, --disable-vici, socket option and default, Windows tcp default, security advice, libvici, davici, govici, Ruby, Python and Perl libraries) and the updown plugin page (child-updown event). Corrected where the operation examples are documented.

Method: documentation only; no commands were run.
