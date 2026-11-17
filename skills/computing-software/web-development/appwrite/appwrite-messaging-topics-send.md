---
id: computing-software.web-development.appwrite.appwrite-messaging-topics-send
name: appwrite-messaging-topics-send
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, messaging, topics, email, sms, push, server-sdk]
level: practitioner
status: docs-checked
description: "Group targets into topics and send email, SMS or push messages immediately or on a schedule."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/messaging/topics/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/messaging/messages/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/messaging/send-email-messages/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: broadcast a message.

Topics: a topic groups targets that should receive the same message; targets subscribe to it and everything published to the topic reaches all subscribers. Give a topic semantic meaning (for example an announcement list). Topics are optimized for the same message to large groups; send private information such as chat messages to individual targets, and to reach all of one user's devices look up their targets (the page points to `account.get()`). Create one in Console > Messaging > Topics > Create topic, with a Server SDK `messaging.createTopic({ topicId, name, subscribe: [<ROLE>] })` where `subscribe` holds permission roles for who can subscribe, or with the CLI: `appwrite init topics` then `appwrite push topics`.

Sending: use a Server SDK. The email guide uses `createEmail`; the messages page shows the same pattern for push notifications and SMS. The email guide says to leave `schedule` empty to send immediately, and to schedule by setting `status` to `'scheduled'` with `schedule` as an ISO 8601 date-time. The messages page lists the options as `draft` (true or false) and `scheduledAt` (an ISO date time string); follow the current SDK reference for the exact parameter names.

Message statuses: `draft`, `scheduled`, `processing`, `failed`, `success`. Lifecycle: a message starts as a draft or goes straight to processing if sent immediately; a scheduled message is `scheduled` and moves to processing at schedule time; after delivery is attempted it is marked sent or failed.

Parameters per type:
- Email: `subject` and `content` required; optional `cc` and `bcc` (arrays of target IDs), `html` (boolean saying `content` is HTML), `draft`, `scheduledAt`.
- Push: `title`, `body`, `data` (extra key-value pairs), `action`, `icon`, `sound`, `color`, `tag` and `badge` (an integer; 0 removes the badge), `contentAvailable`, `critical`, `priority` (normal or high), `draft`, `scheduledAt`. Several are platform specific (icon, color and tag are Android only; badge, contentAvailable and critical are Apple only).
- SMS: `content` required (keep it concise because of character limits), plus `draft` and `scheduledAt`.

Email delivery needs a configured provider and targets (a verified email-password user already has an email target); the email guide lists Mailgun, Resend and SendGrid as supported providers.

## Checked

2026-11-04. Confirmed against the Appwrite docs pages Topics, Messages and Send email messages (read from raw markdown where the rendered page was truncated): topic concept and privacy advice, topic creation methods and the CLI commands, message statuses and lifecycle, the per-type parameter tables, the schedule instructions from the email guide, and the provider and target prerequisites. Removed: `createSms` and `createPush` as named methods, the claims about editing or cancelling drafts and scheduled messages, the "enabled provider" gotcha, and the Verify step. The email guide and messages page disagree on scheduling parameter names, so both are reported.
Method: documentation only; no commands were run.
