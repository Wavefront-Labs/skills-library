---
id: computing-software.digital-privacy-hygiene.two-factor-auth.working-around-weak-bank-mfa
name: working-around-weak-bank-mfa
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, bank-2fa-limitations, mfa-rollout, sms-2fa, banking-app, transaction-alerts, account-alerts, verbal-password, payee-confirmation]
level: practitioner
status: draft
description: "Compensate for banks that only offer SMS or app-push 2FA: use the banking app, transaction alerts, payee limits, verbal passwords and number protection."
sources:
  - "https://consumer.ftc.gov/articles/how-protect-your-phone-and-data-it"
  - "https://www.fcc.gov/sim-swap-port-out-fraud"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Working around weak bank MFA

**Goal:** many banks still offer only SMS codes, or a proprietary app. You can't change
their MFA, but you can make takeover hard to profit from.

## Prefer the bank's app approval over SMS
If the bank offers in-app approvals tied to your enrolled device, use it and disable SMS
where allowed; it's at least not SIM-swappable. Some banks offer hardware tokens or
security keys on request (ask; some do for business or premium accounts).

## Compensating controls
1. **Alerts on everything**: login from new device, password change, new payee, any
   transfer over a small amount, card-not-present transactions. Push + email.
2. **Payee and transfer limits**: lower daily transfer limits; require a cooling-off
   period for new payees where offered.
3. **Verbal password / phone PIN** on the account for phone banking (see
   `computing-software.digital-privacy-hygiene.password-hygiene.verbal-passwords-with-banks-and-carriers`).
4. **Protect the phone number**: carrier port-out PIN, number lock, SIM PIN.
5. **Separate email** for banking login (not public).
6. **Unique strong password** in the manager; bank login URL bookmarked.
7. **Credit freeze** to stop new accounts in your name.

## Know the fraud reimbursement rules
Many jurisdictions protect unauthorised transfers but not authorised push payment scams
where you were tricked into sending money; this is why the scam call is more dangerous
than the hacked password. See
`computing-software.digital-privacy-hygiene.phishing-awareness.bank-fraud-department-impersonation-calls`.

## Verify
- [ ] Alerts configured and tested (make a small transfer, receive alert).
- [ ] New-payee and transfer limits set.
