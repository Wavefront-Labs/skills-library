---
id: computing-software.general-digital-literacy.email-clients.checking-links-before-clicking
name: checking-links-before-clicking
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-security, hover-links, link-preview, url-checking, phishing]
level: intro
status: draft
description: "Check where an email or message link really goes before clicking: hover or long-press, read the real domain, expand short links, and use URL scanners when unsure."
sources:
  - https://www.ncsc.gov.uk/guidance/suspicious-email-actions
  - https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams
  - https://www.virustotal.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Check links before clicking

## See the real destination
- **Computer:** hover the mouse over the link or button (don't click); the real URL shows bottom-left of the browser or in a tooltip in Outlook/Apple Mail. The visible text ("Click here", "paypal.com/login") can be anything.
- **Phone:** **long-press** the link to show a preview with the URL; tap outside to cancel. Don't let the preview load the page if suspicious (iOS: hide preview).
- Outlook "Safe Links" rewrites URLs to `safelinks.protection.outlook.com/?url=...`; the real address is after `url=`.

## Read the domain correctly
- The domain is the part just before the first single `/`, read **right to left** from there: `https://paypal.com.account-verify.co/login` belongs to `account-verify.co`, not PayPal.
- Look for lookalikes: `rnicrosoft.com` (rn ≠ m), `amaz0n`, `paypa1`, extra words (`-secure`, `-support`), wrong country domains.
- `https` and a padlock only mean encrypted, not genuine.

## Short links and QR codes
- `bit.ly`, `tinyurl`, `t.co`: expand with a preview service (add `+` to a bit.ly link, or use unshorten.me).
- QR codes in emails/letters: phone preview shows the URL; read it before opening.

## When in doubt
- Don't click. Go to the company by typing its address or using its app, and log in there.
- Scan the URL at **VirusTotal** or Google Safe Browsing site status (without visiting it).
- Report the message (Report phishing button / forward to report@phishing.gov.uk or reportphishing@apwg.org).

## Verify
- [ ] For a test email, you can state the exact domain a link leads to before clicking it.
