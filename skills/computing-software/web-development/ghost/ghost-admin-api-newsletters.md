---
id: computing-software.web-development.ghost.ghost-admin-api-newsletters
name: ghost-admin-api-newsletters
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, newsletters, opt-in-existing, sender-email]
level: practitioner
status: docs-checked
description: "Create Ghost newsletters via the Admin API with opt_in_existing, and handle the sender_email verification flow."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/newsletters/creating-a-newsletter.mdx
  - https://github.com/TryGhost/docs/blob/main/admin-api/newsletters/sender-email-validation.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add a newsletter and change its sending address correctly.

Create: `POST /admin/newsletters/` with required field `name`. Option: `opt_in_existing`. When true, existing members with a subscription to one or more active newsletters are also subscribed to the new one, and the response metadata includes the number of members opted in.

Example body: `{"newsletters":[{"name":"Product updates"}]}` with `?opt_in_existing=true` if wanted.

Changing the sender address: when you update `sender_email`, email verification is required before emails are sent from the new address. After the update, the response metadata has `sent_email_verification` containing `sender_email`. The stored `sender_email` stays unchanged until the address is verified by clicking the link sent to it.

Workflow:
1. PUT the new `sender_email`.
2. Check the metadata for `sent_email_verification`.
3. Click the link in the mailbox of the new address.
4. Re-fetch the newsletter and confirm `sender_email` changed.

Verify: until the link is clicked, the newsletter keeps the previous sender address.

## Checked

2026-11-04. Confirmed: POST path, required name, opt_in_existing behaviour, sender_email verification and the sent_email_verification metadata (creating a newsletter and sender email validation pages). Removed: nothing.

Method: documentation only; no commands were run.
