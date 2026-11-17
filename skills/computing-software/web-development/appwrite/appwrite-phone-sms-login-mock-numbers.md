---
id: computing-software.web-development.appwrite.appwrite-phone-sms-login-mock-numbers
name: appwrite-phone-sms-login-mock-numbers
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, phone, sms, otp, mock-phones, testing]
level: practitioner
status: docs-checked
description: "Log users in by SMS code and use project mock phone numbers to exercise phone auth in CI or store review without sending real SMS."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/phone-sms/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/partners/project/mock-phones/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: SMS-based login plus deterministic test numbers.

Flow:
1. `const token = await account.createPhoneToken({ userId: ID.unique(), phone: '+14255550123' })`; keep `token.userId`.
2. If the number is new an account is created with that `userId`; if it already exists the ID is ignored and an SMS code is sent.
3. Finish with `account.createSession({ userId, secret: '<CODE>' })`. The secret is usually a 6 digit number.

Cost note from the docs: OTPs are billed per message and rates vary by country (see the phone OTP rates page).

Mock phones: register fictional numbers with a fixed six digit code at project level so testers can sign in without an SMS. Numbers must be E.164 (for example `+15555550100`); use fictional ranges such as `555` numbers. Add them in Console > Auth > Settings > Mock phone numbers (click Save on the row, then Update at the bottom), or with the Server SDK Project service: `createMockPhone({ number, otp })`, `listMockPhones`, `getMockPhone`, `updateMockPhone`, `deleteMockPhone`. Reads need the `mocks.read` scope, writes `mocks.write`.

Gotcha: click Update at the bottom of the settings to persist mock numbers.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/auth/phone-sms, partners/project/mock-phones. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the invented Verify step; Gotcha reworded to the page (click Update at the bottom to persist); added createMockPhone({ number, otp }).

Method: documentation only; no commands were run.
