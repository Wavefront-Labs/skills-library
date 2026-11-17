---
id: computing-software.web-development.ghost.ghost-webhook-events-and-delivery
name: ghost-webhook-events-and-delivery
category: computing-software
field: web-development
product: ghost
tags: [ghost, webhooks, events, post-published, site-changed, integrations]
level: practitioner
status: docs-checked
description: "Ghost webhook events (site, post, page) and delivery rules: configure in Admin and return 2xx for success."
sources:
  - https://github.com/TryGhost/docs/blob/main/webhooks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: react to Ghost content changes in other systems.

Ghost sends a POST with a JSON body describing the event to a URL you configure. Typical end results range from a Slack notice to a full site redeployment.

Set up in Ghost Admin under Settings, Advanced, Integrations, then add a custom integration; the only required inputs for a webhook are the trigger event and target URL.

Events in the docs table: `site.changed` (any content or settings change); `post.added`, `post.deleted`, `post.edited`, `post.published`, `post.published.edited`, `post.unpublished`, `post.scheduled`, `post.unscheduled`, `post.rescheduled`; the same nine for pages (`page.added` and so on); `tag.added`, `tag.edited`, `tag.deleted`; `post.tag.attached`, `post.tag.detached`, `page.tag.attached`, `page.tag.detached`; `member.added`, `member.edited`, `member.deleted`.

Delivery: a 2xx response means success. Anything else counts as a failure and the response body is discarded. The target URL must be reachable from the Internet.

Stripe (local Ghost): the page also covers Stripe webhooks. Run `stripe listen --forward-to http://localhost:2368/members/webhooks/stripe/` (match the port of your local install), then start Ghost with the returned `whsec_` secret: `WEBHOOK_SECRET=whsec_... ghost start`.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 74 lines, code samples inline, no imported snippets): webhooks.mdx. Setup path, required fields and 2xx rule match. Removed as unconfirmed: the static-site `site.changed` rebuild pattern, the "typical end results" wording beyond Slack notice and redeployment, and the Verify step. Completed the event list (the draft covered only part of the table) and added the Stripe local setup. Retry behaviour, headers and payload shape are not on this page and are not claimed.
Method: documentation only; no commands were run.
