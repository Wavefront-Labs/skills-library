---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-oncall-slack-and-mobile-notifications
name: grafana-oncall-slack-and-mobile-notifications
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [oncall-slack-setup, oncall-mobile-notifications, grafana-oncall, grafana-irm, paging-tooling]
level: practitioner
status: docs-checked
description: "Connect Grafana OnCall to Slack and the mobile app: Slack install, user linking, /escalate, push notification types, Do Not Disturb override."
sources: ["https://github.com/grafana/oncall/blob/dev/docs/sources/manage/notify/slack/index.md", "https://github.com/grafana/oncall/blob/dev/docs/sources/manage/mobile-app/push-notifications/index.md", "https://github.com/grafana/oncall/blob/dev/docs/sources/manage/mobile-app/installation-and-setup/index.md", "https://github.com/grafana/oncall/blob/dev/docs/sources/set-up/open-source/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana OnCall: Slack and mobile notifications

The OnCall Slack integration page warns that the OnCall Slack app is now a Grafana IRM app and tells you to migrate;
the page below describes the legacy OnCall integration.

## Slack
Installing needs Admin permissions in both Grafana and the Slack workspace.
- Cloud: Settings -> Chat Ops tab -> Slack -> Install Slack integration, give your workspace URL, sign in, click Allow.
- OSS: set `FEATURE_SLACK_INTEGRATION_ENABLED` to True, serve OnCall over HTTPS, create a Slack app "From an app manifest"
  (the manifest is in the open-source setup page; replace `<YOUR_BOT_NAME>` and `<ONCALL_ENGINE_PUBLIC_URL>`), then set
  `SLACK_CLIENT_OAUTH_ID`, `SLACK_CLIENT_OAUTH_SECRET`, `SLACK_SIGNING_SECRET` (from the app's Basic Information ->
  App Credentials) and `SLACK_INSTALL_RETURN_REDIRECT_HOST` (the OnCall external URL), then install from ChatOps -> Slack.

After install:
- Pick a default Slack channel in the Slack integration settings: alerts go there unless an escalation chain says otherwise.
- Additional Settings can send reminders for acknowledged alerts and revert an alert group to unacknowledged if the
  reminder is not confirmed.
- Each user connects their account: Users -> View my profile -> User Info -> Slack username -> Connect.
- Escalation chains have two Slack steps: notify all members of a Slack channel, and notify a Slack user group. A user's
  own notification steps can use Notify by -> Slack mentions.
- Slack user groups linked to schedules are updated automatically (users added when a shift starts, removed when it
  ends); Slack requires a paid plan for user groups.
- `/escalate` pages a team (and additional responders) from any channel via the Create Alert Group form. `/oncall` is
  deprecated in favour of `/escalate`.
- The message shortcut "Add as resolution note" (More actions menu) works only on messages in an alert group's thread.

## Mobile app
- Connect by QR code (profile icon -> IRM tab on desktop; the QR code times out, so screenshots will not work) or by
  deeplink from the phone (profile icon -> IRM tab -> Sign in).
- OSS needs the instance connected to Grafana Cloud OnCall, which acts as the relay for push notifications, and the
  instance must be reachable from the phone's network.
- Notification types: Mobile push (for all alerts), Mobile push important (louder, default for important alerts),
  on-call shift notifications and shift swap notifications (both optional, in the info notifications section).
- Add them to notification policies: Important notifications should include Mobile push important, Default
  notifications should include Mobile push. Edit in the app (Settings -> Notification policies) or on desktop under
  the profile's User Info tab.
- Send a test notification of default or important priority from the profile's Mobile App connection tab to check
  Do Not Disturb and volume overrides.
- Android: each type (important, default, info) registers a system notification channel; Override Do Not Disturb is
  usually in the channel options. Volume Override needs the separate Override Do Not Disturb app permission.
- iOS: sound, style and Do Not Disturb override for important notifications are set inside the app.
- The docs suggest combining mobile push with phone/SMS in case of degraded connectivity.

## Checked

2026-11-08. Confirmed against the raw OnCall docs in the grafana/oncall repository (manage/notify/slack,
manage/mobile-app and its push-notifications and installation-and-setup pages, set-up/open-source Slack Setup). The
grafana.com versions of these pages redirect to a generic landing page, so the repository sources replaced them in
`sources`. Removed as unconfirmed: the 2025/2026 maintenance and archive dates, button names on alert messages,
the rate-limit gotcha, the "Send demo alert" tip, and the example "Wait 5 min -> Phone call" policy.
Method: documentation only; no commands were run.
