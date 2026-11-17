---
id: computing-software.cybersecurity-defensive.network-defence.registry-lock
name: registry-lock
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [registry-lock, domain-hijacking, registrar-security, domain-transfer-lock, dns-hijack, clienttransferprohibited, dns-security]
level: practitioner
status: docs-checked
description: "Protect domains from hijacking: registry lock vs registrar locks, EPP status codes, registrar account hygiene, expiry and NS change monitoring, and recovery steps."
sources: ["https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registry lock and domain hijack protection

Domain hijacking (changing NS records at the registrar) redirects all your web, mail and SSO traffic and
lets attackers obtain valid certificates.

## Lock levels (ICANN EPP status code guide)
| Lock | Set by | What it does |
|---|---|---|
| `clientTransferProhibited`, `clientUpdateProhibited`, `clientDeleteProhibited` | Registrar, on your request | Registry rejects transfer, update or deletion requests. ICANN says asking your registrar for these can help prevent unauthorized transfers, deletions or updates. To make a change you first ask the registrar to remove the status |
| `serverTransferProhibited`, `serverUpdateProhibited`, `serverDeleteProhibited` | Registry Operator; "some Registry Operators offer a Registry Lock Service" that lets registrants, through their registrars, set these as extra protection | Same prohibitions enforced at the registry. Removing them takes longer because the registrar must forward the request to the registry and wait for it to lift the restriction |

The server statuses are also set during legal disputes or redemption periods, so an unexpected server status
may signal an issue to resolve with your registrar. Check your domain's status with WHOIS or RDAP.
Registry lock availability and the verification process depend on the registry operator and registrar:
ask them what is offered for your TLD.

## Registrar account
- Use a registrar that supports strong account protection for important domains rather than a retail account.
- MFA (phishing-resistant where offered), named accounts with roles, IP allow-lists where offered, change notifications to a monitored list.
- Registrant contact emails on a domain you control and that is itself locked.

## Monitoring
- Alert on NS/DS/A/MX record changes for key domains (external DNS monitoring or comparison against IaC), WHOIS status changes, and Certificate Transparency for unexpected certificates.
- Expiry: auto-renew, multi-year registration, and renewal alerts well ahead of expiry.

## Recovery if hijacked
Contact the registrar's abuse or security line, and the registry if needed; revoke certificates issued during
the window; rotate credentials captured via redirected login or mail; use the ICANN transfer dispute policy
for unauthorised transfers.

## Verify
- [ ] Crown-jewel domains show the `server*Prohibited` statuses where your registry offers the service.
- [ ] Registrar accounts on MFA; change alerts tested.

## Checked
Checked 2026-11-09 against the ICANN EPP status codes page (read the ok, client* and server* rows). Removed:
the CISA ED 19-01 statement (CISA is unreadable), the Verisign source (the page returned only the site home
page), named corporate registrars, the 24x7 claim and the 90/60/30 day alert schedule, none of which is
confirmed by a page read.
Method: docs-checked 2026-11-09 against the ICANN EPP status codes page.
