---
id: computing-software.web-development.eleventy.content-dates
name: content-dates
category: computing-software
field: web-development
product: eleventy
tags: [content-date, page-date, git-last-modified, date-sort, utc-dates]
level: practitioner
status: docs-checked
description: "Set Eleventy content dates in front matter or filenames, use git-based date values, and avoid off-by-one-day and out-of-order CI pitfalls."
sources:
  - https://www.11ty.dev/docs/dates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `date` key overrides the default (file creation date) and controls collection sort. Valid values:

- `"Last Modified"`, `"Created"` (default)
- `"git Last Modified"` (1.0.1+), the latest git commit; `"git Created"` (2.0.0+), the first commit with best-effort rename tracking. Uncommitted files get `Date.now()`. Both are resource intensive, so consider limiting them to CI via a JS data file and environment variables.
- a YAML date such as `2016-01-01` (no time means midnight UTC)
- an ISO 8601 string that Luxon `DateTime.fromISO` can parse

With no `date`, Eleventy looks for `YYYY-MM-DD` anywhere in the file path (first match; assumed UTC), then falls back to file creation date.

In templates use `page.date`; `date` holds the raw cascade value.

**Custom parsing** (3.0): `eleventyConfig.addDateParsing(callback)`. Callbacks run serially and may return a Luxon DateTime, a JS Date, a new value to parse, or falsy to ignore.

**Off by one day:** UTC midnight dates shown in a local zone look a day early. Print UTC: in Nunjucks `{{ page.date.toUTCString() }}`; in Liquid write a filter or pass a timezone like `{{ page.date | date: '%b %d, %Y', 'UCT' }}`.

**Out-of-order collections on CI:** creation dates can reset on a server. Set explicit dates or use `git Last Modified`.

## Checked

2026-11-04. Confirmed against the Eleventy Content Dates page: valid date values and their version gates (git Last Modified v1.0.1, git Created v2.0.0), Date.now() for uncommitted files, resource-intensive note, YAML dates at midnight UTC, Luxon fromISO strings, filename YYYY-MM-DD lookup (first match, UTC), creation-date fallback, page.date versus raw date, addDateParsing (v3.0, serial callbacks and return types), the UTC off-by-one fix for Nunjucks and Liquid, and CI out-of-order creation dates. Corrected the git Created version gate from 2.0.0-canary.13 to 2.0.0.

Method: documentation only; no commands were run.
