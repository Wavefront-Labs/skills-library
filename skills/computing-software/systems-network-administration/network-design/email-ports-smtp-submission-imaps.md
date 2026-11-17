---
id: computing-software.systems-network-administration.network-design.email-ports-smtp-submission-imaps
name: email-ports-smtp-submission-imaps
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, email-ports, smtp, submission, imaps, pop3s, starttls, port-25-blocking]
level: practitioner
status: docs-checked
description: "Choose and open the right email ports: SMTP relay 25, submission 587/465, IMAPS/POP3S, STARTTLS vs implicit TLS, ISP port-25 blocks and how to test each."
sources:
  - https://www.rfc-editor.org/rfc/rfc8314
  - https://www.rfc-editor.org/rfc/rfc6409
  - https://www.rfc-editor.org/rfc/rfc5321
  - https://www.rfc-editor.org/rfc/rfc3207
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Email ports

| Port | Use | TLS |
|---|---|---|
| 25 | server-to-server relay (MTA to MTA) | opportunistic STARTTLS |
| 587 | client submission (RFC 6409), authenticated | STARTTLS |
| 465 | submission with implicit TLS (RFC 8314 re-standardised it, preferred) | implicit |
| 143 / 993 | IMAP / IMAPS | STARTTLS / implicit |
| 110 / 995 | POP3 / POP3S | STARTTLS / implicit |

RFC 8314: prefer implicit TLS (465, 993, 995) for client access over STARTTLS on 587, 143 and 110.

## Design rules
- Inbound from the internet to your MX: 25 only. Clients never submit on 25.
- Outbound 25 from client VLANs: block. Only mail servers/relays may send on 25 (stops spambots
  and data exfiltration). Some ISPs and cloud providers restrict outbound 25: check the provider's
  policy and use an authenticated relay on 587 if needed.
- Applications/printers sending mail: authenticated submission on 587/465 to a relay, or a
  connector restricted by source IP.

## Testing
```
openssl s_client -connect mail.example.com:465 -quiet
openssl s_client -starttls smtp -connect mail.example.com:587
openssl s_client -connect imap.example.com:993
swaks --to user@example.com --server mail.example.com:587 --tls --auth LOGIN
nc -vz mx.example.com 25
```
Check the certificate name matches the hostname clients use, and that `EHLO` on 587 advertises
`AUTH` only after `STARTTLS`.

## Verify
- [ ] Port scan from outside shows only 25/465/587/993 (as designed); outbound 25 blocked from user VLANs; test messages pass with TLS in headers.

## Checked
2026-10-28. Confirmed against RFC 8314 (Implicit TLS preferred; POP 995, IMAP 993, submission 465; STARTTLS on 587 still widely deployed), RFC 6409 (submission on 587), RFC 5321 (SMTP relay on 25) and RFC 3207 (SMTP STARTTLS). Removed: ManageSieve port 4190 (RFC not cited) and the claim that all major clouds block outbound 25.
Method: documentation only; no commands were run.
