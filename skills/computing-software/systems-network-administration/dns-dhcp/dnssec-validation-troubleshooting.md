---
id: computing-software.systems-network-administration.dns-dhcp.dnssec-validation-troubleshooting
name: dnssec-validation-troubleshooting
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dnssec, dnssec-validation, trust-anchor, delv, dnsviz, bogus, servfail, ad-flag, cd-flag, negative-trust-anchor, rndc-nta, expired-signatures, ds-mismatch, nsec3]
level: advanced
status: docs-checked
description: "Diagnose DNSSEC SERVFAILs: confirm with +cd, trace the chain with delv and DNSViz, recognise expired RRSIGs, DS mismatches and NSEC3 issues, and use negative trust anchors."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/manpages.html#delv-dns-lookup-and-validation-utility
  - https://github.com/dnsviz/dnsviz
  - https://github.com/NLnetLabs/unbound
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNSSEC validation troubleshooting

## Is it DNSSEC?
```
dig www.example.org @resolver               # status: SERVFAIL
dig www.example.org @resolver +cd           # CD = checking disabled: answer appears -> DNSSEC failure
dig www.example.org @resolver +dnssec       # 'ad' flag = validated when it works
```
BIND logs validation problems in the `dnssec` logging category. For Unbound, `unbound-control lookup <name>` shows the servers used for a name, and `log-servfail: yes` prints why queries return SERVFAIL.

## Trace the chain
```
delv @resolver www.example.org A +rtrace +vtrace     # step-by-step validation, says where it breaks
delv www.example.org +multiline                      # validating lookup; reports the failure reason
dnsviz probe -o example.org.json example.org
dnsviz graph -Tpng -o example.org.png example.org < example.org.json   # or use dnsviz.net
```

## Common failures
| Cause | Evidence | Fix |
|---|---|---|
| Expired RRSIGs (signer stopped, inline-signing broken, clock) | RRSIG expiration in the past (`dig +dnssec`), delv "signature expired" | fix signer, re-sign; check NTP on signer |
| DS at parent does not match any DNSKEY (KSK rolled without DS update, provider migration) | DS key tag absent from DNSKEY set | publish correct DS, or remove DS to go insecure |
| Missing RRSIG on some records / on secondaries | one NS serves unsigned data (stale secondary) | fix transfers; check serials match |
| Resolver clock wrong | every signed domain fails | NTP on the resolver |
| NSEC3 parameters (the ARM warns extra iterations cause interoperability problems, RFC 9276) | NXDOMAIN answers fail | `nsec3param iterations 0 optout no salt-length 0` in the dnssec-policy |
| Algorithm unsupported by the validator | treated as insecure or bogus | roll to a widely supported algorithm such as ECDSAP256SHA256 or ED25519 |
| Local unsigned zone under a signed parent | internal names fail on validating resolvers | `validate-except` / domain-insecure / NTA |

## Negative trust anchors (temporary relief for someone else's broken zone)
```
rndc nta -lifetime 1d broken.example.com
rndc nta -dump
unbound-control insecure_add broken.example.com    # Unbound equivalent
```
NTAs disable validation for that domain only and expire (`-lifetime`); remove when fixed. `validate-except` (BIND) and `domain-insecure` (Unbound) are the permanent configuration equivalents. Never disable validation globally.

## Trust anchors
BIND `dnssec-validation auto` uses a built-in root trust anchor, kept current by RFC 5011 key management; `trust-anchors` entries with `initial-key` or `initial-ds` are maintained the same way, while `static-key`/`static-ds` are permanent. A new install needs a BIND release recent enough to have the current root key built in. Unbound uses `auto-trust-anchor-file` (see `unbound-anchor`).

## Verify
- [ ] delv reports `fully validated`; DNSViz chain has no errors (warnings reviewed).
- [ ] Any NTA has an expiry and a ticket.

## Checked

Date: 2026-10-26. BIND 9 ARM and man-page sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus bind-9.20 branch checks), read on 2026-10-26. Also read NLnetLabs/unbound doc sources (unbound-control, unbound.conf) and dnsviz README. Confirmed: dig +cd flow is standard; delv +rtrace/+vtrace/+multiline options; rndc nta options (-lifetime, -dump); validate-except versus NTA; unbound-control lookup and insecure_add; log-servfail; domain-insecure; auto-trust-anchor-file; trust-anchors initial-key/static-key semantics; nsec3param example from the dnssec-policy grammar; dnsviz probe/graph syntax. Removed unconfirmed log message strings, the algorithm list and the 2018 roll remark.

Method: documentation only; no commands were run.
