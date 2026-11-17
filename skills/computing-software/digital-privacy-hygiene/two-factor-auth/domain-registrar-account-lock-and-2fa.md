---
id: computing-software.digital-privacy-hygiene.two-factor-auth.domain-registrar-account-lock-and-2fa
name: domain-registrar-account-lock-and-2fa
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, registrar-2fa, domain-renewal-risk, custom-domain-email]
level: practitioner
status: draft
description: "Protect a domain at the registrar: strong 2FA, transfer and registry lock, auto-renew, and a contact email that doesn't depend on the domain itself."
sources:
  - "https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en"
  - "https://www.cloudflare.com/learning/dns/what-is-domain-lock/"
  - "https://www.cisa.gov/news-events/directives/ed-19-01-mitigate-dns-infrastructure-tampering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Domain registrar account lock and 2FA

**Goal:** nobody can hijack your domain (and therefore your email and every password reset) through the
registrar.

## Account
- Security key or passkey 2FA; no SMS.
- Account email on a **different** domain (e.g. a Gmail/Proton address). If the account email is on the domain
  and the domain lapses or is hijacked, you can't receive recovery mail.
- Remove old team members/API keys.

## Domain settings
| Control | What it does |
|---|---|
| Registrar lock (`clientTransferProhibited`) | Blocks transfer away; on by default at most registrars; keep on |
| Registry lock (`serverTransferProhibited` etc.) | Registry-level, changes need manual out-of-band verification; offered for premium/business domains |
| Auto-renew + valid card | Prevents expiry; renew multiple years |
| WHOIS privacy | Hides personal contact data |
| DNSSEC | Protects DNS answers from spoofing (enable if your DNS host supports it) |

## Check status
```
whois example.com | grep -i status
```
Look for `clientTransferProhibited`.

## Monitoring
- Alerts on DNS changes at the DNS host.
- Expiry reminders to two email addresses.

## Gotchas
- Transfer auth codes (EPP codes) are as good as a password; never send by email to "support".
- Some registrars still allow phone support to change account email; set a support PIN.
