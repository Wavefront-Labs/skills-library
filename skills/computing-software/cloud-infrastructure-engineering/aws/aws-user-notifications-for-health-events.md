---
id: computing-software.cloud-infrastructure-engineering.aws.aws-user-notifications-for-health-events
name: aws-user-notifications-for-health-events
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, user-notifications, health, eventbridge, notifications, operations]
level: practitioner
status: docs-checked
description: "Route AWS Health events to email, chat and mobile with AWS User Notifications: hubs, configurations with event rules, aggregation and organization-wide setup."
sources: ["https://docs.aws.amazon.com/notifications/latest/userguide/what-is-service.html", "https://docs.aws.amazon.com/notifications/latest/userguide/notification-hubs.html", "https://docs.aws.amazon.com/notifications/latest/userguide/getting-started.html", "https://docs.aws.amazon.com/notifications/latest/userguide/managing-org-notifications.html", "https://docs.aws.amazon.com/notifications/latest/userguide/ev-managed-rules.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS User Notifications for Health events

**Goal:** the right people see AWS Health events (maintenance, service issues, account notifications) without
building EventBridge-to-Lambda-to-chat plumbing.

## Concepts
- **Notification hub:** where User Notifications stores your notification data; you must select at least one
  when creating a configuration.
- **Notification configuration:** event rules (source service, event type, Regions, optional Advanced filter in
  EventBridge event pattern JSON, no wildcard support) + **delivery channels** + an aggregation setting.
- **Delivery channels:** email addresses, chat channels (through Amazon Q Developer in chat applications) and
  mobile devices (AWS Console Mobile Application push notifications, not SMS).
- **AWS managed notifications:** notifications AWS sends on its own (the guide lists AWS Health, AWS Marketplace and
  Partner Central, and Billing and Cost Management categories) with account contacts and delivery channels you can manage.

## Create (user-configured notification)
Console: User Notifications, Notification configurations, Create. Choose the service (AWS Health), event type
and the Regions where your service data is located, add Advanced filter if needed, then:
- Aggregation (on by default, recommended): receive within 5 minutes (recommended), within 12 hours, or do not aggregate.
- Delivery channels: add email addresses (a verification email is sent when you create the configuration; the
  recipient must be signed in to the AWS account that added it; distribution lists work), chat channels and mobile devices.
- Chat requires the channel to be set up in Amazon Q Developer in chat applications; mobile requires the Console
  Mobile Application with push notifications enabled and the IAM permission to list devices.
Under the hood User Notifications creates one EventBridge managed rule per event source
(`AWSUserNotificationsManagedRule-...`). You cannot edit them; do not delete them by hand, because notifications
may stop working. Deleting the configuration or event rule cleans them up.

## Organization
With AWS Organizations you can configure and view notifications centrally for OUs or all accounts; when a member
account event matches the rules, a notification is generated in the management account. AWS recommends a delegated
administrator. Events from before you enabled trusted access do not generate notifications, and configurations update
automatically as accounts join or leave.

## Tips
- Use separate configurations by urgency and route each to a different channel (on-call chat versus a ticket-queue
  email with 12-hour aggregation).
- Keep EventBridge rules for automation and User Notifications for humans.

## Verify
- [ ] The email channel shows as verified and chat/mobile channels show notifications.
- [ ] A real event reaches the intended channel.

## Checked
2026-10-28. Confirmed on the User Notifications pages (what-is, hubs, getting started, organization, managed rules):
hubs, configuration fields, aggregation options, channels and prerequisites, email verification, managed rule behaviour,
organization behaviour. Removed (not confirmable from these pages): Health `eventTypeCategory` filter and JSON example,
Region/us-east-1 emission claims, "Send test notification", Teams delivery, managed notification category examples
beyond the names the guide lists, and per-event-type tip details. The original `sources` were prose; replaced with URLs.
Method: documentation only; no commands were run.
