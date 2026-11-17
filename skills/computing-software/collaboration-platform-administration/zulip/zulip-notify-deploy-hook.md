---
id: computing-software.collaboration-platform-administration.zulip.zulip-notify-deploy-hook
name: zulip-notify-deploy-hook
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [deploy-hooks, zulip-notify, upgrade-notification]
level: practitioner
status: docs-checked
description: "Configure the zulip_notify deploy hook so Zulip posts a message to a channel before and after each server upgrade, using zulip.conf and zulip-secrets.conf."
sources: ["https://zulip.readthedocs.io/en/latest/production/deployment.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zulip upgrade notification hook

Upgrades run a hook system before and after the change. One bundled hook sends a Zulip message announcing the upgrade.

1. In `/etc/zulip/zulip.conf`, append `, zulip::hooks::zulip_notify` to the `puppet_classes` line.
2. Add a section to the same file:

```
[zulip_notify]
bot_email = your-bot@zulip.example.com
server = zulip.example.com
stream = deployments
```

3. Put the bot's API key in `/etc/zulip/zulip-secrets.conf` as `zulip_release_api_key = ...`. The key is the bot's API key, found in the Zulip UI.
4. As root, run `~zulip/deployments/current/scripts/zulip-puppet-apply` to install the hook.

The `stream` value names the channel that receives the messages.

Other hooks follow the same pattern: add the Puppet class to `puppet_classes`, add a config section, add any secret to the secrets file, and run `zulip-puppet-apply`. Custom hooks of your own are described in the upgrade documentation.

## Checked

Confirmed against the Zulip message deploy hook section of the deployment page: the puppet_classes entry, the zulip_notify section keys, the zulip_release_api_key secret and zulip-puppet-apply. Removed advice about creating the channel and subscribing the bot, and the description of the bot as an ordinary user (not on the page).

Method: docs-checked 2026-11-09 against docs/production/deployment.md in the zulip/zulip repository (main), the source of the cited page.
