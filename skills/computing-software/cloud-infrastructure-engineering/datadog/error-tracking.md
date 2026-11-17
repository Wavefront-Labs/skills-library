---
id: computing-software.cloud-infrastructure-engineering.datadog.error-tracking
name: error-tracking
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, error-tracking, issues, stack-traces, source-maps]
level: practitioner
status: docs-checked
description: "Triage grouped errors in Datadog Error Tracking by issue state, upload JavaScript source maps with datadog-ci, and alert on new or high-impact issues."
sources: ["https://docs.datadoghq.com/error_tracking/issue_states/", "https://docs.datadoghq.com/real_user_monitoring/guide/upload-javascript-source-maps/", "https://docs.datadoghq.com/monitors/types/error_tracking/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error Tracking
Goal: triage application errors by issue instead of by log line.

Error Tracking groups errors from web, mobile and backend applications into issues. Issue states: FOR REVIEW (every issue starts here), REVIEWED, RESOLVED, IGNORED (optionally snoozed) and EXCLUDED (stops collecting new errors and no longer counts toward usage or billing).

- Automatic review: an issue becomes REVIEWED when it is assigned or a work item is created from it.
- Automatic resolution: if an issue was last reported in a version more than 14 days old and a newer version no longer reports it; without `version` tags, if there are no new errors for 14 days. Set version tags on APM, RUM and logs so this works.
- Regressions re-open issues (see Regression Detection) and return to FOR REVIEW.
- Error Tracking monitor (Monitors > New Monitor > Error Tracking): "New Issue" alerts when an issue occurs for the first time or regresses (issues in FOR REVIEW), "High Impact" alerts on the number of impacted users. Pick All, Browser, Mobile or Backend issues and filter with the Error Tracking Explorer search syntax.

Source maps for minified JavaScript (CI step, once per service):

```bash
export DD_API_KEY=<DD_API_KEY>
datadog-ci sourcemaps upload /path/to/dist \
  --service my-service \
  --release-version v35.2395005 \
  --minified-path-prefix https://hostname.com/static/js
```

- Sites other than US1 also need the site configured (the docs use `DATADOG_SITE` and `DATADOG_API_HOST` for this form).
- `--service` and `--release-version` must match the `service` and `version` tags on the Error Tracking, RUM and browser log events. Your server or CDN must serve the files at the `--minified-path-prefix` path.
- Alternative with debug IDs: run `datadog-ci sourcemaps inject /path/to/dist` after the build, then `datadog-ci sourcemaps upload /path/to/dist --debug-id`; do not pass `--service`, `--release-version` or `--minified-path-prefix` with `--debug-id`. Inject modifies bundles in place, so deploy the same artifacts you upload.
- Re-uploading a source map does not override an existing one if the version has not changed.

Gotcha: the API key variable for datadog-ci is `DD_API_KEY`; use a dedicated key stored as a CI secret.

## Verify
- A thrown test error appears as an issue with a de-minified stack trace.

## Checked
2026-11-03. Confirmed against the Issue States, JavaScript source maps and Error Tracking monitor pages. Fixed: the draft told the reader to keep `DATADOG_API_KEY` in CI, but the docs name the variable `DD_API_KEY`. Removed: the draft's `shop.example.net` command, the GitHub source code integration statement (unconfirmed), and daily triage advice.
Method: documentation only; no commands were run.
