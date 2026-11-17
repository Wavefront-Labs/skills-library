---
id: computing-software.digital-privacy-hygiene.phishing-awareness.reading-email-headers-to-spot-spoofing
name: reading-email-headers-to-spot-spoofing
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, email-headers, spf, dkim, dmarc, email-spoofing, reply-to, phishing]
level: practitioner
status: draft
description: "Open full email headers in Gmail, Outlook and Apple Mail and read From/Reply-To/Return-Path and SPF/DKIM/DMARC results to tell spoofed or look-alike mail from real."
sources:
  - "https://support.google.com/mail/answer/29436"
  - "https://toolbox.googleapps.com/apps/messageheader/"
  - "https://www.cisa.gov/news-events/news/avoiding-social-engineering-and-phishing-attacks"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading email headers to spot spoofing

**Goal:** a display name and logo prove nothing. The headers show who actually sent the message and whether the
domain authenticated it.

## Open the headers
- **Gmail** (web): ⋮ menu > **Show original**. The top summary shows SPF, DKIM and DMARC results.
- **Outlook** (web/new Outlook): ... > View > **View message source** (or Message details).
- **Apple Mail**: View > Message > **All Headers** (or Raw Source).
- Paste raw headers into Google Admin Toolbox **Messageheader** or MXToolbox for a parsed view.

## What to read
| Field | Look for |
|---|---|
| `From:` | Actual address behind the display name; look-alike domains (`rnicrosoft.com`, `paypal-support.co`) |
| `Reply-To:` | Different domain from `From:` = replies go to the attacker |
| `Return-Path:` | Envelope sender; mismatch with From is common in mass mail but notable in "personal" mail |
| `Authentication-Results:` | `spf=pass`, `dkim=pass header.d=...`, `dmarc=pass header.from=...` |
| `Received:` | Read bottom-up: first hop shows where it originated (a residential IP or unrelated host for "your bank"?) |
| `Message-ID:` | Domain unrelated to the claimed sender |

## Interpreting authentication
- `dmarc=fail` for a well-known brand's domain: almost certainly spoofed; do not act on it.
- `pass` only proves the mail came from the domain shown; attackers register their own look-alike domains and
  pass everything. Always read the domain itself.
- Mail through forwarding/mailing lists can fail SPF legitimately; DKIM pass with an aligned domain is the stronger signal.

## Then
- Do not click; open the real site from a bookmark. Report with the provider's Report phishing button, or forward
  **as attachment** (keeps headers) to the impersonated company's abuse address.

## Verify
- [ ] You can find Reply-To and Authentication-Results for a message in your own mail client in under a minute.
