---
id: computing-software.digital-privacy-hygiene.vpn-tools.custom-domain-email-ownership
name: custom-domain-email-ownership
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, custom-domain-email, domain-renewal-risk, primary-email-security, registrar-lock, auto-renew, mx-records, spf, dkim, dmarc, email-privacy, whois-privacy]
level: practitioner
status: draft
description: "Run personal email on your own domain for provider portability, and protect the domain itself: registrar 2FA, auto-renew, transfer lock, DNS records and WHOIS privacy."
sources:
  - "https://www.privacyguides.org/en/email/"
  - "https://www.icann.org/resources/pages/expired-2013-05-03-en"
  - "https://www.cloudflare.com/learning/dns/dns-records/dns-dmarc-record/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom domain email ownership

**Goal:** `you@yourname.tld` lets you change email providers without changing every
account. But whoever controls the domain controls every password reset; a lapsed domain
is an account-takeover jackpot for whoever re-registers it.

## Set up
1. Register the domain at a reputable registrar (not a free bundle tied to a host).
2. Point MX records to your mail provider; add the provider's **SPF**, **DKIM** and a
   **DMARC** record (start `p=none` with reporting, move to `quarantine`/`reject`).
3. Optional catch-all or aliases for per-site addresses.

## Protect the domain (the important part)
- Registrar account: unique password + **security key / TOTP**; registrar email must not
  be an address on the same domain (circular: if the domain lapses, you can't receive
  the renewal emails).
- **Auto-renew on**, card on file valid; renew for **multiple years**; calendar reminder
  60 days before expiry and before the card's expiry date.
- **Transfer lock** (clientTransferProhibited) on; registry lock for very high-value domains.
- **WHOIS privacy** (redaction) on to keep your home address out of public records.
- Note the domain in your digital legacy plan; heirs need to renew it.

## If it lapses
Registrars typically have a grace period then a redemption period (fees rise) before
the domain is released. Act immediately; after release anyone can register it.

## Verify
- [ ] `dig MX yourname.tld`, SPF, DKIM and DMARC records resolve; test mail passes DMARC.
- [ ] Registrar shows auto-renew on, transfer lock on, expiry > 1 year away.
