---
id: computing-software.digital-privacy-hygiene.phishing-awareness.fake-password-reset-emails
name: fake-password-reset-emails
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, password-reset-phishing, credential-phishing, push-bombing]
level: practitioner
status: draft
description: "Handle password reset emails and prompts you didn't request: phishing lookalikes, real resets triggered by others, and Apple reset-prompt bombing."
sources:
  - "https://support.apple.com/en-us/102568"
  - "https://www.cisa.gov/secure-our-world/recognize-and-report-phishing"
  - "https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Fake password reset emails

**Goal:** never reset a password from a link you didn't ask for.

## Three situations
| Situation | What it is | Do |
|---|---|---|
| "Your password expires today, click to keep it" | Phishing (credential page) | Delete/report |
| Real reset email you didn't request | Someone typed your email (mistake or attacker testing) | Ignore; don't click; check account security |
| Many reset prompts on your iPhone/Mac ("Reset Password" system dialogs) | Reset-prompt bombing, often followed by a call from fake "Apple Support" | Tap **Don't Allow** every time; never give codes; Apple doesn't call |

## Rules
- Only use reset links within minutes of requesting one yourself.
- To change a password, go to the site directly.
- If real reset emails keep arriving: the attacker knows your email/username. Ensure strong unique password and
  MFA; consider changing the account email to an alias.

## Check a real-looking reset email
Sender domain, link destination (hover), whether you initiated it. Even a genuine-looking one: go direct.

## Gotchas
- Some services email a code instead of a link; never read that code to anyone who calls.
- Corporate "password expiry" phishing mimics Microsoft 365 pages; your IT department uses its own portal.
