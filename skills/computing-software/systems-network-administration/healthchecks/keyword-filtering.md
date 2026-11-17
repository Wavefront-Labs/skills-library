---
id: computing-software.systems-network-administration.healthchecks.keyword-filtering
name: keyword-filtering
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, keyword-filtering, success-keywords, failure-keywords, default-fail]
level: advanced
status: docs-checked
description: "Classify Healthchecks pings as start, success or failure by matching keywords in HTTP bodies or email subjects and bodies, with match order and no-match handling."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/configuring_checks.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Content filtering decides a ping's meaning from its text. Enable it separately for HTTP request bodies, email subject lines and email message bodies (HTML emails are checked as plain text and as HTML).

There are three comma-separated keyword lists: start, success and failure. Matching is case-sensitive. Order of evaluation: failure, then success, then start; the first match wins.

If nothing matches, "If no keywords match" either ignores the ping or classifies it as failure. Ignored pings appear in the event log as "Ignored" and do not change status.

Docs example: a backup job POSTs when finished. Set "Backup successful" as a success keyword and treat no-match as failure; only bodies containing that phrase count as success.

API fields: `start_kw`, `success_kw`, `failure_kw` (comma-separated, case-sensitive), `filter_subject`, `filter_body`, `filter_http_body`, and `filter_default_fail` (false ignores non-matches, true counts them as failures).

Useful when appending a suffix to the ping URL on the client is not feasible.

## Checked

2026-11-04: confirmed against the Configuring Checks page (order failure, success, start; case-sensitive; no-match handling; Ignored label; Backup successful example) and the Management API page (field names and defaults). Removed a deprecation claim for `subject` and `subject_fail` that the page does not make.
Method: documentation only; no commands were run.
