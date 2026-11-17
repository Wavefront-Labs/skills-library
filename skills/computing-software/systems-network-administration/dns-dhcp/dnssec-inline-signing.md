---
id: computing-software.systems-network-administration.dns-dhcp.dnssec-inline-signing
name: dnssec-inline-signing
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [bind, dnssec, inline-signing, bump-in-the-wire, signed-zone, dnssec-policy, raw-zone]
level: practitioner
status: verified
description: "Sign zones without touching the zone file using BIND inline-signing: raw vs signed copies, serial handling, signing a zone received from a hidden primary, and checking signatures."
sources:
  - https://bind9.readthedocs.io/en/latest/dnssec-guide.html
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-inline-signing
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DNSSEC inline signing

Inline signing keeps the unsigned zone (edited by humans, DNS-as-code or an IPAM) separate from the
signed zone served to the world. BIND maintains `example.net.db.signed` with RRSIGs, NSEC/NSEC3 and
DNSKEYs automatically.

## On the primary
```
zone "example.net" {
    type primary;
    file "zones/example.net.db";      // unsigned, you edit this
    dnssec-policy default;
    inline-signing yes;               // enabled by default with dnssec-policy; an explicit zone setting overrides the policy
};
```
Edit the unsigned file, bump the serial, `rndc reload example.net`. BIND resigns changed records and
keeps the signed version in the zone's `file` name with a `.signed` extension. Never edit the `.signed` file.

## Bump-in-the-wire signer
A hidden primary (IPAM, AD DNS, a provisioning system) sends the unsigned zone by AXFR to a BIND
signer, which serves/forwards the signed zone to public secondaries:
```
zone "example.net" {
    type secondary;
    primaries { 10.0.0.10 key xfr-key; };
    file "zones/example.net.db";
    dnssec-policy default;
    inline-signing yes;
    allow-transfer { key pub-xfr; };
    notify yes;
};
```
The signed zone may have a different serial number from the unsigned zone; public
secondaries see the signer's serial, not the hidden primary's.

## Check
```
rndc signing -list example.net
rndc zonestatus example.net          # reports whether the zone is DNSSEC signed and uses inline signing
dig @localhost example.net DNSKEY +multi
dig @localhost www.example.net A +dnssec | grep RRSIG
```

## Gotchas
- Do not point `dnssec-verify` at the `.signed` file of a running zone: it is raw format (plain `dnssec-verify` fails with a syntax error, `-I raw` is needed) and lags behind the `.signed.jnl` journal, so it reported `Zone contains no DNSSEC keys`, and after `rndc sync -clean` still `not fully signed` for a default-policy zone. Verify the served answers with `dig +dnssec` or `delv`.
- Raw serial and signed serial differ; monitoring that compares the hidden primary with public
  servers by serial will alarm. Compare signed serials among public servers instead.
- The key and zone directories must be writable by named.
- Removing inline signing or the policy without a plan breaks validation (DS still at parent): go
  insecure deliberately (`dnssec-policy insecure`, remove DS, wait TTLs).

## Verify
- [ ] `rndc zonestatus` shows the zone as signed, and DNSViz shows a valid chain from the parent DS.

## Checked

Date: 2026-10-26. BIND 9 ARM and man-page sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus bind-9.20 branch checks), read on 2026-10-26. Confirmed: inline-signing default and per-zone override, .signed file naming and possibly different serial (reference.rst), rndc signing -list and zonestatus descriptions (rndc man page), dnssec-verify -o, dnssec-policy insecure. Removed the unconfirmed 9.20 default claim, journal file claim and serial-update-method claim.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (BIND 9.20.30): a primary with `dnssec-policy default; inline-signing yes;` signed automatically (DNSKEY, RRSIG, `.signed` plus `.signed.jnl`), a zone with only `dnssec-policy default` also reporting `inline signing: yes` in `rndc zonestatus`, signed serial differing from the unsigned serial (2026110104 versus 2026110105 on edit and reload, and 2026110103 versus 2026110101 on a secondary), `rndc signing -list`, a bump-in-the-wire secondary with `dnssec-policy default; inline-signing yes;` serving RRSIGs with its own keys. Corrected: dnssec-verify on the `.signed` file. Not run: dnssec-policy insecure transition, DS submission.
