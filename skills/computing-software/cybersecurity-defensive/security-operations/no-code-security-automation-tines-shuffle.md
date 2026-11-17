---
id: computing-software.cybersecurity-defensive.security-operations.no-code-security-automation-tines-shuffle
name: no-code-security-automation-tines-shuffle
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [tines, shuffle, soar-automation, no-code-automation, webhooks, security-automation, workflows]
level: practitioner
status: draft
description: "Build no-code/low-code security automations with Tines or Shuffle: stories/workflows, webhooks, HTTP actions, credentials, error handling and testing."
sources: ["https://www.tines.com/docs", "https://shuffler.io/docs", "https://www.tines.com/docs/actions/types/http-request"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# No-code automation with Tines or Shuffle

## Tines
- A **story** is a flow of **actions**: Webhook (trigger), HTTP Request, Event Transform
  (message-only/extract/deduplicate/implode/explode), Trigger (conditions), Send Email, Send to Story
  (sub-flow), AI action.
- Credentials stored centrally (`<<CREDENTIAL.virustotal>>` placeholders); resources for config
  values (`<<RESOURCE.allowlist>>`).
- Pages for analyst-facing forms (approve/deny, input), cases for lightweight case management.
- Formulas (`=` expressions) for data manipulation; avoid JSON gymnastics in multiple transforms.
- Change control: story versions, drafts, change requests for production stories.

## Shuffle (open source)
- Workflows of apps (OpenAPI-generated) with triggers (webhook, schedule, user input), conditions
  and variables; self-hosted with Orborus/workers in Docker.
- Apps generated from OpenAPI specs for APIs lacking connectors.

## Typical story: phishing report enrichment
Webhook from mailbox -> extract URLs/attachments -> explode list -> URL scan / VirusTotal lookups
(HTTP actions with rate-limit retry) -> implode -> decide (any malicious?) -> create ticket and
reply to reporter; malicious path blocks sender and purges messages after analyst approval page.

## Engineering practice
- Deduplicate inputs early to save API quota.
- Error paths on HTTP actions (retry with backoff on 429/5xx, then notify).
- Test with recorded sample events; keep a test copy of each story.
- Secrets never in action bodies; use credential store.

## Gotchas
- Webhook URLs are secrets; rotate if leaked and validate shared secrets/HMAC.
- Loops over large lists consume event quotas; batch.
- Tenant-level rate limits; monitor action failure rates.

## Verify
Send a known-malicious and a benign sample through the story; both paths end in the right outcome
with all actions succeeding and audit log entries recorded.
