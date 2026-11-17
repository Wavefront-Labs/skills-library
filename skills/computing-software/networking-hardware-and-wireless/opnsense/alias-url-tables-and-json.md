---
id: computing-software.networking-hardware-and-wireless.opnsense.alias-url-tables-and-json
name: alias-url-tables-and-json
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [aliases, url-table, json-alias, jq]
level: practitioner
status: docs-checked
description: "Build OPNsense aliases from remote IP lists: URL, URL Table and JSON URL Table types, refresh frequency, accepted line format and jq path expressions."
sources: ["https://docs.opnsense.org/manual/aliases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# URL table and JSON aliases

Three alias types pull IP addresses from a remote server. URL (IPs) fetches the list once. URL Tables (IPs) fetches it again on a Refresh frequency you set. URL Table in JSON format works the same way but parses a JSON document.

Plain text lists must contain one IPv4 or IPv6 address per line. Lines beginning with whitespace, a comma, semicolon, pipe or hash are ignored, so comments and blank formatting are safe.

For JSON sources, fill in a Path expression that selects the values from the document. A flat file where each row has a field named cidr (the Spamhaus DROP v4 JSON is the documented example) needs only a single path reference. The parser also supports jq, so more selective filters are possible. Examples from the docs:

- https://ip-ranges.amazonaws.com/ip-ranges.json with .prefixes[] | select(.region=="us-east-1") | select(.service=="EC2") | .ip_prefix gives EC2 addresses in us-east-1.
- https://api.github.com/meta with .web + .api + .git | .[] gives GitHub web, API and git ranges.
- The Microsoft endpoints.office.com worldwide feed with .[] | select(.serviceArea=="Exchange") | select(".ips")| .ips | .[]? gives Exchange networks.

Use the jq playground at play.jqlang.org to refine an expression before pasting it into the alias. After saving, check Firewall > Diagnostics > Aliases to confirm the table loaded and review the Loaded# column on the alias overview; if the alias overflows, Firewall Maximum Table Entries under Firewall > Settings > Advanced raises the limit.

## Checked

2026-11-03. Read the Aliases manual page (aliases.html) on docs.opnsense.org and confirmed the claims above against them. Removed: the unsupported claim that Firewall Maximum Table Entries governs URL table limits (the page names it for GeoIP/table overflow).
Method: documentation only; no commands were run.
