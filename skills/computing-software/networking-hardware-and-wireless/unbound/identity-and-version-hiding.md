---
id: computing-software.networking-hardware-and-wireless.unbound.identity-and-version-hiding
name: identity-and-version-hiding
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, hide-identity, hide-version, nsid, chaos-queries, identity]
level: intro
status: docs-checked
description: "Control what Unbound reveals about itself: id.server, hostname.bind, version.server, trustanchor.unbound and NSID."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# identity and version hiding
- `hide-identity: yes` (default no) refuses `id.server` and `hostname.bind` queries; `identity` sets the reported string (empty means the hostname).
- `hide-version: yes` (default no) refuses `version.server` and `version.bind`; `version` sets the reported string (empty means the package version).
- `hide-trustanchor: yes` (default no) refuses `trustanchor.unbound` queries.
- `nsid` adds the given NSID to the EDNS section of answers when the query carries an NSID request; the value is hex characters or an `ascii_` prefix followed by an ASCII string. Disabled by default.
- `log-identity` overrides the identity string in logs.

`hide-identity`, `hide-version`, `identity` and `version` can be set at runtime with `unbound-control set_option`.

## Checked

2026-11-08. Read the identity, version, nsid and hide-trustanchor entries of unbound.conf (source file read in the relevant sections, not end to end) and the unbound-control set_option list. Added the NSID value format and the unbound-control source.

Method: documentation only; no commands were run.
