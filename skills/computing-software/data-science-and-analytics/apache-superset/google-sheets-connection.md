---
id: computing-software.data-science-and-analytics.apache-superset.google-sheets-connection
name: google-sheets-connection
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [google-sheets, service-account, spreadsheet, data-source, upload]
level: practitioner
status: docs-checked
description: "Connect Superset to Google Sheets with a service account: share sheets with client_email, impersonate_user caveat, and upload value formats."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/google-sheets.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use Google Sheets with a service-account credential and avoid identity surprises.

Service-account connections:
- When you configure Google Sheets with service-account JSON in the database dialog, share private spreadsheets with the service account's `client_email`.
- Both catalog validation and queries use the service account, not the Google identity of the administrator adding the spreadsheet. This applies when creating a connection and when editing its catalog.
- The dialog's stored `impersonate_user` flag does not enable domain-wide delegation for this credential path. A spreadsheet shared only with the administrator cannot be validated on that basis, even if the service account has domain-wide delegation. Creating an empty connection and editing it later does not change the identity used.

Upload values (data uploaded into a sheet):
- Date and datetime values are sent as ISO strings, not numeric nanosecond counts.
- Timezone-aware datetimes are converted to UTC and uploaded without a timezone suffix, so Sheets parses them as datetime cells with `USER_ENTERED` input. Example: `2024-03-01 00:30:00+02:00` is uploaded as `2024-02-29 22:30:00`. The original zone is not kept, so read these cells as UTC. Naive datetimes keep their clock time.
- Nullable integer columns keep integer values, and missing values become empty cells.
- Time-only values use `HH:MM:SS[.ffffff]` strings; durations are signed `H:MM:SS[.ffffff]` strings, with hours including days.

## Checked

2026-11-08: read google-sheets.mdx in full. Removed claims not on the page: connection setup steps, "view access" requirement, sharing-scope and caching advice, key rotation advice, and the shillelagh tag.
Method: documentation only; no commands were run.
