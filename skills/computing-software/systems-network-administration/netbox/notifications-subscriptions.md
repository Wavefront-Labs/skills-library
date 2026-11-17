---
id: computing-software.systems-network-administration.netbox.notifications-subscriptions
name: notifications-subscriptions
category: computing-software
field: systems-network-administration
product: netbox
tags: [notifications, subscriptions, event-rule-notifications]
level: intro
status: docs-checked
description: "Subscribe to objects or generate notifications from event rules."
sources: ["https://netboxlabs.com/docs/netbox/features/notifications/", "https://netboxlabs.com/docs/netbox/features/event-rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Notifications

Goal: tell users when things change.

NetBox has a notification system. Notifications can be marked as read or deleted by individual users. Two built-in mechanisms generate them:

1. **Subscriptions.** A user subscribes to an object. When that object is modified, a notification informs the user.
2. **Event rules.** A rule can generate a notification for one or more users in response to specific system events, alongside the other rule actions (running a script or sending a webhook).

Plugins can also generate notifications for their own purposes.

**Setting up an event-rule notification**

1. Create an event rule for the object type and events (create, update, delete).
2. Choose the action that generates user notifications and select the users to notify.
3. Add JSON conditions if only some objects should notify.

**Related.** Event processing uses the Redis queue and the `rqworker` process, so the worker must be running. Per-user display options live under user preferences, which persist across sessions.

**Checklist**

1. Prefer subscriptions for personal watching.
2. Use event rules for team-wide alerts.
3. Confirm the worker is up.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Notifications and Event Rules feature pages (both read in full).
