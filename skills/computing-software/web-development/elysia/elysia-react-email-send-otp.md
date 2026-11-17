---
id: computing-software.web-development.elysia.elysia-react-email-send-otp
name: elysia-react-email-send-otp
category: computing-software
field: web-development
product: elysia
tags: [integrations-react-email, react-email, email, jsx, bun]
level: practitioner
status: docs-checked
description: "Write email templates as React components, preview them with react-email dev, and send rendered HTML from Elysia via Nodemailer, Resend, SES or SendGrid."
sources:
  - https://elysiajs.com/integrations/react-email.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send a transactional email (an OTP) from an Elysia route using a React Email template.

1. Install:

```bash
bun add -d react-email
bun add @react-email/components react react-dom
```

Add the script `"email": "email dev --dir src/emails"` to package.json and keep templates in `src/emails`. For TypeScript set `"jsx": "react"` in `compilerOptions`.

2. Write `src/emails/otp.tsx`: a default-exported component (`export default function OTPEmail({ otp }: { otp: number })`) built from `@react-email/components` (`Tailwind`, `Section`, `Text`). Add `OTPEmail.PreviewProps = { otp: 123456 }`; it is only used by the preview playground.

3. Preview with `bun email` (opens a browser playground).

4. Render and send. Core pattern (Nodemailer):

```tsx
import { renderToStaticMarkup } from 'react-dom/server'
import OTPEmail from './emails/otp'

new Elysia().get('/otp', async ({ body }) => {
    const otp = ~~(Math.random() * (900_000 - 1)) + 100_000   // 100000-999999
    const html = renderToStaticMarkup(<OTPEmail otp={otp} />)
    await transporter.sendMail({ from, to: body, subject: 'Verify your email address', html })
    return { success: true }
}, { body: t.String({ format: 'email' }) })
```

Provider variants: Nodemailer `createTransport({ host, port: 465, auth })` and `sendMail`; Resend `new Resend(key)` then `resend.emails.send({ ..., html: <OTPEmail otp={otp} /> })` (the JSX element is passed directly); AWS SES `ses.sendEmail({ Source, Destination: { ToAddresses: [body] }, Message: { Body: { Html: { Charset: 'UTF-8', Data: html } }, Subject: {...} } })` with `fromEnv()` credentials in production; SendGrid `sendgrid.setApiKey(...)` then `sendgrid.send({ from, to, subject, html })`.

Gotchas:
- Bun imports `.tsx` directly, so no build step is needed for templates.
- The docs' samples use `await` inside handlers declared without `async`, and fake credentials; declare the handler `async` and load real secrets from the environment.

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/react-email.html); each claim, option name and default was compared with the page text. Removed the invented Verify step.

Method: documentation only; no commands were run.
