---
id: computing-software.collaboration-platform-administration.mattermost.telemetry-and-security-update-check
name: telemetry-and-security-update-check
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [telemetry, security-update-check, diagnostics-reporting, opt-out]
level: practitioner
status: docs-checked
description: "What Mattermost telemetry, the daily security update check and Sentry error reporting collect, and where self-hosted admins opt out."
sources: ["https://docs.mattermost.com/administration-guide/manage/telemetry.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Telemetry and diagnostics

Telemetry shared from Mattermost servers is used to find security and reliability issues, fix software problems, improve quality and inform design decisions. It is encrypted in transit and excludes personally identifiable information and message contents. It is enabled by default; self-hosted admins can opt out in the System Console, while Cloud admins cannot disable it.

Security update check: servers share diagnostic information so Mattermost can send alerts about high priority security updates. Collected once every 24 hours: build number and version, build type (Enterprise or Team Edition), server operating system, the diagnostic ID (also used for the push notification proxy and to prevent double counting), database type and version, counts of teams, users and activated users, whether unit tests have been run, and the date and time of the last check. Opt out by disabling Enable Security Alerts under Environment > SMTP.

Error and diagnostics reporting: when enabled, server errors and panics are sent to a Mattermost-hosted Sentry endpoint, without message content or personal information. Opt out by disabling Enable Diagnostics and Error Reporting under Environment > Logging.

Android app performance monitoring: the Android Beta build sends trace events (durations of actions such as start:overall, team:switch, channel:loading, posts:loading, named start observation:end observation) and non-personal device information such as api_level, brand, model, system_version, timezone and server_version.

If your policy forbids outbound telemetry, switch off both toggles above and record that the security alert feed is lost as a result.

## Checked

Confirmed against the Telemetry page: purposes, default-on and opt-out rules, the 24-hour security update data list, both opt-out paths, Sentry error reporting and the Android Beta trace events and device fields named. Nothing removed.

Method: docs-checked 2026-11-09 against the full administration-guide/manage/telemetry page (source rst from the mattermost/docs repo).
