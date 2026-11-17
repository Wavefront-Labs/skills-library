---
id: computing-software.web-development.ghost.ghost-newsletter-bulk-email-mailgun
name: ghost-newsletter-bulk-email-mailgun
category: computing-software
field: web-development
product: ghost
tags: [ghost, newsletters, bulk-email, mailgun, smtp, members]
level: practitioner
status: docs-checked
description: "Configure Ghost newsletter delivery: why bulk email needs Mailgun, how it differs from transactional mail, and multiple newsletters."
sources:
  - https://github.com/TryGhost/docs/blob/main/newsletters.mdx
  - https://github.com/TryGhost/docs/blob/main/faq/mailgun-newsletters.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send newsletters from a self-hosted Ghost site.

Two mail paths:
- Transactional email (invites, resets, member sign-in links) uses the standard `mail` config and can use any SMTP or mail service.
- Bulk newsletter email requires a bulk mail API, and the only supported one is Mailgun. Sending bulk mail over basic SMTP will get your IP blacklisted and marked as spam, which is why Ghost does not support it.

Self-hosted setup: enter your Mailgun API keys under the Email newsletter settings in Ghost Admin. Ghost(Pro) includes email delivery. If you never email posts to members you can ignore the newsletter settings and need no Mailgun account.

You can still use another provider such as Mailchimp or Sendgrid to send your newsletter outside Ghost's built-in delivery.

Newsletters: a site has one newsletter by default; extra ones can be created so members choose what they receive. Posts can go to free members, paid members or a segment.

Auth emails (members' passwordless login links) are not bulk and use the standard mail configuration; self-hosted installs can use Mailgun or other providers for it.

The FAQ says Ghost supports only one bulk mail API because supporting several is too much overhead for a small team, and that Ghost has no partnership or referral arrangement with Mailgun. It also notes you can sync your members database to an external newsletter provider via Zapier or the integration guides.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, no imported snippets): newsletters.mdx (37 lines) and faq/mailgun-newsletters.mdx (30 lines). Every claim above matches. Removed the Verify step (test post and Mailgun logs are not on either page). The newsletters page also quotes a Mailgun free allowance and pricing; deliberately not repeated, since prices are not kept.
Method: documentation only; no commands were run.
