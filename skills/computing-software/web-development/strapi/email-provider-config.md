---
id: computing-software.web-development.strapi.email-provider-config
name: email-provider-config
category: computing-software
field: web-development
product: strapi
tags: [strapi, email, provider, sendgrid, nodemailer, sendmail, config-plugins]
level: practitioner
status: docs-checked
description: "Configure a Strapi email provider in config/plugins, set defaultFrom and testAddress, and send mail from code."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/email.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Email feature

The Email feature only handles outbound delivery. It needs a provider (the package Strapi calls) and its config in `config/plugins`. Sendmail (via Nodemailer) is the default provider, meant for local development; for a production SMTP relay consider `@strapi/provider-email-nodemailer` with `provider` set to `"nodemailer"`.

```js
module.exports = ({ env }) => ({
  // ...
  email: {
    config: {
      provider: 'sendgrid', // For community providers pass the full package name (e.g. provider: 'strapi-provider-email-mandrill')
      providerOptions: {
        apiKey: env('SENDGRID_API_KEY'),
        // region: 'eu', // Optional: set to 'eu' for EU data residency (default: 'global')
      },
      settings: {
        defaultFrom: 'juliasedefdjian@strapi.io',
        defaultReplyTo: 'juliasedefdjian@strapi.io',
        testAddress: 'juliasedefdjian@strapi.io',
      },
    },
  },
  // ...
});
```

## Send from code
```js
strapi.plugin('email').service('email').send({
  to: 'valid email address',
  from: 'your verified email address', // e.g. single sender verification in SendGrid
  cc: 'valid email address',
  bcc: 'valid email address',
  replyTo: 'valid email address',
  subject: 'The Strapi Email feature worked successfully',
  text: '${fieldName}', // Replace with a valid field ID
  html: 'Hello world!',
})
```

The admin Settings > Email feature > Configuration page is read-only except a test recipient and **Send test email**; it needs the "Access the Email Settings page" permission.

## Checked

Checked 2026-11-04 against the Strapi Email page (default Sendmail provider, SendGrid config example, send example, admin configuration page). Nothing removed.

Method: documentation only; no commands were run.
