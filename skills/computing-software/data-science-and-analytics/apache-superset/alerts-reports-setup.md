---
id: computing-software.data-science-and-analytics.apache-superset.alerts-reports-setup
name: alerts-reports-setup
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [alerts-reports, playwright, celery-beat, smtp, webdriver]
level: practitioner
status: docs-checked
description: "Set up Superset Alerts and Reports: feature flags, SMTP and webdriver settings, Celery beat entries, Playwright requirement, troubleshooting."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/alerts-reports.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get scheduled alerts and reports delivering.

Feature flags: `ALERT_REPORTS` must be `True`; also `ALERT_REPORT_SLACK_V2`, `ALERT_REPORT_WEBHOOK`, `ALERT_REPORT_DYNAMIC_EXECUTOR` (per-schedule "Run as"), `DATE_FORMAT_IN_EMAIL_SUBJECT`.

Core config:
- `ALERT_REPORTS_NOTIFICATION_DRY_RUN` is `True` in the dev config; set `False` to send real notifications.
- Email: `SMTP_HOST`, `SMTP_PORT`, `SMTP_STARTTLS`, `SMTP_SSL_SERVER_AUTH`, `SMTP_SSL`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_MAIL_FROM`, plus `EMAIL_REPORTS_SUBJECT_PREFIX`, `EMAIL_REPORTS_CTA`.
- `WEBDRIVER_BASEURL` is the internal URL the worker uses (e.g. `http://superset:8088`); `WEBDRIVER_BASEURL_USER_FRIENDLY` is the link sent to recipients.
- `WEBDRIVER_WINDOW` defaults to `{"dashboard": (1600, 2000), "slice": (3000, 1200), "pixel_density": 1}`.
- `SCREENSHOT_LOCATE_WAIT = 100`, `SCREENSHOT_LOAD_WAIT = 600`.

Celery beat must schedule `reports.scheduler` (`crontab(minute="*", hour="*")`) and `reports.prune_log` (`crontab(minute=0, hour=0)`). Run one or more workers and a single beat.

Requirements: Superset 7.0.0+ takes screenshots only through Playwright driving headless Chromium (Selenium and `WEBDRIVER_TYPE` are unsupported). Default images include Chromium; `-lean` and `-dev` do not (build with `INCLUDE_CHROMIUM=true docker compose build`). Only the worker needs the browser. Docker Compose needs Redis and PostgreSQL, not SQLite.

Worker command: `celery worker --pool=prefork --max-tasks-per-child=128`.

Troubleshooting: errors containing `Playwright is required for screenshots` or `Failed to launch the headless browser for screenshots`; check from the worker with `curl http://superset:8088/dashboard/1/`; log identifiers `ScreenshotBlankCaptureError`, `report_capture_validation`, `report_delivery_blocked`.

## Checked

2026-11-08. Confirmed against the Alerts and Reports page (read in full): feature flags, SMTP and webdriver settings, WEBDRIVER_WINDOW defaults, screenshot waits, beat_schedule entries, Playwright-only screenshots from 7.0.0, image variants, Compose requirements, worker command, error strings and log identifiers. Nothing removed.
Method: documentation only; no commands were run.
