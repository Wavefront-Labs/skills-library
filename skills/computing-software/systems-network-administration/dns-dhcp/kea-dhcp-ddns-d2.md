---
id: computing-software.systems-network-administration.dns-dhcp.kea-dhcp-ddns-d2
name: kea-dhcp-ddns-d2
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dns, kea, dynamic-dns, ddns, kea-ddns, dhcp-ddns, kea-dhcp-ddns, d2, dhcid, tsig, forward-ddns, reverse-ddns, ddns-qualifying-suffix, conflict-resolution]
level: advanced
status: verified
description: "Register DHCP clients in DNS with Kea DHCP-DDNS (D2): enabling DDNS, forward/reverse domains with TSIG, qualifying suffix, DHCID conflict resolution."
sources:
  - https://kea.readthedocs.io/en/latest/arm/ddns.html
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#ddns-for-dhcpv4
  - https://datatracker.ietf.org/doc/html/rfc4703
  - https://datatracker.ietf.org/doc/html/rfc4701
  - https://datatracker.ietf.org/doc/html/rfc2136
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea DHCP-DDNS (D2)

Kea splits DDNS: kea-dhcp4/6 decide **what** to register and send name change requests (NCRs)
to the separate `kea-dhcp-ddns` daemon (D2), which performs RFC 2136 updates against DNS.

## kea-dhcp4 side
```json
"Dhcp4": {
  "dhcp-ddns": {"enable-updates": true, "server-ip": "127.0.0.1", "server-port": 53001},
  "ddns-send-updates": true,
  "ddns-qualifying-suffix": "dyn.example.org.",
  "ddns-override-client-update": true,
  "ddns-replace-client-name": "when-not-present",
  "ddns-generated-prefix": "host",
  "ddns-conflict-resolution-mode": "check-with-dhcid",
  "hostname-char-set": "[^A-Za-z0-9.-]", "hostname-char-replacement": "-"
}
```
- Clients sending option 81 (FQDN) or 12 (hostname) get `<name>.dyn.example.org`; clients without a
  name get `host-10-20-10-57.dyn.example.org` when `when-not-present` (the format is
  `[ddns-generated-prefix]-[address-text].[ddns-qualifying-suffix].`; the default prefix is
  `myhost`). `ddns-replace-client-name` defaults to `never`.
- `dhcp-ddns.enable-updates` (default false) only controls whether kea-dhcp4 connects to D2;
  `ddns-send-updates` (default true) decides per scope whether updates are requested. Both must
  allow it.
- `ddns-override-client-update: true` makes Kea ignore a client's request to do its own updates and
  send forward and reverse updates itself (N-S-O flags 0-1-1 in the reply); with
  `ddns-override-no-update: true` it also updates for clients that asked for no updates.
- The behaviour parameters can be set globally or per shared-network, subnet and (Kea 2.7.6+) pool,
  e.g. a different suffix per site; the connectivity parameters live only in `dhcp-ddns`.

## D2 side (kea-dhcp-ddns.conf)
```json
"DhcpDdns": {
  "ip-address": "127.0.0.1", "port": 53001,
  "tsig-keys": [{"name": "dhcp-key", "algorithm": "HMAC-SHA256", "secret": "<BASE64_SECRET>"}],
  "forward-ddns": {"ddns-domains": [
     {"name": "dyn.example.org.", "key-name": "dhcp-key", "dns-servers": [{"ip-address": "10.0.0.10"}]}]},
  "reverse-ddns": {"ddns-domains": [
     {"name": "20.10.in-addr.arpa.", "key-name": "dhcp-key", "dns-servers": [{"ip-address": "10.0.0.10"}]}]}
}
```
On BIND grant the key A/AAAA/PTR/DHCID updates on those zones (see nsupdate-and-update-policy).

## Conflict resolution
With `check-with-dhcid` (RFC 4703), D2 adds a **DHCID** record alongside each A/AAAA proving which
client owns the name; another client claiming the same hostname is refused rather than hijacking
it. `no-check-with-dhcid` (any client may overwrite, new entries still get DHCID),
`check-exists-with-dhcid` (overwrite only entries that have a DHCID, which protects static records)
and `no-check-without-dhcid` (overwrite anything, no DHCID written) relax it, and any mode other
than the default disables the RFC 4703 overwrite safeguards. The mode parameter replaced the older
boolean `ddns-use-conflict-resolution` in Kea 2.5.0. Leases expiring or released trigger removals.

## Troubleshoot
- Loggers `kea-dhcp-ddns.d2-to-dns`, `kea-dhcp4.ddns` at DEBUG.
- D2 logs `DHCP_DDNS_ADD_SUCCEEDED` on success and, for example, `DHCP_DDNS_FORWARD_ADD_REJECTED`
  with the RCODE when the DNS server refuses. REFUSED (RCODE 5) means the server refuses to
  perform the update, typically a key or grant problem; NOTAUTH (RCODE 9, RFC 2136) means the
  server is not authoritative for the zone, so the domain or server in the D2 config is wrong.
- Clients that update DNS themselves (for example AD-joined hosts): decide which side owns
  registration, and use `ddns-override-client-update` only if Kea should take it over.

## Verify
- [ ] New lease creates A and PTR (and DHCID) records; release removes them.
- [ ] A second client using the same hostname does not overwrite the first.
