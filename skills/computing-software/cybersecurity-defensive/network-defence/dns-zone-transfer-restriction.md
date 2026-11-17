---
id: computing-software.cybersecurity-defensive.network-defence.dns-zone-transfer-restriction
name: dns-zone-transfer-restriction
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [zone-transfer, axfr, ixfr, tsig, authoritative-dns, dns-security, bind]
level: practitioner
status: docs-checked
description: "Restrict DNS zone transfers: allow-transfer to named secondaries only, TSIG-authenticated AXFR/IXFR, notify settings, testing for open transfers and split-horizon leakage."
sources: ["https://bind9.readthedocs.io/en/latest/reference.html", "https://datatracker.ietf.org/doc/html/rfc8945", "https://learn.microsoft.com/en-us/windows-server/networking/dns/manage-dns-zones"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zone transfer restriction

An open AXFR hands an attacker your full zone: hostnames, internal naming, mail and VPN endpoints.

## BIND (primary)
```
key "xfer-ns2" { algorithm hmac-sha256; secret "<base64>"; };
acl secondaries { 192.0.2.53; };
options { allow-transfer { none; }; };          # default deny
zone "example.com" {
  type primary; file "db.example.com";
  allow-transfer { key xfer-ns2; };
  also-notify { 192.0.2.53; };
};
```
Secondary: `server <primary-ip> { keys { xfer-ns2; }; };` and `primaries { <primary-ip> key xfer-ns2; };`.

## Windows DNS
Zone properties -> Zone Transfers -> "Only to servers listed on the Name Servers tab" or a specific list;
AD-integrated zones replicate via AD and need no transfers - disable transfers entirely for them.

## Managed DNS
Check each provider's documentation for whether zone transfers are offered and how they are restricted.

## Test (from outside and from a user subnet)
```
dig axfr example.com @ns1.example.com
# expected: the transfer is refused
```
Also test every listed NS and IPv6 addresses - one forgotten secondary often allows it.

## Split horizon
Internal views must not be transferable to external secondaries; keep internal zones on internal-only
servers.

## Verify
- [ ] AXFR refused from unauthenticated sources on all NS (v4 and v6).
- [ ] Secondaries transfer successfully with TSIG (logs show the transfer completing with the key name).

## Checked
2026-10-28. Confirmed against official pages: BIND allow-transfer, also-notify, primaries and TSIG keys (BIND 9 reference, RFC 8945), Windows DNS Zone Transfers tab options and AD-integrated zones (Microsoft Learn: manage DNS zones).
Removed or rewritten: the tsig-keygen comment, the managed-DNS default claim, and quoted dig and log output strings.
Method: documentation only; no commands were run.
