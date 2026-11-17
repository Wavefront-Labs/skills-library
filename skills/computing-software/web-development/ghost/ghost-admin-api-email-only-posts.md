---
id: computing-software.web-development.ghost.ghost-admin-api-email-only-posts
name: ghost-admin-api-email-only-posts
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, email-only, newsletter, sent-status]
level: practitioner
status: docs-checked
description: "Send a Ghost post only as an email, without publishing it on the site, using email_only and the newsletter parameter."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/posts/email-only-posts.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: deliver content by email without a public web page.

Set the post property `email_only` to `true` when you publish or schedule, in combination with the `newsletter` query parameter (the newsletter slug).

Example: `PUT /admin/posts/{id}/?newsletter=weekly` with body `{"posts":[{"status":"published","email_only":true,"updated_at":"<value>"}]}`.

Lifecycle: once the email has been sent, the post has a `status` of `sent` instead of `published`. A scheduled email-only post changes to `sent` when its `published_at` time arrives.

Notes:
- The sending page documents `email_segment` (a members NQL filter) for restricting the audience of an emailed post.
- Failed sends on emailed posts can be retried by moving the post back to `draft` and republishing.
- The scheduling page confirms that email-only scheduled posts end as `sent`, not `published`.

Verify: the post's `status` is `sent` and the email object shows delivery progress.

## Checked

2026-11-04. Confirmed: email_only with the newsletter parameter, the sent status, scheduled email-only ending as sent, retry by reverting to draft (email-only posts, sending a post and scheduling pages). Removed: the use-case paragraph and the "nowhere for the email to go" rationale, which no page states.

Method: documentation only; no commands were run.
