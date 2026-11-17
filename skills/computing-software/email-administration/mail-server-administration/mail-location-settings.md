---
id: computing-software.email-administration.mail-server-administration.mail-location-settings
name: mail-location-settings
category: computing-software
field: email-administration
product: mail-server-administration
tags: [mail-location-settings, mail-location, vmail, virtual-users]
level: practitioner
status: docs-checked
description: "Set mail_location with %d and %n variables, home directories and the vmail user for virtual users."
sources:
  - https://doc.dovecot.org/2.3/configuration_manual/virtual_users/
  - https://doc.dovecot.org/2.3/settings/core/
  - https://doc.dovecot.org/main/installation/upgrade/2.3-to-2.4/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mail location settings

**Goal:** a consistent path per user.
## Steps
1. `mail_location = maildir:/var/vmail/%d/%n/Maildir`
2. Mail is not accessed as the `dovecot` user: use one system user such as `vmail` that owns all mail (or a UID per user), and make `/var/vmail` owned by it.
3. In userdb set uid/gid to that user. A user whose UID is outside `first_valid_uid` (default 500) to `last_valid_uid` cannot log in, so keep the UID inside the range.
4. Dovecot 2.4 splits `mail_location` into several `mail_*` settings; this skill uses the 2.3 form.
## Failure modes
- Login refused for a UID outside `first_valid_uid`..`last_valid_uid`.
- Case-mixed usernames creating duplicate directories: `auth_username_format` defaults to `%Lu` (lowercase) in 2.3, so do not override it with a non-lowercase format.
## Verify
- Deliver a test message and check the file appears under the expected path with correct owner.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 Virtual Users page (vmail user, `mail_home = /var/vmail/%d/%n`, not the dovecot user), the settings reference (`first_valid_uid`, `last_valid_uid`, `auth_username_format` default `%Lu`) and the 2.3 to 2.4 converted-settings table. Removed the useradd and chown commands, the Postfix virtual_mailbox_base claim and the unsourced permission-denied cause.

Method: documentation only; no commands were run.
