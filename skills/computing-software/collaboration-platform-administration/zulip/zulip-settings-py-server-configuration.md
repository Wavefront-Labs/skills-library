---
id: computing-software.collaboration-platform-administration.zulip.zulip-settings-py-server-configuration
name: zulip-settings-py-server-configuration
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [settings-py, server-configuration, restart-server, navigation-tour]
level: intro
status: docs-checked
description: "Edit /etc/zulip/settings.py safely: key settings, restarting with restart-server, onboarding video URL and where support and Docker configuration live."
sources: ["https://zulip.readthedocs.io/en/latest/production/settings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Server configuration with settings.py

`/etc/zulip/settings.py` is the main file system administrators use to configure the Zulip server. Organization administrators separately configure many organization options in the web or desktop app, and `/etc/zulip/zulip.conf` covers service-level configuration.

The file documents more than a hundred settings in organised comments; the template is also readable online. Key ones:

- `EXTERNAL_HOST` and `ZULIP_ADMINISTRATOR`, mandatory and prefilled by the installer.
- Authentication methods, including data sync options like LDAP and SCIM.
- The email gateway.
- Video and voice call integrations.
- The uploaded-files storage backend.

To change a setting, edit and save the file, then restart:

```
su zulip -c '~zulip/deployments/current/scripts/restart-server'
```

Onboarding: new users are offered a 2-minute navigation tour video. Point `NAVIGATION_TOUR_VIDEO_URL` at a copy hosted on your network, or at your own introduction video; `None` removes the experience.

In Docker, settings are supplied as `SETTING_*` environment variables, or by editing the file directly via the Compose manual configuration route.

Support is best-effort in the community chat, with paid options available by contacting the project's sales address.

## Checked

Confirmed against the Server configuration page: the role of settings.py versus zulip.conf, the key settings list, the restart command, NAVIGATION_TOUR_VIDEO_URL behaviour, the Docker environment variables and the support options. Removed the sentence about secrets living in zulip-secrets.conf (not on this page).

Method: docs-checked 2026-11-09 against docs/production/settings.md in the zulip/zulip repository (main), the source of the cited page.
