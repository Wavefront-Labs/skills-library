---
id: computing-software.systems-network-administration.dns-dhcp.isc-dhcp-ddns-to-kea-d2
name: isc-dhcp-ddns-to-kea-d2
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, ddns-migration, kea-dhcp-ddns, dynamic-dns, isc-dhcp-migration]
level: practitioner
status: verified
description: "Convert ISC dhcpd DDNS settings (ddns-update-style, zone statements, TSIG keys) to Kea DHCP-DDNS (D2) forward/reverse domains and server parameters."
sources:
  - https://kea.readthedocs.io/en/latest/arm/ddns.html
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#ddns-for-dhcpv4
  - https://github.com/isc-projects/dhcp/blob/master/server/dhcpd.conf.5
  - https://datatracker.ietf.org/doc/html/rfc4701
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converting DDNS settings to D2

dhcpd did DNS updates in-process. Kea splits it: kea-dhcp4/6 decide what to update and send name
change requests to the separate `kea-dhcp-ddns` (D2) daemon, which talks to DNS servers.

## Mapping
| dhcpd | Kea |
|-------|-----|
| `ddns-update-style standard;` (or interim) | `"ddns-send-updates": true` (default) + `dhcp-ddns.enable-updates: true` (default false); Kea has only the standard DHCID scheme |
| `ddns-domainname "corp.example.com";` | `"ddns-qualifying-suffix": "corp.example.com."` |
| `ddns-rev-domainname` | reverse domains in D2 |
| `zone corp.example.com. { primary 10.0.0.53; key ddns-key; }` | D2 `forward-ddns.ddns-domains` |
| `zone 5.0.10.in-addr.arpa. { ... }` | D2 `reverse-ddns.ddns-domains` |
| `key ddns-key { algorithm hmac-sha256; secret ...; }` | D2 `tsig-keys` |
| `update-conflict-detection` | `"ddns-conflict-resolution-mode"` (since Kea 2.5.0, stable 2.6: `check-with-dhcid` (default), `no-check-with-dhcid`, `check-exists-with-dhcid`, `no-check-without-dhcid`) |
| `update-optimization` | `ddns-update-on-renew` (default false: no DNS update on renewal unless something changed); not a one-to-one match, read both docs |
| `allow client-updates` (dhcpd default: honour a client's request to update its own A record) | Kea default `ddns-override-client-update: false` |
| `ignore client-updates` / `deny client-updates` (server does the updates itself) | `ddns-override-client-update: true` (Kea then sends both forward and reverse updates and replies with N-S-O flags 0-1-1); `ddns-override-no-update: true` additionally updates for clients that asked for no updates (no matching statement in the dhcpd.conf man page checked) |

## kea-dhcp4 snippet
```json
"dhcp-ddns": { "enable-updates": true, "server-ip": "127.0.0.1", "server-port": 53001 },
"ddns-send-updates": true,
"ddns-qualifying-suffix": "corp.example.com.",
"ddns-replace-client-name": "when-not-present",
"ddns-generated-prefix": "dhcp"
```

## kea-dhcp-ddns.conf
```json
{ "DhcpDdns": {
  "ip-address": "127.0.0.1", "port": 53001,
  "tsig-keys": [ { "name": "ddns-key", "algorithm": "HMAC-SHA256", "secret": "..." } ],
  "forward-ddns": { "ddns-domains": [ { "name": "corp.example.com.", "key-name": "ddns-key", "dns-servers": [ { "ip-address": "10.0.0.53" } ] } ] },
  "reverse-ddns": { "ddns-domains": [ { "name": "5.0.10.in-addr.arpa.", "key-name": "ddns-key", "dns-servers": [ { "ip-address": "10.0.0.53" } ] } ] }
} }
```

## Existing records
dhcpd's interim style used a TXT RR for conflict detection, the standard style uses a DHCID RR
(RFC 4701), and the two are not equivalent (the TXT format resembles DHCID but differs, for
example MD5 versus SHA-2). Kea uses DHCID only, so records written by interim-style dhcpd carry no
DHCID that Kea recognises: with the default `check-with-dhcid` an existing name without a
matching DHCID is not overwritten. Clean those records up, or relax the mode during the
transition (`no-check-with-dhcid` allows any client to overwrite, and any mode other than the
default disables the RFC 4703 safeguards).

## Verify
- [ ] A new lease creates A and PTR records (plus DHCID) and lease expiry removes them; D2 logs show `DHCP_DDNS_ADD_SUCCEEDED`.
