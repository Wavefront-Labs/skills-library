---
id: computing-software.systems-network-administration.dns-dhcp.dkim-selectors-and-key-rotation
name: dkim-selectors-and-key-rotation
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, email-authentication, dkim, dkim-selector, domainkey, txt, cname, key-rotation, rsa-2048, ed25519, opendkim, d-tag, email-dns]
level: practitioner
status: verified
description: "Publish and rotate DKIM keys: selector naming, TXT vs CNAME delegation to providers, 2048-bit keys split across strings, safe rotation and header checks."
sources:
  - https://datatracker.ietf.org/doc/html/rfc6376
  - https://datatracker.ietf.org/doc/html/rfc8463
  - https://www.m3aawg.org/sites/default/files/m3aawg-dkim-key-rotation-bp-2019-03.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DKIM selectors and key rotation

DKIM signs selected headers and the body; receivers fetch the public key from DNS at
`<selector>._domainkey.<domain>` (the `s=` and `d=` tags of the DKIM-Signature header).

## Publish
Self-hosted (OpenDKIM, Postfix/rspamd, Exchange via a signing gateway):
```
s2026a._domainkey.example.org. TXT ( "v=DKIM1; k=rsa; "
  "p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...first-part..."
  "...second-part...IDAQAB" )
```
- RSA **2048-bit** (RFC 8301: signers MUST use at least 1024 bits and SHOULD use at least 2048; verifiers must
  accept 1024 to 4096). A 2048-bit key's `p=` is 392 characters, so the record is ~410 characters: over the 255-byte
  limit of one TXT character-string, so it must be split into several strings in one TXT record (dnspython rejects
  a 410-character single string with `string too long`; split at 255 and it gives strings of 255 and 155). Most
  DNS UIs do this; some need it manual. Receivers join the strings.
- Ed25519 (RFC 8463, `k=ed25519`, `p=` is the 32-byte raw key in base64, 44 characters, not SPKI) is allowed but
  not universally verified: dual-sign with RSA if used.
Hosted providers: Microsoft 365 uses two CNAMEs, `selector1._domainkey` and `selector2._domainkey`, pointing at
`selector1-<CustomDomainWithDashes>._domainkey.<InitialDomainPrefix>.<DynamicPartitionCharacter>-v1.dkim.mail.microsoft`
(and the selector2 equivalent). Older tenants may still show `...onmicrosoft.com` targets, so copy the exact values
from the Defender portal or Exchange Online PowerShell; Microsoft activates the second selector on rotation.
Google Workspace gives a TXT at `google._domainkey` (default prefix selector). Use CNAME delegation where offered
so the provider can rotate.

## Selector naming
Unique per sending system and per key generation: `m365-1`, `mkt2026a`, `s2026a`. Never reuse a
selector name for a new key.

## Rotation (at least every six months per M3AAWG, or on compromise)
1. Generate the new key; publish `s2026b._domainkey` TXT.
2. Wait for TTL/propagation (and at least a day).
3. Switch the signer to the new selector.
4. Keep the old public key published unchanged for at least 7 days and up to 30 (M3AAWG; mail in queues and
   delayed verification).
5. Retire it by setting `p=` empty (revoked; a signature then fails verification, checked with dkimpy) and do not
   reuse the selector. RFC 6376 defines no semantic difference between a revoked and a removed record.

## Test
```
dig +short TXT s2026a._domainkey.example.org
opendkim-testkey -d example.org -s s2026a -vvv
```
Header of received mail: `DKIM-Signature: ... d=example.org; s=s2026a;` and
`Authentication-Results: ... dkim=pass header.d=example.org`. For DMARC alignment, `d=` must match
(or be a subdomain of, in relaxed mode) the From domain.

## Verify
- [ ] Every sending system signs with an aligned `d=` and passes at Gmail/Outlook test mailboxes.
- [ ] Key length >= 2048; rotation date recorded.
