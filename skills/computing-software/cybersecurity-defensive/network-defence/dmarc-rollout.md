---
id: computing-software.cybersecurity-defensive.network-defence.dmarc-rollout
name: dmarc-rollout
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [email-security, dmarc, dmarc-reporting, rua, p-reject, alignment, bimi, email-spoofing, bulk-sender-requirements]
level: practitioner
status: docs-checked
description: "Roll DMARC from p=none to p=reject using aggregate reports: find all senders, fix SPF/DKIM alignment, step up policy safely and meet bulk-sender rules."
sources: ["https://datatracker.ietf.org/doc/html/rfc7489", "https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dmarc-configure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMARC rollout

**Goal:** reach `p=reject` so attackers cannot send email that displays your domain in the
From address, without blocking your own legitimate mail.

## Steps
1. **Monitor**: publish
```
_dmarc.example.com. TXT "v=DMARC1; p=none; rua=mailto:dmarc-rua@example.com"
```
   Send `rua` to a DMARC report processor; raw XML aggregate reports are hard to read at scale.
2. **Inventory senders** from reports: for each source IP/service, check SPF and DKIM pass **and alignment** with the From domain.
3. **Fix** each legitimate source: custom DKIM with your domain, SPF include or a subdomain, or route through your main mail platform. Decommission unknown senders.
4. **Quarantine** gradually using the `pct` tag (RFC 7489), raising it step by step to 100.
5. **Reject**: move to `p=reject`.
6. Keep monitoring; new SaaS tools appear constantly.

## Alignment
- Relaxed (default): organisational domains match (`mail.example.com` aligns with `example.com`).
- Strict: exact match; rarely needed.
DMARC passes if **either** SPF or DKIM passes **and** is aligned.

## Gotchas
- Forwarded mail and mailing lists fail SPF; DKIM must be in place before reject.
- Lookalike domains (example-support.com) are not stopped by DMARC: monitor them separately.
- Failure (forensic) reports can contain message content; mind privacy.

## Verify
- [ ] Aggregate reports show all legitimate volume passing DMARC before moving to reject.
- [ ] The `_dmarc` TXT record shows `p=reject`.

## Checked

2026-10-28. Confirmed against: RFC 7489 (pct, aggregate and failure reports, alignment modes, SPF-or-DKIM pass rule); Microsoft Learn 'Use DMARC to validate email' (rollout policies).

Removed as unconfirmed: Google/Yahoo bulk-sender thresholds, BIMI, DMARCbis note, fo and sp tags, 99% figure, report-processor product list, CISA BOD 18-01 citation.

Method: documentation only; no commands were run.
