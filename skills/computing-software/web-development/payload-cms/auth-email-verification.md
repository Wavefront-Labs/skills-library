---
id: computing-software.web-development.payload-cms.auth-email-verification
name: auth-email-verification
category: computing-software
field: web-development
product: payload-cms
tags: [email-verification, verify-email, forgot-password, generateemailhtml]
level: practitioner
status: docs-checked
description: "Require email verification with auth.verify and customise verification and forgot-password emails with generateEmailHTML and generateEmailSubject."
sources:
  - https://payloadcms.com/docs/authentication/email
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Email verification and forgot password

Goal: confirm email ownership and customise the emails sent.

```ts
export const Customers: CollectionConfig = {
  slug: 'customers',
  auth: {
    verify: true,
  },
  fields: [],
}
```

`verify` may also be an object with:

- `generateEmailHTML` - function receiving `{ req, token, user }` returning the HTML body.
- `generateEmailSubject` - function returning the subject.

```ts
auth: {
  verify: {
    generateEmailSubject: () => 'Confirm your account',
    generateEmailHTML: ({ token }) =>
      `<a href="https://my-app.com/verify?token=${token}">Verify</a>`,
  },
}
```

The `forgotPassword` auth option takes `generateEmailHTML` and `generateEmailSubject` overrides for the reset email, plus `expiration` (milliseconds) and `minRequestInterval` (default 15000 ms; 0 disables the limit). If the verify link points at a custom frontend URL, that page must itself call the verify operation (`POST /api/<slug>/verify/{token}`).

Emails are sent through the configured email adapter (see email-adapters); without one, Payload logs a warning on startup and again on any attempt to send.

Verification is a POST to `/api/<slug>/verify/{token}`.

## Checked

2026-11-04. Read authentication/email, authentication/operations and email/overview in the payloadcms/payload docs. Confirmed: verify and forgotPassword options, email adapter requirement. Fixed: the verify route is POST, not GET; without an adapter Payload logs a warning, not the message. Added: forgotPassword expiration and minRequestInterval.
Method: documentation only; no commands were run.
