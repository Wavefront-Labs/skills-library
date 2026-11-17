---
id: computing-software.systems-network-administration.dns-dhcp.wpad-option-252-and-dns-wpad
name: wpad-option-252-and-dns-wpad
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, wpad, option-252, proxy-autoconfig, pac-file, security]
level: practitioner
status: gated
description: "Configure Web Proxy Auto-Discovery via DHCP option 252 and DNS wpad records, serve the PAC file correctly, and block WPAD spoofing risks."
sources:
  - https://datatracker.ietf.org/doc/html/draft-ietf-wrec-wpad-01
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#custom-dhcpv4-options
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WPAD option 252

Browsers with "Automatically detect settings" look for a PAC file via:
1. DHCP option 252 (URL string);
2. DNS: `http://wpad.<domain>/wpad.dat`, stripping the leading label of the client's domain step by
   step (the expired draft-ietf-wrec-wpad-01 pseudo-code).
Which methods a given browser or OS implements varies, so test your clients. IANA lists 224-254 as
private use, so 252 is a de facto code, not an assigned option.

## DHCP option 252
Kea (custom option):
```json
"option-def": [ { "name": "wpad", "code": 252, "type": "string" } ],
"option-data": [ { "name": "wpad", "data": "http://proxy.corp.example.com/wpad.dat" } ]
```
Windows DHCP: Set Predefined Options > Add > code 252, String. Clients request it only when
auto-detect is on (gated: unconfirmed, source is paywalled or blocked) (`dhcp.option.request_list_item == 252` matches a request list
containing 252; it matched a test packet in tshark 4.4.1).

## DNS
```
wpad.corp.example.com. IN A 10.0.0.80
```
Serve `wpad.dat` with MIME type `application/x-ns-proxy-autoconfig`.
Windows DNS blocks `wpad` and `isatap` names by default (Global Query Block List); remove from the
list only if you intentionally use DNS WPAD: `Set-DnsServerGlobalQueryBlockList`. (gated: unconfirmed, source is paywalled or blocked)

## PAC example
Run in Node with `isPlainHostName` and `dnsDomainIs` stubbed as MDN defines them, it returned `DIRECT`
for `intranet` and `a.corp.example.com` and the proxy line for `www.example.org`.
```js
function FindProxyForURL(url, host) {
  if (isPlainHostName(host) || dnsDomainIs(host, ".corp.example.com")) return "DIRECT";
  return "PROXY proxy.corp.example.com:8080; DIRECT";
}
```

## Security
- WPAD lookups leak to the internet for names like `wpad.corp` or new gTLDs, and attackers on the
  LAN can answer via LLMNR/NBT-NS to hijack proxies and capture credentials. (gated: unconfirmed, source is paywalled or blocked)
- Mitigate: register/own `wpad.<your-domain>`, disable LLMNR and NetBIOS, or disable auto-detect and
  push an explicit PAC URL by GPO/MDM.

## Verify
- [ ] Clients fetch the PAC from the intended host (check proxy logs) and `wpad` lookups never leave the network.
