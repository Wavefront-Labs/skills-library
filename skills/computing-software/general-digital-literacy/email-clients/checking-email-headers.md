---
id: computing-software.general-digital-literacy.email-clients.checking-email-headers
name: checking-email-headers
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-security, email-headers, show-original, message-source, spf-dkim-dmarc, received-headers, authentication-results]
level: intro
status: docs-checked
description: "View full email headers in Gmail, Apple Mail and classic Outlook and read Received, Return-Path and Authentication-Results to judge a suspicious email."
sources:
  - https://support.google.com/mail/answer/29436
  - https://www.rfc-editor.org/rfc/rfc5321.txt
  - https://www.rfc-editor.org/rfc/rfc8601.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Checking the real sender in message headers

**Goal:** see where an email really came from when the visible sender is in doubt.

## Open the headers
- **Gmail (browser):** open the message > next to Reply click **More** > **Show original** > **Copy to clipboard**. "Created at" there shows the delivery time.
- **Apple Mail:** open the message > View > Message > **All Headers**.
- **Classic Outlook:** open the message > File > Properties; headers appear in the Internet headers box.
- Google's Admin Toolbox Messageheader can analyse a pasted header; headers contain addresses and IP data, so do not post them publicly.

## What to read
| Header | Meaning |
|---|---|
| `From:` | Displayed sender; easy to fake |
| `Return-Path:` | Where bounces go; the receiving server inserts it from the envelope sender (RFC 5321) |
| `Received:` | Each SMTP server inserts one at the beginning of the message, so the oldest hop is at the bottom: read bottom-up (RFC 5321 section 4.4) |
| `Authentication-Results:` | Verdicts such as `spf=pass`, `dkim=pass header.d=example.com` (RFC 8601 examples) |

## Interpreting
- A pass means the domain's own checks succeeded, not that the content is safe.
- A fail for a bank or big brand's domain, or a DKIM signing domain unrelated to the From domain, is a warning sign.
- Check that the sender name and address match, and hover links to see that the URL matches its description (Gmail's phishing guidance).

## Verify
- [ ] For a known-good email from your bank, you can find the pass results and the bank's domain.

## Checked
2026-10-27. Google Gmail Help "Trace an email with its full header" and "Avoid and report phishing emails"; RFC 5321 section 4.4 and RFC 8601 examples. Confirmed the open-header paths, bottom-up reading and the Authentication-Results syntax. Removed unconfirmed Gmail PASS/FAIL summary, new Outlook menu, Apple keyboard shortcut and DMARC interpretation claims.
Method: documentation only; no commands were run.
