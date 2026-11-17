---
id: computing-software.systems-network-administration.dns-dhcp.bimi-brand-indicator-records
name: bimi-brand-indicator-records
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bimi, email-authentication, dmarc, vmc, svg-tiny-ps]
level: practitioner
status: verified
description: "Publish a BIMI record to show a brand logo in mail clients: DMARC enforcement prerequisite, SVG Tiny PS logo, VMC/CMC certificates and validation."
sources:
  - https://bimigroup.org/implementation-guide/
  - https://datatracker.ietf.org/doc/draft-brand-indicators-for-message-identification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIMI

Brand Indicators for Message Identification lets supporting mailbox providers show your logo next to
authenticated mail. BIMI is still an IETF Internet-Draft (draft-brand-indicators-for-message-identification-14,
May 2026, expires 2 November 2026), not an RFC; Gmail's setup page is the most concrete provider reference.

## Prerequisites
- DMARC at enforcement on the organisational domain AND the RFC5322.From domain: `p=quarantine`
  (the draft says quarantine MUST NOT have `pct` below 100) or `p=reject`. Gmail: `p` must be quarantine or reject,
  `p=none` is not supported, and `pct` must be 100.
- SPF and DKIM aligned for the mail streams.
- Logo in SVG Tiny Portable/Secure (SVG Tiny PS) format: `baseProfile="tiny-ps"`, `version="1.2"`, a `<title>`
  element (BIMI Group); Gmail also recommends a logo centred in a square on a solid background, 32 KB or smaller.
  Plain SVG Tiny 1.2 exports need modification to comply. The draft accepts only SVG or SVGZ in `l=`.
- Gmail requires a Verified Mark Certificate (VMC, based on a registered trademark) or Common Mark Certificate
  (CMC, no trademark needed) from a Mark Verifying Authority. BIMI Group calls the certificate optional but says
  self-asserted BIMI records have limited support across mailbox providers.

## Record
```
default._bimi.example.com. IN TXT "v=BIMI1; l=https://example.com/bimi/logo.svg; a=https://example.com/bimi/vmc.pem"
```
- `l=` HTTPS URL of the SVG; `a=` HTTPS URL of the VMC/CMC PEM (empty or absent means no evidence). `v=BIMI1`
  must be the first tag.
- Other selectors: mail can carry `BIMI-Selector: v=BIMI1; s=brand2;` to pick `brand2._bimi`; the draft says
  receivers should ignore the header unless it is covered by the DMARC-aligned DKIM signature.
- Opt out (explicit declination, distinct from publishing nothing, e.g. for a subdomain): `v=BIMI1; l=; a=;`.

## Validate
```
dig +short TXT default._bimi.example.com
```
Provider and BIMI Group tools validate the SVG and VMC. The draft has the receiver add `BIMI-Location` and
`BIMI-Indicator` headers and a BIMI result in Authentication-Results; those headers must not be DKIM signed.

## Gotchas
- Providers apply their own extra display rules, so a valid record does not guarantee the logo appears (check the provider's page).
- A VMC or CMC is issued for a specific logo, so changing the logo means a new certificate.

## Verify
- [ ] DMARC at enforcement, validator passes, and the logo shows in a test mailbox at a supporting provider.
