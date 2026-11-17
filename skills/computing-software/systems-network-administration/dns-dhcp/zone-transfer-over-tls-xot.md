---
id: computing-software.systems-network-administration.dns-dhcp.zone-transfer-over-tls-xot
name: zone-transfer-over-tls-xot
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, xot, zone-transfers, dns-over-tls, bind, rfc9103]
level: practitioner
status: docs-checked
description: "Encrypt zone transfers with XoT (RFC 9103) between BIND primaries and secondaries: tls blocks, listen-on tls, primaries with tls, and verification."
sources:
  - https://www.rfc-editor.org/rfc/rfc9103
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Zone transfer over TLS (XoT)

AXFR/IXFR over TCP 53 is plaintext; TSIG authenticates but does not hide zone contents. XoT runs
transfers over TLS, by default on port 853 (RFC 9103; BIND supports it, check other vendors' documentation for theirs).

## Primary
```
tls primary-tls {
    cert-file "/etc/bind/tls/ns1.crt";
    key-file  "/etc/bind/tls/ns1.key";
};
options {
    listen-on port 853 tls primary-tls { any; };
    listen-on port 53 { any; };
};
zone "example.com" {
    type primary; file "example.com.db";
    allow-transfer port 853 transport tls { key "xfr-key"; };
};
```

## Secondary
```
tls to-primary {
    remote-hostname "ns1.example.com";     // verify the certificate name (strict TLS)
    ca-file "/etc/bind/tls/ca.pem";
};
zone "example.com" {
    type secondary; file "sec/example.com.db";
    primaries { 192.0.2.53 port 853 key "xfr-key" tls to-primary; };
};
```
Without `remote-hostname` or `ca-file`, TLS to primaries is opportunistic: encrypted but not authenticated, so it does not stop man-in-the-middle attacks; keep TSIG for authentication in that case. With `remote-hostname` and `ca-file` it is strict TLS (if `remote-hostname` is omitted but `ca-file` is set, the server IP address is used for verification).

## NOTIFY
The ARM says `allow-transfer ... transport` limits are for the transfer transports (TCP and TLS); do not assume NOTIFY moves to TLS.

## Verify the transport
```
rndc retransfer example.com
grep "transfer of 'example.com" /var/log/named/xfer.log    # check the transport and port in the log line
ss -tnp | grep :853
dig @192.0.2.53 +tls example.com AXFR -y hmac-sha256:xfr-key:<secret>
```

## Gotchas
- Firewalls must allow TCP 853 between servers.
- Certificate expiry breaks strict XoT until the next refresh fails; monitor certificate dates.
- Mixing vendors: confirm both ends support XoT and its authentication model.

## Verify
- [ ] The secondary log shows a successful transfer over TLS and packet capture shows no AXFR on port 53.

## Checked

Date: 2026-10-26. BIND 9 ARM and man-page sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27; grammar cross-checked on bind-9.20), read on 2026-10-26. Confirmed: tls block options (ca-file, cert-file, key-file, remote-hostname), remote-servers/primaries `tls` keyword, unauthenticated-by-default warning and strict TLS behaviour, allow-transfer `port 853 transport tls` example, dig +tls. Removed unconfirmed BIND version and Knot/NSD option names, and the NOTIFY-over-TCP statement.

Method: documentation only; no commands were run.
