---
id: computing-software.collaboration-platform-administration.zulip.bigbluebutton-video-call-integration
name: bigbluebutton-video-call-integration
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [bigbluebutton, big-blue-button-url, bbb-conf-secret]
level: practitioner
status: docs-checked
description: "Connect a BigBlueButton 2.4+ server to Zulip video calls with bbb-conf --secret, big_blue_button_secret and BIG_BLUE_BUTTON_URL, then select it per organization."
sources: ["https://zulip.readthedocs.io/en/latest/production/video-calls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BigBlueButton call integration

You need a BigBlueButton server, version 2.4 or newer.

Gather two values from that server:

1. The Shared Secret, from `bbb-conf --secret`. The BigBlueButton administration documentation also describes extracting it.
2. The API URL, of the form `https://bigbluebutton.example.com/bigbluebutton/`, which `bbb-conf --secret` also shows.

Configure Zulip:

1. In `/etc/zulip/zulip-secrets.conf` set `big_blue_button_secret` to the shared secret.
2. In `/etc/zulip/settings.py` set `BIG_BLUE_BUTTON_URL` to the API URL.
3. Restart the server with `~zulip/deployments/current/scripts/restart-server`.

That enables BigBlueButton on the server. It still must be chosen as the video call provider in each Zulip organization that should use it, via the call provider setting.

Notes on the other providers covered by the same documentation page:

- Jitsi Meet needs no server configuration: Zulip defaults to the cloud-hosted Jitsi Meet, and a self-hosted instance is set by entering its URL in organization settings.
- Setting the call provider to "None" disables the call buttons for an organization.
- Nextcloud Talk needs a Nextcloud server, version 22 or newer, with the Talk app enabled.
- Constructor Groups needs a Constructor Groups account.

## Checked

2026-11-08. Checked: read against the Zulip video-calls page (docs/production/video-calls.md, read in full). Removed: the administrator-only claim and the never-in-settings.py advice.

Method: documentation only; no commands were run.
