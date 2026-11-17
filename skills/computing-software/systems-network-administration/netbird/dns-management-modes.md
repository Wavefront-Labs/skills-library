---
id: computing-software.systems-network-administration.netbird.dns-management-modes
name: dns-management-modes
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, dns-settings, unmanaged-dns, disable-dns, domain-controllers]
level: practitioner
status: docs-checked
description: "Switch NetBird peers between managed and unmanaged DNS per group or per client with --disable-dns, including the API and what unmanaged mode ignores."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/dns/dns-settings.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Modes per peer:
- Managed (default): NetBird configures system DNS and routes queries through its local resolver.
- Unmanaged: NetBird leaves system DNS alone. Nameservers and Custom Zone records are ignored, including zones assigned to the peer's groups. Peers still reach each other over NetBird; only name resolution changes.

Use unmanaged for conflicting VPN or DNS requirements, corporate DNS policy, or DNS troubleshooting. If you run NetBird alongside Active Directory, the docs advise disabling DNS management for domain controller groups.

Group setting: DNS > DNS Settings > select or create groups > Save Changes. Takes about 10 to 30 seconds. Remove the group and save to re-enable.

Client override: `netbird up --disable-dns` or `netbird up --disable-dns=false`. It overrides server-side settings and persists across reconnects until explicitly changed.

API: `GET` and `PUT` on `https://api.netbird.io/api/dns/settings` with an `Authorization: Token` header; the PUT body has a `disabled_management_groups` array of group IDs.

## Checked

2026-11-04: read the DNS Settings page in full. Confirmed the two modes, what unmanaged mode ignores, the 10-30 second propagation, the --disable-dns override and persistence, and the API endpoint and body field. Nothing removed.

Method: documentation only; no commands were run.
