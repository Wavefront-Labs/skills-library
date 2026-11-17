---
id: computing-software.collaboration-platform-administration.zulip.webex-and-google-meet-integrations
name: webex-and-google-meet-integrations
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [webex-integration, google-meet-integration, oauth-redirect-uri]
level: advanced
status: docs-checked
description: "Set up Webex and Google Meet call providers in self-hosted Zulip: OAuth app redirect URIs under /calls/, scopes, secrets, client IDs and audience settings."
sources: ["https://zulip.readthedocs.io/en/latest/production/video-calls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Webex and Google Meet integrations

**Webex.** Register a custom integration on the Webex developer portal ("New Integration"). Answer "No" to the mobile SDK question, choose name, icon and description, set Redirect URI to `https://zulip.example.com/calls/webex/complete`, and select scopes `spark:all`, `meeting:schedules_read` and `meeting:schedules_write`. App Hub submission is optional. Paid Webex organizations get an ad-hoc meeting; free ones get a personal room meeting.

In Zulip: set `video_webex_client_secret` in `/etc/zulip/zulip-secrets.conf`, set `VIDEO_WEBEX_CLIENT_ID` in `/etc/zulip/settings.py`, and restart with `scripts/restart-server`.

**Google Meet.** Create a Google Cloud OAuth 2.0 app in a project with the Google Meet REST API enabled (APIs & Services > Library). On the OAuth consent screen set app name, support email and developer contact, and pick an audience:

- Internal: users need accounts in your Google Workspace organization.
- External: any Google account works, but the app must pass Google's OAuth verification.

For use outside your Workspace add the scope `https://www.googleapis.com/auth/meetings.space.created`. Under Credentials create an OAuth client ID of type Web application with authorized redirect URI `https://zulip.example.com/calls/google_meet/complete`, and note the Client ID and Secret.

In Zulip: set `video_google_meet_client_secret` in `zulip-secrets.conf`, then `VIDEO_GOOGLE_MEET_CLIENT_ID` and `VIDEO_GOOGLE_MEET_AUDIENCE_INTERNAL` (matching the audience) in `settings.py`, and restart.

Finish by selecting the provider in each organization's settings.

## Checked

2026-11-08. Checked: read against the Zulip video-calls page (docs/production/video-calls.md, read in full). Removed: nothing.

Method: documentation only; no commands were run.
