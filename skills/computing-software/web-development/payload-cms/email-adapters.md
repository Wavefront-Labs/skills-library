---
id: computing-software.web-development.payload-cms.email-adapters
name: email-adapters
category: computing-software
field: web-development
product: payload-cms
tags: [email, nodemailer, resend, email-adapter]
level: practitioner
status: docs-checked
description: "Configure outgoing email with an adapter (Nodemailer SMTP or Resend) and default from name and address."
sources:
  - https://payloadcms.com/docs/email/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Email adapters

Goal: send verification, reset and custom emails.

Official adapters: `@payloadcms/email-nodemailer` (any Nodemailer transport) and `@payloadcms/email-resend` (Resend REST API, preferred for serverless).

Required options: `defaultFromName` and `defaultFromAddress`.

SMTP with Nodemailer:

```ts
import { nodemailerAdapter } from '@payloadcms/email-nodemailer'

export default buildConfig({
  email: nodemailerAdapter({
    defaultFromAddress: 'info@payloadcms.com',
    defaultFromName: 'Payload',
    transportOptions: {
      host: process.env.SMTP_HOST,
      port: 587,
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
    },
  }),
})
```

Nodemailer options: `transport` (your own transport object) or `transportOptions` (Payload creates the transporter).

Send mail from code with `payload.sendEmail({ to, subject, html })` (`text` also works). Without an adapter Payload logs a warning on startup and on any send attempt. `nodemailerAdapter()` with no arguments uses ethereal.email in development and logs the details on startup. The Resend adapter needs `apiKey`. Attachments: Nodemailer accepts `path` or `content`; Resend accepts a remote `path` URL or Base64 `content`.

## Checked

2026-11-04. Read email/overview in the payloadcms/payload docs. Confirmed: adapters and packages, required defaultFromName and defaultFromAddress, transport and transportOptions, sendEmail. Added: no-adapter warning, ethereal development default, Resend apiKey and attachment notes. Removed: the delivery verify step.
Method: documentation only; no commands were run.
