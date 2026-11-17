---
id: computing-software.collaboration-platform-administration.zulip.zoom-video-call-integration
name: zoom-video-call-integration
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [zoom-integration, video-calls, video-zoom-client-id, server-to-server-oauth]
level: practitioner
status: docs-checked
description: "Configure Zoom as a self-hosted Zulip call provider using a Server to Server OAuth app or General OAuth app, video_zoom_client_secret and VIDEO_ZOOM settings."
sources: ["https://zulip.readthedocs.io/en/latest/production/video-calls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zoom call integration

Register a custom Zoom app for your server. Two types:

**Server to Server OAuth app** (since Zulip 10.0): easiest and ideal for most self-hosters, but users must belong to your Zoom organization and use the same email in Zulip as in Zoom. Build it at the Zoom Marketplace: name it, fill the Information tab with description, company and developer contact, add scopes `meeting:write:meeting:admin` and `meeting:write:meeting:master`, then activate it.

**General OAuth app**: more flexible and what Zulip Cloud uses, but Zoom requires the full Marketplace review even for unlisted apps. Create a General App, choose user-managed, set the OAuth Redirect URL to `https://zulip.example.com/calls/zoom/complete`, add the `meeting:write:meeting` scope, complete the Production tab (App Listing and Technical Design), submit for review choosing "Publish the app by myself" (unlisted), and wait for approval.

Then configure Zulip:

1. In `/etc/zulip/zulip-secrets.conf` set `video_zoom_client_secret` to the Client Secret.
2. In `/etc/zulip/settings.py` set `VIDEO_ZOOM_CLIENT_ID`. Enterprise customers not on `zoom.us` may need `VIDEO_ZOOM_API_URL` and `VIDEO_ZOOM_OAUTH_URL`. For a Server to Server app also set `VIDEO_ZOOM_SERVER_TO_SERVER_ACCOUNT_ID` to the Account ID.
3. Restart with `~zulip/deployments/current/scripts/restart-server`.

Finally, set Zoom as the call provider in each organization that should use it.

## Checked

2026-11-08. Checked: read against the Zulip video-calls page (docs/production/video-calls.md, read in full). Removed: the claim that an administrator sets the provider.

Method: documentation only; no commands were run.
