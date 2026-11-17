---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.verifying-spf-dkim-dmarc-in-investigations
name: verifying-spf-dkim-dmarc-in-investigations
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [dkim-verification, email-header-analysis, email-forensics, phishing-analysis, dfir]
level: advanced
status: docs-checked
description: "Verify SPF, DKIM, DMARC and ARC results in email investigations: what each result proves, re-validating DKIM with the DNS key, and spoofing and integrity limits."
sources: ["https://datatracker.ietf.org/doc/html/rfc6376", "https://datatracker.ietf.org/doc/html/rfc7489", "https://datatracker.ietf.org/doc/html/rfc8617", "https://datatracker.ietf.org/doc/html/rfc7208"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verifying SPF, DKIM, DMARC and ARC in investigations

**Goal:** determine whether a message really came from the domain it claims, and show whether
its signed content was altered, for phishing, BEC and fraud cases.

## Read what the receiving server concluded
Use the authentication results recorded by your own gateway (the top-most ones added by your
own MTA); results lower in the header were added by other parties and may be forged.
- **SPF** (RFC 7208) is about the "MAIL FROM" (envelope) or "HELO" identity of the connecting
  host, not the visible From address.
- **DKIM** (RFC 6376) is a signature that associates the `d=` domain with a hash of some or all
  of the message.
- **DMARC** (RFC 7489) passes when SPF or DKIM passes and the domain aligns with the
  RFC5322.From domain.
- **ARC** (RFC 8617) lets each intermediate handler add its authentication assessment to an
  ordered set, using `ARC-Authentication-Results`, `ARC-Message-Signature` and `ARC-Seal`
  header fields. Use it to see where alteration may have occurred and as extra trace
  information; it does not replace your own checks.

## Re-validate DKIM offline (message integrity)
- Take the `d=` domain and selector from the `DKIM-Signature` header; the public key is a DNS
  TXT record under `<selector>._domainkey.<domain>` (RFC 6376 gives
  `foo.bar._domainkey.example.com` as an example).
- Verify with a DKIM verifier of your choice on the original raw message.
- Verifying a signature asserts that the hashed content has not changed since it was signed,
  and nothing else; RFC 6376 says it does not protect end-to-end integrity. That is useful in
  disputes about altered invoices, but only for the parts the signature covers.
- Selectors let a domain change keys over time, so an old selector may no longer be in DNS;
  historical DNS records may be needed to verify old messages.

## Spoofing patterns
- Lookalike domain with its own valid SPF/DKIM: authentication shows the sender controls that
  domain, not that it is legitimate.
- Display name that claims a person but an unrelated From domain.
- Domain with a DMARC policy of `none`: that policy requests no specific action, so failing
  mail can still be delivered.
- Compromised real mailbox: everything passes and aligns; the investigation moves to the
  sender's tenant.

## Gotchas
- Intermediaries that change a message (the RFC 8617 introduction notes that intermediate
  handlers can cause authentication failures) can break SPF and DKIM; prefer a copy taken
  before any rewriting if one exists.

## Verify
Report states which domain authenticated the message and whether integrity of the signed
content is cryptographically shown.

## Checked
Confirmed in RFC 7208 (MAIL FROM/HELO identities), RFC 6376 (`d=` association, data-integrity
limits, selectors and key change, `_domainkey` TXT binding), RFC 7489 (alignment, `none`
policy meaning) and RFC 8617 (ARC purpose and header fields). Removed as not in these pages:
the sample Authentication-Results line, the `pip install dkimpy` / `dkimverify` commands,
the `dmarc=fail action=none` string, `compauth`, and the claim about internal Exchange mail.
Method: docs-only read of cited pages, 2026-11-08
