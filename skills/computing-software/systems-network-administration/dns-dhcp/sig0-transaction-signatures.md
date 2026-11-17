---
id: computing-software.systems-network-administration.dns-dhcp.sig0-transaction-signatures
name: sig0-transaction-signatures
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, sig0, dynamic-dns, public-key-authentication, nsupdate, bind]
level: practitioner
status: verified
description: "Authenticate DNS dynamic updates with SIG(0) public-key signatures in BIND: key generation, KEY records, update-policy, nsupdate usage and limits."
sources:
  - https://www.rfc-editor.org/rfc/rfc2931
  - https://bind9.readthedocs.io/en/latest/chapter7.html#sig-0
  - https://bind9.readthedocs.io/en/latest/manpages.html#nsupdate-dynamic-dns-update-utility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SIG(0)

SIG(0) signs DNS messages with a private key whose public KEY record lives in DNS. Unlike TSIG
there is no shared secret on the server, which suits many clients each with their own key.

## Create a client key
```
dnssec-keygen -a ED25519 -T KEY -n HOST host1.example.com
# Khost1.example.com.+015+23456.key / .private
```
Publish the public KEY record in the zone (it must be in a zone the server serves; BIND does not fetch or validate it
elsewhere). Flags 512 are the RFC 2535 NAMTYP "entity/host" value, protocol 3, algorithm 15 is Ed25519 (parses in
dnspython as `512 3 15 <base64 of the 32-byte raw key>`):
```
host1.example.com. IN KEY 512 3 15 <base64>
```

## Allow updates
```
zone "example.com" {
    type primary; file "dyn/example.com.db";
    update-policy {
        grant host1.example.com. self host1.example.com. A AAAA;    // key name = owner name
        grant *.dyn.example.com. selfsub . ANY;
    };
};
```
The signer is identified by the KEY owner name. For `self` the ARM says the record name must match the `identity`
field and the `name` field is ignored, so set it equal to identity or `.`.

## Update with nsupdate
```
nsupdate -k Khost1.example.com.+015+23456.private <<EOF
server ns1.example.com
update delete host1.example.com A
update add host1.example.com 300 A 198.51.100.21
send
EOF
```

## Limits and cautions
- CVE-2024-1975 (CPU exhaustion through SIG(0) signed requests; affected 9.18.0 to 9.18.27, fixed in 9.18.28 and
  9.20.0). The 9.18.28 release notes say support for SIG(0) message validation was removed from that version of
  named. The 9.21.6 development release notes add `sig0key-checks-limit` (default 16) and `sig0message-checks-limit`
  (default 2), and the current ARM again describes partial SIG(0) support (verified only if the key is known and
  trusted, no signing of multi-message TCP streams; `nsupdate` is the only BIND tool that generates SIG(0) messages).
  Read the ARM and release notes of your exact BIND version before choosing it.
- Prefer TSIG (per-client keys with update-policy) or GSS-TSIG in AD environments.

## Verify
- [ ] nsupdate succeeds with the key, fails without it, and the record appears with the expected TTL.
