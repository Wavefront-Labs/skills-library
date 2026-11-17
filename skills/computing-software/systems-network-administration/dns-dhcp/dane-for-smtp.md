---
id: computing-software.systems-network-administration.dns-dhcp.dane-for-smtp
name: dane-for-smtp
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dane-smtp, tlsa-record, dnssec, smtp-tls, mta-security]
level: practitioner
status: verified
description: "Deploy DANE for SMTP: DNSSEC-signed MX hosts, TLSA 3 1 1 records on port 25, Postfix sending-side validation, rollover and monitoring."
sources:
  - https://www.rfc-editor.org/rfc/rfc7672
  - https://github.com/vdukhovni/postfix/blob/master/postfix/html/TLS_README.html
  - https://datatracker.ietf.org/doc/html/rfc7671
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DANE for SMTP

SMTP between MTAs uses opportunistic STARTTLS, which an attacker can strip. DANE (RFC 7672) lets a
sending MTA require TLS and verify the receiving server's key via DNSSEC.

## Receiving side (publishing)
1. Sign the zone containing the MX hostnames (and the domain's MX RRset) with DNSSEC.
2. Publish TLSA for each MX host on port 25:
```
_25._tcp.mx1.example.com. IN TLSA 3 1 1 <sha256 SPKI>
_25._tcp.mx1.example.com. IN TLSA 3 1 1 <next key sha256>     ; pre-published for rollover
```
Use usage 3 (DANE-EE) selector 1 (SPKI) or 2 1 1 pinning your issuing CA key. RFC 7672 says SMTP TLSA
records SHOULD NOT use usages 0 or 1, and Postfix does not support them. The digest is the SHA-256 of the
DER SubjectPublicKeyInfo: `openssl x509 -in c.pem -pubkey -noout | openssl pkey -pubin -outform DER | openssl dgst -sha256`.
Test a record before publishing with `openssl s_client -connect mx1.example.com:25 -starttls smtp
-dane_tlsa_domain mx1.example.com -dane_tlsa_rrdata "3 1 1 <hex>"` (a match prints `DANE TLSA 3 1 1 ... matched the
EE certificate at depth 0`, a miss gives `Verify return code: 65 (no matching DANE TLSA records)`).
3. If MX points to a provider host, the provider must publish TLSA for it. Microsoft documents inbound SMTP DANE with
   DNSSEC for Exchange Online; for other hosters check the MX host's `_25._tcp` name.

## Sending side (Postfix)
```
smtp_dns_support_level = dnssec
smtp_tls_security_level = dane
```
Needs a local validating resolver (Unbound on 127.0.0.1) and `smtp_host_lookup` including `dns`. Postfix logs
`Verified TLS connection established to ...` when the certificate matched the TLSA records (the word is
`Verified`, `Trusted` or `Untrusted` depending on how far verification went). Failure to match published TLSA
records typically defers delivery.

## Rollover
Generate the new key, publish its TLSA next to the old one, wait at least 2 x TTL, deploy the new cert/key, then
remove the old TLSA (RFC 7671 section 8.1; never leave only a not-yet-deployed record published).
Let's Encrypt with automatic key rotation breaks DANE-EE; reuse the key on renewal
(`--reuse-key` in certbot) or pin with 2 1 1.

## Monitoring
- `posttls-finger -t30 -T180 -c -L verbose,summary example.com` checks from the sender's view.
- Test sites (dane.sys4.de / internet.nl) report mismatch before senders defer your mail.

## Verify
- [ ] posttls-finger shows `Verified TLS connection` for every MX, and TLSA records validate with AD.
