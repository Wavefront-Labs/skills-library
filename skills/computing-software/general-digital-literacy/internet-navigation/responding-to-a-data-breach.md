---
id: computing-software.general-digital-literacy.internet-navigation.responding-to-a-data-breach
name: responding-to-a-data-breach
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, online-privacy, data-breach-response, breach-notification, have-i-been-pwned, password-reuse, credit-freeze, breach-phishing]
level: intro
status: docs-checked
description: "Respond to a data breach notice or Have I Been Pwned alert: what to change, which accounts to check, watching for follow-up phishing and protecting your credit."
sources:
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online
  - https://ico.org.uk/for-the-public/
  - https://consumer.ftc.gov/features/scam-alerts
  - https://haveibeenpwned.com/NotifyMe
  - https://consumer.ftc.gov/articles/credit-freezes-and-fraud-alerts
  - https://www.cifas.org.uk/pr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responding to a data breach notice

**Goal:** close the doors a breach opened before criminals use them.

## Find out what leaked
- Read the company's notice: email address only, passwords (hashed or not), phone, address, date of
  birth, payment cards, ID documents?
- Check **haveibeenpwned.com** for your email address and sign up for its free breach notifications. Many password managers also notify you if a password is found in a data breach (NCSC).

## Act by data type
| Leaked | Do |
|---|---|
| Password | change it on that site **and every site using the same password**; turn on 2-step |
| Email + personal details | expect targeted phishing that quotes real details; don't trust it |
| Phone number | watch for scam texts; set a PIN or password on your carrier account (FTC SIM-swap advice) |
| Card number | cancel/replace the card; check statements |
| Date of birth, address, ID / SSN / NI number | US: freeze your credit with all three bureaus (Equifax, Experian, TransUnion); the FTC says freezes are free and do not affect your score. UK: check your credit report and consider Cifas Protective Registration |

## Watch out
- Fake breach emails ("your account was in a breach, verify here") are a scam of their own; go to the
  company's site yourself.
- Breached companies often offer free credit monitoring; enrol through their official notice.
- You can complain to the regulator (UK ICO, EU national DPA) if the company handled it badly.

## Verify
- [ ] Breached passwords changed everywhere they were reused; 2-step on key accounts.

## Checked

Checked 2026-10-27 against FTC credit freeze guidance, Have I Been Pwned Notify Me, the Cifas Protective Registration page and NCSC password manager guidance. Confirmed: free freezes at Equifax, Experian and TransUnion that do not affect credit scores, Cifas Protective Registration exists, HIBP free notifications, managers can flag breached passwords.

Method: documentation only; no commands were run.
