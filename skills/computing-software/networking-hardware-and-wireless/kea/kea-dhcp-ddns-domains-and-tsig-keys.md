---
id: computing-software.networking-hardware-and-wireless.kea.kea-dhcp-ddns-domains-and-tsig-keys
name: kea-dhcp-ddns-domains-and-tsig-keys
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp-ddns, forward-ddns, reverse-ddns, tsig, ddns-domains]
level: practitioner
status: docs-checked
description: "Define forward and reverse DDNS domains, their DNS servers and TSIG keys in kea-dhcp-ddns, including key-name, secret and secret-file."
sources:
  - https://kea.readthedocs.io/en/latest/arm/ddns.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D2 DDNS domains and TSIG keys
Both `forward-ddns` and `reverse-ddns` hold a `ddns-domains` list, empty by default (which makes D2 ignore that half of requests). Each zone needs its own domain, even if servers are shared.

Domain fields:
- `name`: zone FQDN, unique in the catalog, compared against the request.
- `key-name`: name of a TSIG key; blank (default) means no TSIG.
- `dns-servers`: tried first to last until one succeeds. A domain without servers fails any request it matches.

Server fields: `ip-address` (IPv4 or IPv6; `hostname` is not yet implemented), `port` (default 53).

```json
"forward-ddns": { "ddns-domains": [ { "name": "other.example.com.",
  "key-name": "", "dns-servers": [
    { "ip-address": "172.88.99.10", "port": 53 } ] } ] }
```

TSIG keys go in `tsig-keys`, each with `name` (unique, preferably matching the DNS server's key name), `algorithm` (HMAC-MD5, SHA1, SHA224, SHA256, SHA384, SHA512, case-insensitive; must match the server) and `secret` (case-sensitive base64) or, since Kea 2.5.8, `secret-file` naming a file that holds the base64 secret.

```json
"tsig-keys": [ { "name": "key.four.example.com.",
  "algorithm": "HMAC-SHA224", "secret": "bZEG7Ow8OgAUPfLWV3aAUQ==" } ]
```

One key can serve several domains.

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (The DHCP-DDNS Server chapter (domains, DNS servers, TSIG keys)). Removed: nothing.
Method: documentation only; no commands were run.
