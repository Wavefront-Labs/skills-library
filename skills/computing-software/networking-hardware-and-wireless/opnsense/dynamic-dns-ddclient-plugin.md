---
id: computing-software.networking-hardware-and-wireless.opnsense.dynamic-dns-ddclient-plugin
name: dynamic-dns-ddclient-plugin
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [dynamic-dns, os-ddclient, cloudflare, ddclient]
level: practitioner
status: docs-checked
description: "Set up the os-ddclient plugin on OPNsense: general settings, backend choice, account fields, A and AAAA records, Cloudflare, Netcup and Mythic Beasts."
sources: ["https://docs.opnsense.org/manual/dynamic_dns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dynamic DNS with os-ddclient

Install the os-ddclient plugin from System > Firmware > Plugins, then configure under Services > Dynamic DNS > Settings. Register with a supported DNS provider first.

General tab: Enable, Verbose (detailed logs), Allow IPv6, Interval (seconds between IP change checks) and Backend, either ddclient or native. Because ddclient development is winding down, a Python-based native backend is offered; it also supports custom HTTP requests, and the docs advise trying it if your provider is supported.

Accounts tab (each uses an HTTP(S) API call): Enabled, Description, Service, resourceId (only Azure), Username (empty for token auth), Password (password, API key or token), Zone (typically the second-level domain, e.g. example.com), Hostname(s) comma-separated FQDNs, Check ip method, Interface to monitor (where the IP check connects from, or the interface to read the address from when method is Interface), Dynamic ipv6 host (overrides the interface identifier, e.g. ::aabb:33ff:fe44:ccdd), Check ip timeout, Force SSL.

To update both A and AAAA records for one name, create two accounts, one with an IPv4 check method and one with an IPv6 method, and enable Allow IPv6 on the General tab.

Cloudflare: Zone is the zone name, not its ID. Global key auth uses the account email as Username and the Global API Key as Password. Preferred is an API token with Zone > DNS > Edit limited to the specific zone: Username is the word token, Password the token. Netcup: Username is the customer number, Password is APIPassword|APIKey joined with a pipe. Mythic Beasts: Username is the Key ID, Password the secret.

## Checked

2026-11-03. Read the Dynamic DNS manual page (dynamic_dns.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
