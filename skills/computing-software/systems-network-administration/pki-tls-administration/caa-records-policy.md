---
id: computing-software.systems-network-administration.pki-tls-administration.caa-records-policy
name: caa-records-policy
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [caa-records-policy, pki-caa, caa, dns-caa, rfc8659, issue-tag, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Publish CAA records to restrict which CAs may issue for a domain, with account and method binding."
sources:
  - https://www.rfc-editor.org/rfc/rfc8659
  - https://letsencrypt.org/docs/caa/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CAA records for issuance control
Goal: only your chosen CAs can issue for the domain.
```
example.org  CAA 0 issue "letsencrypt.org;accounturi=https://acme-v02.api.letsencrypt.org/acme/acct/<ACCOUNT_ID>"
example.org  CAA 0 issue "myca.org;validationmethods=dns-01"
example.org  CAA 0 issuewild ";"
example.org  CAA 0 iodef "mailto:security@example.org"
```
- Presentation format is `CAA <flags> <tag> <value>`. Flags is an integer 0 to 255; use 0, or 128 for the critical bit.
- A CA must check for a Relevant RRset before issuing and must not issue if the request conflicts with it. The lookup starts at the name and climbs towards the root until a CAA RRset is found; the closest one wins (RFC 8659 section 3, Let's Encrypt page). An RRset with only `iodef` or unrecognised tags does not restrict issuance.
- `issue` values are a CA identifying domain name plus optional semicolon-separated parameters. Multiple records of the same tag are additive.
- `issue ";"` (no issuer name) requests no issuance by anyone; a value that does not match the grammar is treated the same way.
- Parameter meanings are defined by each CA. Let's Encrypt documents `validationmethods` (`http-01`, `dns-01`, `tls-alpn-01`) and `accounturi` (your ACME account URI, so a party who hijacks the domain without your account key cannot issue). Its CAA identifier is `letsencrypt.org`.
- `iodef` takes a `mailto:` or `http(s):` URL for violation reports.
- Critical flag (128): a CA must not issue if the RRset contains a critical property it does not understand.
- DNSSEC for CAA records is strongly recommended, not required (RFC 8659 section 5.1).
- Your DNS provider only needs to answer NOERROR for unknown query types; NOTIMP or dropped queries cause CAA errors for CAs (Let's Encrypt page).
Gotcha: CAA does not stop mis-issue by a CA you authorised (RFC 8659 section 5.3); it reduces risk only if CAs honour it.
Gotcha: because the closest RRset wins, a record set at a subdomain replaces the parent's for that name and below.
Verify:
- [ ] A CAA query for the name returns the expected set from your authoritative servers.
- [ ] Issuance from an unlisted CA is refused.

## Checked
Confirmed 2026-11-08 against RFC 8659 (sections 3, 4.1 to 4.5, 5, 6) and the Let's Encrypt CAA documentation (placement, parameters, errors). Removed: the "BR 3.2.2.8" citation, the RFC 8657 citation (RFC 8657 itself was not fetched; the parameters are taken from the Let's Encrypt page), the `dig` commands, and "forgotten entry blocks a new CA on migration" (not stated). The `<ACCOUNT_ID>` and `myca.org` values are placeholders.
Method: docs-only read of cited pages, 2026-11-08
