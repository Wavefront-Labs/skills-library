---
id: computing-software.collaboration-platform-administration.zulip.import-into-new-zulip-server
name: import-into-new-zulip-server
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [manage-py-import, data-import, delete-realm, password-reset-email]
level: advanced
status: docs-checked
description: "Import a Zulip data export into a fresh server with manage.py import: version match, which secrets to copy, subdomain option, password reset emails and delete_realm cleanup."
sources: ["https://zulip.readthedocs.io/en/latest/production/export-and-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Importing a Zulip export

1. Install a new server but skip the organization-creation step. Use the same Zulip version as the exporter; for Zulip Cloud exports run `upgrade-zulip-from-git zulip-cloud-current`. With little free RAM, run `./scripts/stop-server` during the import.
2. When replacing a server, copying `/etc/zulip/settings.py`, `zulip.conf` and most of `zulip-secrets.conf` is recommended. Exceptions: do not copy `avatar_salt` (avatars are rewritten for renumbered IDs and browser caching could show wrong images); do copy `zulip_org_id` and `zulip_org_key` to stay registered with the push notification service; do copy `camo_key` or links to external images break; if you copy `rabbitmq_password`, run `scripts/setup/configure-rabbitmq` as root.
3. As the `zulip` user:

```
cd ~
tar -xf /path/to/zulip-export-<timestamp>.tar.gz
cd ~zulip/deployments/current
./manage.py import '' ~/zulip-export-<timestamp>
./scripts/start-server
```

Use a subdomain instead of `''` to import beside an existing root organization. It can take several minutes.

Passwords are not exported. Users must use SSO or reset: test with `./manage.py send_password_reset_email -u username@example.com`, then `-r '' --all-users`.

To redo a test import, run `./manage.py delete_realm -r ''`, which permanently deletes the organization. With local uploads, remove files under the uploads directory for that organization's realm id before re-importing.

## Checked

Method: docs-checked 2026-11-09 against https://raw.githubusercontent.com/zulip/zulip/main/docs/production/export-and-import.md (the Import into a new Zulip server section, import options, logging in and deleting/re-importing read in full).
