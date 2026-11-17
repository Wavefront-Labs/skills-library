---
id: computing-software.digital-privacy-hygiene.phishing-awareness.spotting-and-handling-phishing
name: spotting-and-handling-phishing
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, phishing, spear-phishing, smishing, vishing, quishing, qr-code-phishing, lookalike-domains, punycode, homograph-attack, display-name-spoofing, link-inspection, malicious-attachments, html-attachments, macros, deepfake-voice, ai-voice-scam, mfa-fatigue, aitm, adversary-in-the-middle, session-hijacking, passkeys, report-phishing, 7726, apwg, business-email-compromise, scam]
level: intro
status: draft
description: "Spot phishing in email, SMS, QR codes and calls: red flags, reading a link's real domain, risky attachments, AI voice scams, MFA fatigue, and what to do if you clicked."
sources:
  - "https://www.ncsc.gov.uk/collection/phishing-scams"
  - "https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams"
  - "https://apwg.org/reportphishing/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spotting and handling phishing

**Goal:** recognise a lure in any channel within seconds, verify without using
anything the message gave you, and contain the damage fast if you did bite. Basic
email checks are in `computing-software.general-digital-literacy.email-clients.managing-email-and-calendar`;
this goes further.

## 1. Red flags
- **Urgency or fear**: "account suspended in 24 hours", unpaid toll/parcel fee,
  "unusual sign-in", a boss needing gift cards *now*.
- **A request that changes money or access**: new bank details, a login, a code, remote access.
- **Sender mismatch**: the display name says "PayPal" but the address is something
  else (display-name spoofing). On phones tap the name to reveal the address.
- **Lookalike domains**: `rnicrosoft`, `micros0ft`, `microsoft-support.help`, extra
  words, odd endings. **Punycode** domains (`xn--...`) can render with letters from
  other alphabets that look identical to Latin ones.
- Generic greeting, unexpected attachment, or a "shared document" you weren't expecting.
Good spelling and your real name prove nothing — AI writes clean, personalised lures.

## 2. Read a link's real domain
1. Hover (desktop) or long-press (phone) to preview; don't tap.
2. Take the part after `://` up to the **first single `/`** — that's the host name.
3. Read it **right to left**: the last two labels (three for `co.uk`-style endings)
   are the domain that owns it.
   - `https://paypal.com.secure-login.example/account` → owner is `secure-login.example`.
   - `https://login.paypal.com/` → owner is `paypal.com`.
4. Anything before an `@` in the host is ignored by browsers; shorteners hide the
   destination entirely. When unsure, don't click — type the known address yourself.

## 3. Attachments
- Office files asking you to **"Enable Content / Enable Macros"** — close them.
- **`.html`/`.htm`/`.svg`** attachments that open a login page are credential traps.
- **`.iso`, `.img`, `.zip`/`.7z` (especially password-protected), `.lnk`, `.js`,
  `.one`** — common malware containers. Real invoices are rarely any of these.
- Unexpected files from known contacts may come from a hijacked account; check first.

## 4. Other channels
- **QR codes** (quishing): stickers on parking meters, letters, emails with a QR to
  "re-verify". Preview the URL before opening; pay via the official app instead.
- **SMS (smishing)**: toll, parcel, tax refund, bank "fraud alert". Never use links
  or numbers in the text.
- **Voice (vishing) and AI voice clones**: a few seconds of audio can clone a voice.
  Hang up and call back on a number you already have; agree a family **code word**
  for emergencies. Caller ID can be spoofed.
- **MFA fatigue**: repeated sign-in prompts you didn't start mean your password is
  known. Deny, then change it.
- **Adversary-in-the-middle proxies** relay a real login page, capturing your
  password, the TOTP code *and* the session cookie. Only **passkeys/security keys**
  reliably resist this, because they won't sign in for the wrong domain (see
  `computing-software.digital-privacy-hygiene.two-factor-auth.setting-up-mfa-and-backup-methods`).
  A password manager that refuses to autofill is the same warning.

## 5. Verify independently
Contact the organisation or person through a channel **you** supply: the app, a
bookmarked site, the number on your card or a previous invoice, or a separate message
to the colleague. Never through the reply button, link or number in the message.

## 6. If you clicked
- **Clicked but entered nothing**: close the tab; risk is usually low. Keep the
  browser and OS updated.
- **Entered a password**: from a trusted device, go to the site directly, change the
  password (and anywhere it was reused), **sign out all sessions**, check MFA methods,
  recovery details and mail forwarding rules
  (`computing-software.digital-privacy-hygiene.password-hygiene.account-security-audit-and-breach-response`).
- **Opened a file or installed something**: disconnect from the network (Wi-Fi off /
  unplug), run a full antivirus scan, and change passwords from *another* device.
  If in doubt, restore or reset the device.
- **Gave card or bank details**: call the bank on the number on your card now.
- **Work device or account**: report to IT immediately — speed matters more than embarrassment.

## 7. Report it
- Email: the client's **Report phishing** / Report button (Gmail ⋮ menu, Outlook).
- **SMS**: forward the text to **7726** (free in the US and UK, and some other countries).
- US: reportphishing@apwg.org and ReportFraud.ftc.gov; UK: report@phishing.gov.uk
  (NCSC). Other countries have their own centres — I'm not certain of each one's address.
Then delete the message.

## Gotchas
- The padlock means an encrypted connection, not a legitimate site — phishing sites
  have HTTPS too.
- Real support doesn't ask you to read a code aloud or install remote-access tools.

## Verify
- [ ] You can extract the owning domain from any URL right-to-left.
- [ ] You know which attachment types you never open unsolicited.
- [ ] Family/colleagues share a callback rule or code word.
- [ ] You know the report button in your mail app and the 7726 forward.
- [ ] You can list the four steps after entering a password on a phishing page.
