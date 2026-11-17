---
id: computing-software.web-development.appwrite.appwrite-custom-mfa-factor
name: appwrite-custom-mfa-factor
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, mfa, custom-factor, functions]
level: sme
status: docs-checked
description: "Deliver the second authentication factor over any channel using the custom MFA factor and an Appwrite Function that reads the code."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/custom-mfa/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send MFA codes via WhatsApp, voice, an internal system or another provider Appwrite does not support.

How it works: Appwrite generates and verifies a 6 digit code; your application chooses how the user receives it. A custom challenge sends no email and no SMS, so if you do not deliver the code the user cannot finish.

Flow:
1. Client: after the first factor, create a challenge with the `custom` factor, for example `account.createMFAChallenge({ factor: AuthenticationFactor.Custom })`. The response holds the challenge ID and expiry, never the code.
2. Client: call your function with `createExecution`, passing the challenge ID. Do not call the function domain directly, because only `createExecution` fills the `x-appwrite-user-id` header.
3. Function: read the code using a Server SDK `users.getMFAChallenge({ userId, challengeId })`, taking `userId` from `x-appwrite-user-id`.
4. Function: send the code through your channel, reading the destination (phone number, chat ID, address) from your own data, never from the request body, or an attacker who knows the password can send the code to their own device.
5. Client: complete the challenge with `account.updateMFAChallenge({ challengeId, otp })`, using the code the user typed.

Requirements: a Function or backend, and the `users.read` scope. On a Function, set the scope there; Appwrite supplies a temporary key in the `x-appwrite-key` header, so no permanent key is stored.

Gotcha: never trust a user ID sent by the client; use the header value so Appwrite rejects a challenge that belongs to a different user. Never log the code or return it to the client.

Built-in factors for comparison: email, phone (SMS) and TOTP.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Custom MFA factor (auth/custom-mfa): the use cases, Appwrite generating and verifying a 6-digit code, no delivery by Appwrite, the five-step flow, `createExecution` versus the function domain and the `x-appwrite-user-id` header, the `users.read` scope with the temporary key in `x-appwrite-key`, `getMFAChallenge` with user ID and challenge ID, and the security requirements. Removed: the two-user Verify test, which the page does not describe.
Method: documentation only; no commands were run.
