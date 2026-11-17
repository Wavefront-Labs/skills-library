---
id: computing-software.devops-ci-cd.forgejo.moderation-and-spam-controls
name: moderation-and-spam-controls
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [moderation, abuse-reports, spam-bots, user-purge]
level: practitioner
status: docs-checked
description: "Use Forgejo's moderation features: signup notifications, abuse reports, user blocking and purging users."
sources:
  - https://forgejo.org/docs/latest/admin/advanced/moderation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo's moderation tools help deal with spam bots and unwanted interaction.

- New signup alerts: on small instances with open registration set `[admin] SEND_NOTIFICATION_EMAIL_ON_NEW_USER = true` so the admin is emailed instead of checking manually.
- Self moderation: on large instances users can block unwanted interaction from another user, as described in the user blocking guide.
- Deleting users with their content: use the administration panel, or run `forgejo admin user delete --purge`, which removes the user including their repositories and issues.
- Abusive content reporting: disabled by default. Enable with `[moderation]` `ENABLED = true`. A `Report abuse` action then appears in the context menu of user and organization profiles, and `Report content` in the menu of repositories, issues, pull requests and comments. Optionally set `KEEP_RESOLVED_REPORTS_FOR = 168h` to auto-delete resolved reports when the corresponding cron is enabled.

Administrators then see a Moderation reports section in Site administration, where a report can be marked Handled or Ignored, the user suspended (SSH access could still be allowed), or the reported content deleted.

## Checked

2026-11-04. Confirmed against the Forgejo Moderation tools page: signup notification setting, user blocking, user deletion options, the [moderation] settings, the report menu entries and the administrator report actions. Removed: the closing advice to combine with captcha settings and to back up before purging, not on the page.

Method: documentation only; no commands were run.
