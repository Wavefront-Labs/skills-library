---
id: computing-software.collaboration-platform-administration.vikunja.config-new-user-defaults
name: config-new-user-defaults
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, defaultsettings-section, new-user-defaults, avatar-provider, overdue-reminders, week-start]
level: practitioner
status: docs-checked
description: "Set default preferences applied to newly created Vikunja users: avatar, reminders, discoverability, default project, week start, language and time zone."
sources:
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`defaultsettings.*` are applied when a user is created. Changing them later does not alter existing users.

Options and defaults:
- `avatar_provider` `initials`; also `gravatar`, `upload` (needs `avatar_file_id`) or `marble`. `avatar_file_id` 0.
- `email_reminders_enabled` false.
- `discoverable_by_name` false (others find the user by partial name); `discoverable_by_email` false (exact email).
- `overdue_tasks_reminders_enabled` true and `overdue_tasks_reminders_time` `9:00`: a daily mail listing overdue tasks.
- `default_project_id` 0: make sure users have access to the project you name.
- `week_start` 0: 0 is Sunday, 1 Monday.
- `language`: ISO 639-1 code plus ISO 3166-1 country code; otherwise the browser language at sign-up.
- `timezone`: defaults to `service.timezone`; affects reminder and overdue email times.

Related global avatar options: `avatar.gravatarexpiration` (3600 seconds) and `avatar.gravatarbaseurl` for Gravatar-compatible services such as libravatar.

## Checked

2026-11-04: checked against config-raw.json (defaultsettings and avatar sections). Removed the claim that `service.enableemailreminders` and a working mailer are needed for reminder emails (not stated for these settings).

Method: documentation only; no commands were run.
