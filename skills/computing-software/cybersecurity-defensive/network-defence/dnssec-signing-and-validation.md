---
id: computing-software.cybersecurity-defensive.network-defence.dnssec-signing-and-validation
name: dnssec-signing-and-validation
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [dns-security, dnssec, dnssec-validation, ksk-zsk, ds-record, key-rollover, bind]
level: advanced
status: docs-checked
description: "Sign authoritative zones with DNSSEC and enable validation on resolvers: key strategy, automated signing in BIND or managed DNS, DS publication, rollovers and troubleshooting."
sources: ["https://bind9.readthedocs.io/en/latest/reference.html", "https://datatracker.ietf.org/doc/html/rfc9276"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNSSEC signing and validation

**Goal:** your zones are signed so resolvers can detect forged answers, and your resolvers validate others' signatures.

## Signing (authoritative)
BIND with `dnssec-policy` (automated keys and rollovers; see the dnssec-policy section of the ARM for the key, lifetime and NSEC3 options):
```
dnssec-policy "standard" {
  nsec3param iterations 0 optout no salt-length 0;
};
zone "corp-example.com" { type primary; file "db.corp-example.com"; dnssec-policy "standard"; inline-signing yes; };
```
- If NSEC3 is used, RFC 9276 requires an iterations count of 0.
- Many managed DNS providers offer DNSSEC signing; check the provider's documentation.

## Chain of trust
Publish the DS record (from your provider console or key tooling, or CDS/CDNSKEY automation if the registry supports it) at the registrar. Without DS, the zone is signed but not validated ("island of security").

## Rollovers
- ZSK rollovers are automatic with dnssec-policy.
- KSK rollover requires DS update at parent: publish new DS, wait for parent TTL, retire old key. Use `rndc dnssec -checkds published` to tell BIND when DS is live.
- Moving DNS providers on a signed zone needs a coordinated multi-signer or go-insecure-then-resign plan to avoid outage.

## Validation (resolvers)
- BIND `dnssec-validation auto;`, Unbound `auto-trust-anchor-file`.
- Clients get `ad` flag; failures return SERVFAIL.

## Troubleshoot
`dig +dnssec corp-example.com SOA` and a DNSSEC chain-analysis tool. Common failures: expired signatures (signer stopped), DS mismatch after key change, clock skew on validators.

## Verify
- [ ] A DNSSEC analysis tool shows a secure chain with no errors.
- [ ] Monitoring alerts on RRSIG expiry before signatures lapse.
- [ ] A query for a deliberately mis-signed test zone returns SERVFAIL (validation on).

## Checked
2026-10-28. Confirmed against official pages: dnssec-policy, nsec3param, inline-signing and rndc dnssec -checkds (BIND 9 reference); NSEC3 iterations count of 0 (RFC 9276).
Removed or rewritten: the version gate, explicit algorithm names, Route 53/KMS and one-click claims, dnssec-dsfromkey, the Windows trust-anchor cmdlet, DNSViz/delv/Verisign tool names, the 7-day figure and the dnssec-failed.org test; non-URL sources replaced.
Method: documentation only; no commands were run.
