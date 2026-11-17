---
id: computing-software.cybersecurity-defensive.network-defence.parked-domains
name: parked-domains
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [parked-domains, non-sending-domains, null-spf, dmarc-reject, null-mx, domain-spoofing, email-security]
level: practitioner
status: docs-checked
description: "Protect parked and non-sending domains from spoofing: null SPF, DMARC p=reject with rua, null MX, wildcard DKIM revocation, and covering subdomains and lookalikes."
sources: ["https://www.gov.uk/guidance/protect-domains-that-dont-send-email", "https://datatracker.ietf.org/doc/html/rfc7505", "https://datatracker.ietf.org/doc/html/rfc7489"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protecting parked domains

Domains that never send email are easy to spoof because nobody published policy for them. Publish
records saying "no mail comes from here".

## Records for each non-sending domain
```
example-parked.com.            TXT   "v=spf1 -all"
_dmarc.example-parked.com.     TXT   "v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s; rua=mailto:dmarc@reports.example.com"
*._domainkey.example-parked.com. TXT "v=DKIM1; p="
example-parked.com.            MX    0 .          ; null MX (RFC 7505) - accepts no mail
```
- `sp=reject` sets the policy for subdomains; the GOV.UK guidance also publishes `v=spf1 -all` on subdomains. If a subdomain does send mail, GOV.UK says to use `sp=none` and give that subdomain its own SPF and DMARC records.
- The `*._domainkey` record revokes DKIM selectors: also revoke any existing selectors in both TXT and CNAME records.
- For the external reporting address on another domain, the report destination domain must publish a `example-parked.com._report._dmarc.reports.example.com TXT "v=DMARC1"` authorisation record.

## Programme
- Inventory all registered domains (registrar exports), including defensive registrations and acquired brands.
- Apply the template via IaC (DNS provider Terraform) so new domains get it automatically.
- Monitor DMARC aggregate reports: any volume on a parked domain is spoofing.

## Gotchas
- Some "non-sending" domains turn out to send (old marketing tools, ticketing systems); DMARC reports in p=none for a short period reveal them - but for truly unused domains go straight to reject.
- Some DNS providers do not support a null MX record (GOV.UK says not to worry if you cannot create it).
- RFC 7505: a domain with a null MX must not publish any other MX record, and mail systems should not publish a null MX for domains they use in MailFrom or From addresses, or their mail risks rejection. Fine for parked domains only.

## Verify
- [ ] `dig TXT _dmarc.example-parked.com` shows p=reject for every parked domain.
- [ ] Spoof test from an external server is rejected by major receivers (check DMARC reports).

## Checked
Checked 2026-11-09 against the GOV.UK page "Protect domains that do not send email" (the four records and their values, subdomain advice, null MX note), RFC 7505 (null MX syntax and section 4 effects) and RFC 7489 (`_report._dmarc` external reporting authorisation, `adkim` and `aspf` tags). Removed: the M3AAWG PDF source (not read as text), and the wildcard-TXT-for-SPF suggestion and the "prevents bounce handling" wording, which the sources do not state.
Method: docs-checked 2026-11-09 against the GOV.UK guidance, RFC 7505 and RFC 7489.
