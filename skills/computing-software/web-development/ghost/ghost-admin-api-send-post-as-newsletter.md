---
id: computing-software.web-development.ghost.ghost-admin-api-send-post-as-newsletter
name: ghost-admin-api-send-post-as-newsletter
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, newsletter, email-segment, nql, send-post]
level: advanced
status: docs-checked
description: "Email a Ghost post to subscribers via the Admin API with the newsletter slug and optional email_segment filter."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/posts/sending-a-post.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: publish a post and email it to a newsletter's subscribers.

Rule: a post is emailed if and only if an active newsletter is provided. Pass the `newsletter` query parameter, set to the newsletter's `slug`, when publishing or scheduling. Find slugs by browsing the newsletters endpoint.

Segmenting: add `email_segment` with a members NQL filter to send to a subset of that newsletter's subscribers. Common values: `status:free` (free members), `status:-free` (paid members), `all`. If omitted, `all` is used.

Example request: `PUT /admin/posts/{id}/?newsletter=weekly&email_segment=status:-free` with body `{"posts":[{"status":"published","updated_at":"<value>"}]}`.

After sending, the post object includes related `newsletter` and `email` objects. If the `email` object has `status: failed`, retry by reverting the post to `draft` and then republishing.

Prerequisite: Mailgun is required for bulk mail on self-hosted sites (see ghost-newsletter-bulk-email-mailgun).

Verify: the post JSON shows an `email` object, and its status is not `failed`.

## Checked

2026-11-04. Confirmed: newsletter slug parameter, the if-and-only-if rule, email_segment values and default, newsletter and email objects, failed-send retry (sending a post page); Mailgun requirement (configuration page). Removed: nothing material.

Method: documentation only; no commands were run.
