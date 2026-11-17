---
id: computing-software.networking-hardware-and-wireless.opnsense.alias-dynamic-ipv6-external-openvpn
name: alias-dynamic-ipv6-external-openvpn
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [aliases, dynamic-ipv6-host, external-alias, openvpn-group, pfctl]
level: advanced
status: docs-checked
description: "Dynamic IPv6 host, BGP ASN, external and OpenVPN group aliases in OPNsense, including pfctl table edits and the alias_util API call."
sources: ["https://docs.opnsense.org/manual/aliases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dynamic IPv6, BGP ASN, external and OpenVPN group aliases

Dynamic IPv6 Host: use this when the LAN prefix is delegated and can change. Enter only the lower 64 bits as a suffix, always starting with "::" (for example ::1000:1000:0000:1); no prefix length is needed because /128 is assumed. Pick the interface that supplies the upper 64 bits. The alias always splits on the /64 boundary regardless of delegation size. With a /48 delegation and two LANs you need one alias per LAN interface, because each interface contributes a different upper half. Several suffixes can be added to one alias for multiple servers on a segment.

BGP ASN: maps autonomous system numbers to the networks they announce, e.g. 13335 for Cloudflare or 8075 for Microsoft.

External (advanced): OPNsense only keeps the placeholder; something else fills it. Firewall > Diagnostics > Aliases lets you view, add and remove entries immediately. Because OPNsense does not touch the content, scripts may use pfctl directly, for example pfctl -t MyAlias -T add 10.0.0.3. With the REST API you can add entries to Host, Network and External aliases using POST /api/firewall/alias_util/add/MyAlias with a JSON body like {"address":"10.0.0.2"} and an API key and secret as basic auth. For external aliases such additions are not persistent across reboots, which suits large, frequently changing lists.

OpenVPN group: lets rules target logged-in OpenVPN users by group from System > Access > Groups. The alias follows the current connections (VPN > OpenVPN > Connection Status): if user fred in group remote_users gets 10.10.10.2, that address appears in the alias. The certificate common name must equal the username, which holds by default when the certificate is created in the user manager. LDAP group sync avoids double administration.

## Checked

2026-11-03. Read the Aliases manual page (aliases.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
