---
id: computing-software.systems-network-administration.dns-dhcp.dnssec-manual-signing-with-signzone
name: dnssec-manual-signing-with-signzone
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dnssec, dnssec-signzone, dnssec-keygen, zone-signing, bind]
level: practitioner
status: verified
description: "Sign a zone manually with dnssec-keygen and dnssec-signzone: KSK/ZSK generation, NSEC3 options, re-signing before expiry and publishing DS records."
sources:
  - https://bind9.readthedocs.io/en/latest/manpages.html
  - https://www.rfc-editor.org/rfc/rfc9276
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Manual signing with dnssec-keygen/dnssec-signzone

Modern BIND should use `dnssec-policy` (automatic). Manual signing still matters for offline-signed
zones, static hosting, other servers (NSD) serving a signed file, and understanding what automation does.

## Generate keys
```
cd /etc/bind/keys
dnssec-keygen -a ECDSAP256SHA256 -f KSK example.com     # Kexample.com.+013+12345.{key,private}
dnssec-keygen -a ECDSAP256SHA256 example.com            # ZSK
```
Include the public keys in the zone (`$INCLUDE Kexample.com.+013+12345.key`) or let signzone find
them with `-S` (smart signing). Valid `-a` names include RSASHA256, RSASHA512, ECDSAP256SHA256, ECDSAP384SHA384, ED25519 and ED448; RSASHA1 is deprecated.

## Sign
```
dnssec-signzone -S -K /etc/bind/keys -o example.com -N increment \
  -3 - -H 0 -e +2592000 -j 86400 -f example.com.db.signed example.com.db
```
- `-S` smart signing: use the keys found in the `-K` directory according to their timing metadata.
- `-3 -` NSEC3 with no salt (recommended per RFC 9276), `-H 0` zero iterations (the default).
- `-e +2592000` signatures expire 2592000 seconds (30 days) after the start time (also the default); `-j` jitter randomises expiry so re-signing is spread out.
- `-N increment` increments the SOA serial (the default is `keep`; others are `unixtime`, `date`).
It also writes a `dsset-example.com.` file with the DS records for the parent.

## Serve and publish DS
Point the zone's `file` at `example.com.db.signed`, reload, verify, then submit DS to the registrar.

## Re-signing
Signatures expire. Re-run signzone well before expiry (cron weekly with 30-day validity). Forgetting
this is the classic manual-DNSSEC outage: every validating resolver returns SERVFAIL once RRSIGs expire.

## Verify
```
dnssec-verify -o example.com example.com.db.signed
dig +dnssec example.com SOA @ns1
delv @resolver example.com SOA       # validating lookup through your resolver
delv -a anchor.conf +root=example.com @ns1 example.com SOA   # same, with a trust anchor file (trust-anchors { "example.com." static-ds TAG ALG DIGESTTYPE "HEX"; };) built from the dsset
```
- [ ] dnssec-verify passes and delv reports the answer as validated.

## Checked

Date: 2026-10-26. BIND 9 ARM and man-page sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus bind-9.20 branch checks), read on 2026-10-26. Confirmed against the dnssec-signzone and dnssec-keygen man pages: -S, -K, -o, -N formats (keep default, increment, unixtime, date), -3 with dash for no salt, -H default 0, -e default 30 days and +N syntax, -j jitter, -f, dsset file, -a algorithm names, -f KSK, dnssec-verify -o, delv +rtrace/+vtrace options.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (BIND 9.20.30): dnssec-keygen -a ECDSAP256SHA256 with and without -f KSK, key creation with RSASHA256, RSASHA512, ECDSAP384SHA384, ED25519, ED448 and RSASHA1; dnssec-signzone -S -K -o -N increment -3 - -H 0 -e +2592000 -j 86400 -f (serial 2026110101 became 2026110102, NSEC3PARAM `1 0 0 -`, RRSIG expiry about 29 to 30 days after inception, dsset file written); dnssec-verify -o; the signed file served by named with dig +dnssec; delv with a static-ds trust anchor from the dsset reporting `fully validated`. Not run: -N unixtime and date, the effect of -j, re-signing before expiry.
