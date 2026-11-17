---
id: computing-software.digital-privacy-hygiene.phishing-awareness.bank-fraud-department-impersonation-calls
name: bank-fraud-department-impersonation-calls
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, bank-impersonation-call, callback-verification, vishing, caller-id-spoofing, safe-account-scam, authorised-push-payment, otp-relay-scam, smishing]
level: intro
status: draft
description: "Defeat 'this is your bank's fraud team' calls: spot the script (safe account, read me the code, buy gold), hang up, and call back on the number from your card."
sources:
  - "https://consumer.ftc.gov/articles/how-avoid-bank-impersonation-scams"
  - "https://www.cisa.gov/secure-our-world/recognize-and-report-phishing"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bank fraud department impersonation calls

**Goal:** the most costly scam for many households: a caller (often after a "fraud alert"
text) convinces you to move money yourself, which banks often won't reimburse.

## The script
1. Text: "Did you attempt a $1,240 purchase at ...? Reply YES or NO." You reply; minutes
   later a call from a number that **shows your bank's name** (caller ID spoofing).
2. Caller knows your name, last card digits, recent transactions (from breaches or
   phished logins). They sound professional and urgent.
3. The ask, one of:
   - "Your account is compromised; move money to a **safe account**" (theirs).
   - "Read me the code we just sent to verify you" (it authorises their login/payment).
   - "Withdraw cash/buy gold; a courier will collect it for safekeeping."
   - "Install this app so we can secure your device" (remote access).
   - "Don't tell branch staff; they may be involved."

## The callback rule
**Hang up and call the number on the back of your card** (or typed from the bank's site),
ideally from a different phone; scammers can keep a landline open after you hang up.
Real fraud teams never ask you to move money to protect it, read codes, or hand cash to
couriers.

## Teach the household
- Your bank will never ask for your PIN, password, or a one-time code.
- "Safe account" = scam, every time.
- Pressure and secrecy are the tells.

## If money was sent
Call the bank's fraud line immediately and ask for a payment recall (see
`computing-software.digital-privacy-hygiene.phishing-awareness.recalling-a-scam-payment`).

## Verify
- [ ] Bank's real fraud number saved in contacts from the card/back of statement.
- [ ] Family members can recite the callback rule.
