---
id: computing-software.web-development.appwrite.appwrite-mfa-totp-email-phone
name: appwrite-mfa-totp-email-phone
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, mfa, totp, recovery-codes]
level: advanced
status: docs-checked
description: "Add multi-factor authentication for end users with recovery codes, email, phone or TOTP factors and a challenge step at login."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/mfa/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enforce a second factor for your app users (not Console accounts, which have their own MFA page). The built-in factors are email, phone (SMS), TOTP and recovery codes; a custom factor sends the code through your own channel (see the custom MFA docs).

Enrollment order:
1. Show recovery codes before enabling MFA: `account.createMfaRecoveryCodes()` returns `recoveryCodes`. They are single-use passwords for when the user loses their MFA email, phone or authenticator app, and can only be generated once, so warn users to store them in a secure place.
2. Add a factor. Email: `account.updateEmail`, then `createVerification` and `updateVerification`. Phone: `account.updatePhone`, then `createPhoneVerification` and `updatePhoneVerification`. TOTP: `account.createMfaAuthenticator({ type: 'totp' })` returns a `secret` and `uri`; render the QR with `avatars.getQR({ text: uri })` (optional `size`, `margin`, `download`; show the `secret` if the user cannot scan), then confirm with `account.updateMfaAuthenticator({ type: 'totp', otp })`.
3. Turn it on with `account.updateMFA({ enabled: true })`. MFA is enforced only once more than one factor of authentication has been added to the account.

Login:
1. Sign in with your default method (for example `account.createEmailPasswordSession`), then call `account.get()`. If more factors are required you receive the error `user_more_factors_required` (`error.type`); redirect the user to the MFA challenge.
2. List options with `account.listMfaFactors()`, which returns booleans such as `{ totp: true, email: false, phone: true }`.
3. Create a challenge with `account.createMfaChallenge({ factor })` using `email`, `phone`, `totp` or `recoverycode` (the page also shows a custom factor), save the challenge ID (`challenge.$id`), then complete it with `account.updateMfaChallenge({ challengeId, otp })` (for recovery, the `otp` is a recovery code). The email factor is not valid as a second factor if the user logged in with email OTP, and the phone factor cannot be used if they logged in with phone OTP.

Gotcha: every email or phone must be verified before it can act as a factor. On mobile, email verification links need a deep link to handle `userId` and `secret`.

After completing the challenge the user is authenticated; the page suggests confirming with `account.get()`.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Multi-factor authentication (auth/mfa), read from the raw markdown because the rendered page was truncated: recovery codes, email, phone and TOTP enrolment calls, `updateMFA`, the `user_more_factors_required` check, `listMfaFactors`, challenge creation and completion per factor, and recovery. Added the OTP-login restrictions from the page. Removed: the unqualified "Verify" claim that `get()` stops throwing (reworded to the page's suggestion).
Method: documentation only; no commands were run.
