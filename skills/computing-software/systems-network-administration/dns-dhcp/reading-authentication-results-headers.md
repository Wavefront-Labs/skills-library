---
id: computing-software.systems-network-administration.dns-dhcp.reading-authentication-results-headers
name: reading-authentication-results-headers
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, authentication-results, email-authentication, spf, dkim, dmarc]
level: practitioner
status: verified
description: "Read Authentication-Results and related headers to diagnose SPF, DKIM, DMARC and ARC outcomes, identifying which domain and selector each check used."
sources:
  - https://www.rfc-editor.org/rfc/rfc8601
  - https://www.rfc-editor.org/rfc/rfc7489
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading Authentication-Results headers

The receiving server records its verdicts in `Authentication-Results` (RFC 8601). It is the
fastest way to see why mail landed in spam or was rejected.

## Example
```
Authentication-Results: mx.google.com;
       dkim=pass header.i=@example.com header.s=s2026 header.b=Ab12Cd34;
       spf=pass (google.com: domain of bounce@mail.example.com designates 198.51.100.7 as permitted sender) smtp.mailfrom=bounce@mail.example.com;
       dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=example.com
```
| Part | Meaning |
|------|---------|
| `dkim=pass header.i/d=` | which domain signed; `header.s` selector to check in DNS |
| `spf=... smtp.mailfrom=` | SPF checks the envelope sender domain, not From: |
| `dmarc=... header.from=` | DMARC needs SPF or DKIM pass AND alignment with this domain |
| `dis=` | in Google's comment `(p=REJECT sp=REJECT dis=NONE)`: the policy published and the disposition applied; this is a provider comment, not an RFC 8601 property |
| `compauth=` (Microsoft) | composite authentication result: Microsoft 365 combines SPF, DKIM, DMARC and other parts of the message, using the From: domain; a compauth fail does not by itself mean the message is blocked; `reason=` code |

## Diagnosing
- `spf=pass` and `dkim=pass` but `dmarc=fail`: neither domain aligns with From: (e.g. ESP signs
  with `d=esp.net`). Fix by DKIM signing with your domain or custom return-path.
- `dkim=fail (body hash did not verify)`: message modified in transit (footer, gateway).
- `spf=softfail/neutral`: sending IP not in SPF; check `include:` for that service.
- `dkim=temperror` / `spf=temperror`: likely transient, such as a DNS lookup that could not complete (RFC 8601). An SPF
  record needing more than 10 DNS-querying terms is `spf=permerror` (RFC 7208), which retrying will not fix.
- Multiple Authentication-Results: trust only those added by your own boundary (`authserv-id`);
  others can be forged by senders.

## Related headers
`Received-SPF` (RFC 7208: `pass`, `fail`, `softfail`, `neutral`, `none`, `permerror`, `temperror`),
`ARC-Authentication-Results`, and Microsoft's `X-Forefront-Antispam-Report` (SCL spam confidence level, CAT threat
category such as BULK or HSPM).

## Verify
- [ ] The failing check is identified with the domain/selector involved and confirmed by a DNS lookup.
