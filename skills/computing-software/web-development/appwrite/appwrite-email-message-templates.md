---
id: computing-software.web-development.appwrite.appwrite-email-message-templates
name: appwrite-email-message-templates
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, email-templates, smtp, localization]
level: practitioner
status: docs-checked
description: "Customize verification, magic URL, reset and invite emails per language after switching the project to a custom SMTP server."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/message-templates/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: brand the emails Appwrite sends for auth.

Prerequisite: Appwrite Cloud ships a default SMTP server for getting started that sends generic emails and does not allow template customization (to prevent malicious templates). Configure your own server first.

Custom SMTP: Project Settings > SMTP tab > toggle Custom SMTP server and enter Sender name, Sender email, Server host, Server port, Username and Password from a provider such as SendGrid or Mailgun, then click Update.

Edit templates:
1. Open the Auth service > Templates tab.
2. Expand the template to change.
3. Pick the Template language; each supported locale can have its own version.
4. Edit the fields and click Update.

Templates covered: account verification, magic-url authentication, password resets and user invites. Each project has its own set, and templates support localization served by configured locale.

Gotcha: the built-in email service does not support custom templates, to prevent malicious templates; the Sender email must be authenticated on your SMTP provider (usually the same domain as your SMTP username) or mail lands in spam.

Template parts: Sender name, Sender email, Reply to (empty means the sender address is used), Subject, and Message (HTML). Variables, usable only in Message: `{{project}}`, `{{team}}`, `{{user}}` (not available in the Magic URL template) and `{{redirect}}`. Locale is set with `client.setLocale('fr')` in the SDKs or the `X-Appwrite-Locale` HTTP header.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Message templates (auth/message-templates): the default SMTP limitation, Custom SMTP steps and fields, template editing steps, the four template types, components, variables, and localization. Replaced the unverified "probably still on default SMTP" gotcha with the page's stated limitation; removed the createVerification Verify step.
Method: documentation only; no commands were run.
