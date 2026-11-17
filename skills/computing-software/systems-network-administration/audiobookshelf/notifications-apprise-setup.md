---
id: computing-software.systems-network-administration.audiobookshelf.notifications-apprise-setup
name: notifications-apprise-setup
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [notifications, apprise, webhook, templates, rate-limit]
level: practitioner
status: docs-checked
description: "Configure Audiobookshelf notifications through an Apprise API endpoint, including event templates and the rate limits that drop messages."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/notifications.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All notifications go through [Apprise](https://github.com/caronc/apprise). Audiobookshelf will not build service-specific notification code. You need a running **Apprise API** instance, or another endpoint that handles the same requests.

Apprise configuration: enter the full URL path to your Apprise API instance.

Per-event entries each have:

- **Notification Event** - the trigger, such as `onTest` or `onBackupCompleted`.
- **Apprise URL** - destination, typically the Apprise API endpoint (for example `http://localhost:9000/notify`) or your webhook; different events can go to different endpoints.
- **Title Template** and **Body Template** - use variable substitution with double braces such as `{{variable}}`. The available variables for each event are listed at the bottom of the pop-up.

Limits: at most 1 notification per second to prevent spam. If the queue is full, new notifications are dropped. A notification is disabled if it fails to send the configured number of times in a row.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Notifications page.

Method: documentation only; no commands were run.
