---
id: computing-software.systems-network-administration.dns-dhcp.parked-domain-email-protection
name: parked-domain-email-protection
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, parked-domain, spf, dmarc, null-mx, domain-security]
level: practitioner
status: docs-checked
description: "Lock down parked and non-sending domains against spoofing with SPF -all, DMARC reject, null MX and an empty DKIM record."
sources:
  - https://www.gov.uk/guidance/protect-domains-that-dont-send-email
  - https://www.rfc-editor.org/rfc/rfc7505
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parked domain protection

Domains that never send mail (defensive registrations, legacy domains, or domains that used to send mail) can be used for spoofing and phishing if left unprotected. You only need access to DNS to fix this. The UK government guidance asks for four records.

## Records to publish
```
example-parked.com.              IN TXT  "v=spf1 -all"
_dmarc.example-parked.com.       IN TXT  "v=DMARC1;p=reject;sp=reject;adkim=s;aspf=s;fo=1;rua=mailto:dmarc@example.com"
example-parked.com.              IN MX   0 .
*._domainkey.example-parked.com. IN TXT  "v=DKIM1; p="
```
- SPF: `v=spf1 -all` says there are no sending servers. The guidance shows the same record on subdomains too.
- DMARC: reject with `sp=reject` for subdomains, strict alignment, and `rua` pointing at a mailbox you read for reports. Replace the address with your own.
- DKIM: an empty wildcard key record (`*._domainkey` with `v=DKIM1; p=`) makes servers more likely to reject mail. Also revoke all existing DKIM selectors, in both TXT and CNAME records. A wildcard cannot be checked with a lookup; look in the DNS host's admin panel.
- Null MX: priority 0 and target `.` (RFC 7505) says the domain accepts no mail. Some DNS providers cannot create it; that is acceptable.
- A parent domain that sends no mail may have subdomains that do send. To protect those, use `sp=none` instead of `sp=reject` and give each sending subdomain its own SPF, DMARC and other anti-spoofing records.
- The records can be changed later if you decide to send mail from the domain. The UK NCSC Mail Check service can verify the configuration.

## Verify
- [ ] `dig TXT`, `dig MX` and `dig TXT _dmarc.` on the domain show the records above.

## Checked
Method: docs-checked 2026-11-09 against the GOV.UK guidance "Protect domains that do not send email" (read in full) and RFC 7505 (title and abstract, the null MX definition). The M3AAWG PDF was not read and is dropped. Removed the wildcard SPF and MX records, the cross-domain report authorisation record, the CAA suggestion and operations advice as not confirmed by those pages.
