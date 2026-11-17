---
id: computing-software.collaboration-platform-administration.zulip.register-mobile-push-notification-service
name: register-mobile-push-notification-service
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [mobile-push, push-notification-service, register-server, zulip-service-push]
level: practitioner
status: docs-checked
description: "Register a self-hosted Zulip server with the Mobile Push Notification Service: ZULIP_SERVICE_PUSH_NOTIFICATIONS, register_server, usage statistics opt-out and app re-login."
sources: ["https://zulip.readthedocs.io/en/latest/production/mobile-push-notifications.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mobile Push Notification Service registration

Apple and Google do not let self-hosted servers push directly to the shared Zulip mobile apps, so Zulip runs a forwarding service. Zulip Server 10.0+ installers do this with `--push-notifications`; the manual steps (Zulip 9.0+) are:

1. Ensure outgoing HTTPS to the Internet works, configuring the outgoing proxy first if one is required.
2. Make `ZULIP_ADMINISTRATOR` in `/etc/zulip/settings.py` a monitored real address; the service contacts it.
3. Set `ZULIP_SERVICE_PUSH_NOTIFICATIONS = True` by uncommenting that line.
4. Decide on usage statistics. By default they are uploaded; disable with `ZULIP_SERVICE_SUBMIT_USAGE_STATISTICS=False`. Basic organization metadata is always uploaded.
5. Restart the server.
6. Register, as root:

```
su zulip -c '~zulip/deployments/current/manage.py register_server'
```

It prints the data it would send, asks you to accept the terms of service, and registers. Docker users run `./manage.py register_server` from the docker-zulip directory.

7. Organizations with more than 10 users need a paid plan, or the free Community plan if eligible.
8. Anyone already using the mobile app must log out and back in to start receiving notifications.

Test using the help center's mobile notification test instructions.

If you move to a new server, copy `zulip_org_id` and `zulip_org_key` from `zulip-secrets.conf` to keep the registration. These are also the plan-management login credentials.

## Checked

2026-11-08. Checked: read against the Zulip mobile-push-notifications page (docs/production/mobile-push-notifications.md, read in full). Removed: nothing.

Method: documentation only; no commands were run.
