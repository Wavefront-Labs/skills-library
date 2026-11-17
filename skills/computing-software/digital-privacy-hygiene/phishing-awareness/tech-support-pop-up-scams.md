---
id: computing-software.digital-privacy-hygiene.phishing-awareness.tech-support-pop-up-scams
name: tech-support-pop-up-scams
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, tech-support-scam, scam, browser-locker, fake-virus-alert, fullscreen-popup, remote-access, refund-scam]
level: intro
status: draft
description: "Handle fake 'your computer is infected, call Microsoft' pop-ups and calls: close the browser safely, never call the number, and know the refund-overpayment follow-up."
sources:
  - "https://consumer.ftc.gov/articles/how-spot-avoid-and-report-tech-support-scams"
  - "https://support.microsoft.com/en-us/windows/protect-yourself-from-tech-support-scams-2ebf91bd-f94c-2a8a-e541-f5c800d18435"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tech support pop-up scams

**Goal:** a full-screen browser page with alarms and a phone number is not a virus; it's a
web page. Getting out is easy once you know how.

## Recognise
- Full-screen warning, sometimes with audio, "Windows Defender alert", "Do not shut down",
  a toll-free number; mouse seems stuck. Arrives via malicious ads or typo domains.
- Or a cold call "from Microsoft/Apple/your ISP" about a problem with your computer.
- Microsoft and Apple never put phone numbers in error messages or call you unprompted.

## Escape the pop-up
1. Press **Esc** (exits full screen), then close the tab.
2. If stuck: **Ctrl+Shift+Esc** (Task Manager) > end the browser; macOS
   **Cmd+Option+Esc** > Force Quit.
3. When reopening the browser, **don't restore** the previous session.
4. Optionally run a Defender quick scan; the page itself typically didn't infect anything.

## If someone already called the number
They likely installed remote software and may have charged for "support" or staged a
**refund scam** ("we refunded too much, send back the difference" by gift card/wire after
editing your online banking page). See
`computing-software.digital-privacy-hygiene.phishing-awareness.cleaning-up-after-a-remote-access-scam`.

## Prevention
Ad blocker (uBlock Origin), up-to-date browser, and a sticky note for older relatives:
"Real Microsoft never shows a phone number. Close the browser, call me."

## Verify
- [ ] Household knows Esc / Task Manager escape and the "no phone numbers" rule.
