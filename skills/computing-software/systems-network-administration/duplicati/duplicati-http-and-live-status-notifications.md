---
id: computing-software.systems-network-administration.duplicati.duplicati-http-and-live-status-notifications
name: duplicati-http-and-live-status-notifications
category: computing-software
field: systems-network-administration
product: duplicati
tags: [http-notifications, send-http-json-urls, send-http-form-urls, live-status-report, http-report-status-url, send-http-retries]
level: practitioner
status: docs-checked
description: "Post Duplicati results to webhooks as form or JSON bodies with retries and certificate options, and stream live progress to a dashboard URL."
sources: ["https://docs.duplicati.com/detailed-descriptions/monitoring-and-notifications/sending-reports-via-email/sending-http-notifications", "https://docs.duplicati.com/detailed-descriptions/monitoring-and-notifications/sending-reports-via-email/sending-live-status-reports"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTP notifications and live status reports

HTTP is the most versatile reporting option. By default the message is a form-url-encoded body in a request to the URL you supply. Configurable: message body and type (JSON is supported), the HTTP verb, conditions on when to send and which log elements to include. Message content can be customized.

From 2.0.9.106 several URLs can be given with `--send-http-form-urls=` and `--send-http-json-urls=`, which also lets you send both the text and JSON forms.

Failures are retried `--send-http-retries` times (default 3) with `--send-http-retry-delay` (default 1s) between tries. For a self-signed certificate use `--send-http-accept-specified-ssl-hash=<sha1 hash>` to trust that one certificate; `--send-http-accept-any-ssl-certificate` trusts any and is for testing only.

Live status reports (2.4.0.0 and later) differ: other modules send when an operation ends, while this one posts the state of a running operation at intervals, suited to dashboards. It is inactive until `--http-report-status-url=https://dashboard.example.com/duplicati` is set; several URLs are separated by semicolons. At most once per `--http-report-status-interval` (default 30s), and once more at completion, Duplicati posts JSON with the operation, status, startedUtc, reportedUtc, isCompleted, backendEvents, a progress object (phase, progress, filesProcessed, fileCount, activeTransfers and so on), recentLogLines and metadata (duplicatiVersion, machineId, backupId, backupName, machineName, destinationType, operatingSystem).

## Checked

2026-11-04. Confirmed against the Sending HTTP notifications and Sending live status reports pages. Replaced the unsupported claim that message content uses the same templates as email with a neutral pointer to message customization.

Method: documentation only; no commands were run.
