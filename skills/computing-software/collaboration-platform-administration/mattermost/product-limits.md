---
id: computing-software.collaboration-platform-administration.mattermost.product-limits
name: product-limits
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [product-limits, hard-limits, attachments, message-length]
level: intro
status: docs-checked
description: "Reference of Mattermost hard and recommended product limits such as message length, attachments, channel fields, sessions and teams."
sources: ["https://docs.mattermost.com/administration-guide/manage/product-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Product limits

Mattermost documents hard and recommended limits. Check these before designing integrations or sizing guidance.

Messaging: message length 16,383 characters; group messages 8 participants (use a private channel if you need more); emoji reactions per message 50; custom emoji uploads 6000; bookmarked links and files per channel 50; custom user group notifications 256 users per group; message acknowledgement response time 5 minutes.

Names and text fields: channel name 64 characters, channel purpose 250, channel header 1024, custom status 100, user nickname 64, team description 50, custom brand text 500, custom site description 1024.

Files: 10 attachments per message; attachment file size 100 MB, image file size 253 MB, dimensions 7680 x 4320 pixels, and image resolution 33 megapixels (8K). The attachment limits are marked configurable.

Sessions: SSO and mobile session duration 30 days.

Scale: 10,000 teams per deployment; users per team have no enforced limit and depend on infrastructure. Call participants are unlimited but 50 is recommended. Advanced log output has a 500 MB file size limit and 1000 audit records.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/manage/product-limits (limits table). Nothing removed.

Method: documentation only; no commands were run.
