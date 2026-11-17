---
id: computing-software.collaboration-platform-administration.zulip.mobile-push-plan-management
name: mobile-push-plan-management
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [push-plan, billing-admin, zulip-org-key, self-hosted-billing]
level: practitioner
status: docs-checked
description: "Manage the plan and billing for Zulip's push notification service: billing administrators via change_user_role, server-level login with zulip_org_id and zulip_org_key."
sources: ["https://zulip.readthedocs.io/en/latest/production/mobile-push-notifications.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Push notification plan management

Organizations with more than 10 users must have a paid self-hosted plan or the free Community plan (if eligible) to use the service. Servers on Zulip 8.0+ make this easier, but the same plans exist for all versions.

**Per organization (8.0+).** Organization owners and billing administrators reach plan management from the Zulip app. On Zulip Server 10.0+ the help center explains how to configure who may manage plans and billing. On older versions, add billing administrators with the management command, passing the realm's string ID and the user's email:

```
~zulip/deployments/current/manage.py change_user_role -r '' username@example.com is_billing_admin
```

Remove the permission by adding `--revoke`.

**Per server.** Servers older than 8.0 start from the server login page of the selfhosting site. It also works on 8.0+, and lets one plan cover multiple organizations on an installation. The username and password are your server's `zulip_org_id` and `zulip_org_key`. Read them from `/etc/zulip/zulip-secrets.conf`, or run:

```
~zulip/deployments/current/scripts/get-django-setting ZULIP_ORG_ID
~zulip/deployments/current/scripts/get-django-setting ZULIP_ORG_KEY
```

Treat the key like a password. When moving to a new server, copy these two secrets across to keep the registration.

## Checked

2026-11-08. Checked: read against the Zulip mobile-push-notifications page (docs/production/mobile-push-notifications.md, read in full). Removed: a claim about re-registering after backups and a support/sales contact line not on the page.

Method: documentation only; no commands were run.
