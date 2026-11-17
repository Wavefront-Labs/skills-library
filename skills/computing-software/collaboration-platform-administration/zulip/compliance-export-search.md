---
id: computing-software.collaboration-platform-administration.zulip.compliance-export-search
name: compliance-export-search
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [compliance-export, export-search, message-export]
level: practitioner
status: docs-checked
description: "Run a selective compliance export of Zulip messages with manage.py export_search by keyword, sender, recipient and time range to JSON or CSV, with attachments optional."
sources: ["https://zulip.readthedocs.io/en/latest/production/export-and-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compliance exports with export_search

When legal or corporate compliance needs selected messages rather than a whole organization, use `export_search`. You can filter by:

- keywords in the message text
- message sender or recipient
- a time range

Example, run from the current deployment, searching one organization for "wonderland" from a given sender between two timestamps:

```
~zulip/deployments/current/manage.py export_search --output compliance-export.json \
    -r zulip \
    --after '2022-11-01 00:00:00' --before '2022-11-06 14:00:00' \
    --sender alice@example.com \
    wonderland
```

Output goes to a JSON or CSV file. Two limits matter for legal accuracy:

- Earlier versions of edited messages are not searched.
- Deleted messages are not searched.

Attachments belonging to matching messages can optionally be exported with them.

Run `export_search --help` for the complete option list.

This is distinct from the full organization export, which carries all non-transient data. Keep the output files protected, since they contain message content.

## Checked

Confirmed against the Compliance exports section of the export-and-import page: the filter options (keywords, sender or recipient, time range), the example command, JSON or CSV output, the two limits (edited-message history and deleted messages not searched) and optional attachments. Removed the claim that -r takes the string ID (the page only shows -r zulip) and the single-user export aside (not on this page).

Method: docs-checked 2026-11-09 against docs/production/export-and-import.md in the zulip/zulip repository (main), the source of the cited page.
