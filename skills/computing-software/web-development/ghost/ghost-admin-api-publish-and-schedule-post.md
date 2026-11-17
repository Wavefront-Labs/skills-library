---
id: computing-software.web-development.ghost.ghost-admin-api-publish-and-schedule-post
name: ghost-admin-api-publish-and-schedule-post
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, publish, schedule, status, published-at]
level: practitioner
status: docs-checked
description: "Publish or schedule a Ghost post through the Admin API by changing status and published_at."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/posts/publishing-a-post.mdx
  - https://github.com/TryGhost/docs/blob/main/admin-api/posts/scheduling-a-post.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move a draft to published or scheduled with a single update.

Publish now: update the draft with `"status": "published"` using the normal edit call with the current `updated_at`.

Schedule: update or set `"status": "scheduled"` and set `published_at` to a datetime in the future, for example `"2030-01-01T09:00:00.000Z"`.

At the scheduled time Ghost publishes the post, sends newsletter emails if applicable, and changes the status to `published`. For email-only posts the final status is `sent`.

Walkthrough:
1. `GET /admin/posts/{id}/` to read `updated_at`.
2. `PUT /admin/posts/{id}/` with `{"posts":[{"status":"scheduled","published_at":"<future ISO date>","updated_at":"<value>"}]}`.
3. Optionally add the `newsletter` query parameter (see the sending skill) to email it.

Use a UTC ISO 8601 timestamp such as the example. Webhook event names are covered in ghost-webhook-events-and-delivery.

Verify: the returned post shows the new `status`, and for scheduled posts the future `published_at`.

## Checked

2026-11-04. Confirmed: status published and scheduled updates, future published_at, post-schedule behaviour including sent for email-only posts (publishing and scheduling pages). Removed: the four webhook event names, which the fetched pages do not list.

Method: documentation only; no commands were run.
