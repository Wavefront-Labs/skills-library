---
id: computing-software.collaboration-platform-administration.mattermost.push-notification-health-targets
name: push-notification-health-targets
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [push-notifications, grafana-dashboard, delivery-rate, notification-monitoring]
level: advanced
status: docs-checked
description: "Read the Mattermost Notification Health Grafana panels, the 100 percent delivery target, error breakdowns and why some pushes are never acked."
sources: ["https://docs.mattermost.com/administration-guide/scale/push-notification-health-targets.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Push notification health targets

The Mattermost Notification Health Grafana dashboard tracks notifications sent from Mattermost. Prerequisites: MetricsSettings.Enable true, the NotificationMonitoring feature flag true, and MetricsSettings.EnableNotificationMetrics enabled in the performance monitoring configuration. Admins can switch notification monitoring data collection off in the System Console.

Panels and targets:
- Push Proxy Delivery Rate: percentage of pushes delivered to the push service (Apple APNs or Firebase Cloud Messaging). It should always be 100 percent; anything under 99 percent deserves investigation.
- Push Notifications Errors by Reason: breakdown of send errors to pinpoint recurring problems and spot intermittent trends early. Missing profile errors are usually safe to ignore, but if they rise, check the logs for push_proxy_send_error.
- Push Notifications Not Sent Distribution: why notifications were not sent (for example the channel was muted), helping separate configuration issues from real faults.
- Push Notifications Stats: sends versus acknowledgements. An acknowledgement means the device received the push and confirmed delivery; the closer the two lines, the better.
- Total Acked Push Notifications: total acknowledged. The remaining roughly 10 to 20 percent of unacknowledged notifications are explained by: servers removed from the mobile app without logging out (the server keeps sending), iOS notifications disabled (the app cannot process or ack them), notifications dropped by APNs or FCM (especially without device connectivity), and Android extreme battery save mode.

Use the delivery rate as the alerting signal, and use the error and not-sent panels to explain dips.

## Checked

Confirmed against the Push notification health targets page: prerequisites, all five panels, the 100 percent target and the 99 percent investigation threshold, push_proxy_send_error, and the four causes of unacknowledged pushes. The closing alerting advice is the author's.

Method: docs-checked 2026-11-09 against the full administration-guide/scale/push-notification-health-targets page (source rst from the mattermost/docs repo).
