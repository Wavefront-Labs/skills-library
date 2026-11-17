---
id: computing-software.systems-network-administration.paperless-ngx.mail-rules
name: mail-rules
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, mail-rules, imap, mail-account, mail-fetcher, email-consumption]
level: practitioner
status: docs-checked
description: "Set up mail accounts and rules so Paperless-ngx consumes attachments, with rule actions, folder separators, processed mail tracking and fetch schedule."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/administration/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consuming email

Configure under Settings > Mail: first an account, then rules.

## How a rule runs
It connects, fetches mail matching folder, maximum age and filters, looks for consumable attachments, consumes them with the rule's metadata, then applies the rule action to mails that produced documents. Mail is checked once; non-matching mail is ignored. Attachment filename patterns allow wildcards and comma-separated lists.

## Actions
- Delete: removes the mail immediately; use with caution.
- Mark as read: later reads are ignored, so mail you read first is skipped.
- Flag: sets important; flagged mail is not consumed.
- Move to folder.
- Add custom tag (IMAP keyword): not all servers support it. For Apple Mail colours use `apple:green` and similar.

The action also runs if the consume itself later fails, so a failed consume can leave a document missing.

## Practical notes
- Rules run in the order shown in the admin; put a catch-all last that tags "Unknown mail document".
- Folder separators vary (`.`, `/`, `|`). If a folder is not found, Paperless logs all folders in the account.
- Mail is fetched every 10 minutes; change it with `PAPERLESS_EMAIL_TASK_CRON` or set `disable`. Run now with `mail_fetcher`.
- Processed mail is tracked by server UID under Mail > Processed Mails; delete an entry to reprocess it.
- `PAPERLESS_EMAIL_ALLOW_INTERNAL_HOSTS=false` blocks private IMAP hosts.

## Checked
2026-11-04. Compared with Incoming Email and Processed Mail in usage, Fetching e-mail in administration, and PAPERLESS_EMAIL_TASK_CRON and PAPERLESS_EMAIL_ALLOW_INTERNAL_HOSTS in configuration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: rule flow, check-once behaviour, wildcard patterns, every action and its caveat, Apple Mail tags, failed consume warning, rule order and catch-all, folder separators and logging, 10 minute fetch, disable, mail_fetcher, processed mail tracking, internal hosts setting. Nothing removed.

Method: documentation only; no commands were run.
