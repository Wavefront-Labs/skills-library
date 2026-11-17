---
id: computing-software.systems-network-administration.paperless-ngx.low-power-tuning
name: low-power-tuning
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, raspberry-pi, performance, task-workers, ocr-pages, low-power]
level: practitioner
status: docs-checked
description: "Tune Paperless-ngx for Raspberry Pi class hardware by trimming workers, OCR scope, cleaning and archive generation."
sources:
  - "https://docs.paperless-ngx.com/setup/"
  - "https://docs.paperless-ngx.com/faq/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running on low-powered devices

Paperless runs on a Raspberry Pi (arm64 Docker images exist), but OCR is slow. These settings help:

- Stay on SQLite to save resources; the troubleshooting page covers SQLite locking.
- `PAPERLESS_CONSUMER_DISABLE=true` if you never use the consumption folder.
- `PAPERLESS_OCR_PAGES=1` OCRs only the first page, usually enough to find a document.
- `PAPERLESS_TASK_WORKERS` and `PAPERLESS_THREADS_PER_WORKER` are described on the setup page as configured to use all cores: on a four-core Pi, 2 workers with 2 threads, which can make the system sluggish during consumption. The example there is 2 workers and 1 thread. The configuration reference lists `PAPERLESS_TASK_WORKERS` as defaulting to 1, and says the product of workers and threads should not exceed your core count.
- Keep `PAPERLESS_OCR_MODE=auto` and, if possible, OCR documents before they arrive (some scanners can).
- `PAPERLESS_ARCHIVE_FILE_GENERATION=never` skips archive creation, saving disk space at the cost of in-browser PDF/A viewing.
- `PAPERLESS_OCR_CLEAN=none` speeds OCR and uses less memory with slightly worse results.
- `PAPERLESS_WEBSERVER_WORKERS=1` saves memory in Docker.
- `PAPERLESS_WORKER_TIMEOUT` (default 1800 seconds) can be raised if large documents time out.

## Classifier cost
Retraining the automatic matcher takes noticeable CPU. Training only does the heavy work if your data changed; you can move the schedule to daily in the admin interface. Matching itself is fast.

## Checked
2026-11-04. Compared with Running Paperless-ngx on less powerful devices in setup, the Raspberry Pi entries in the FAQ, and the worker, timeout and archive settings in configuration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: every bullet, arm64 images, 1800 second timeout, classifier schedule note. Reworded the workers bullet because setup and configuration differ on the default, and replaced the cross-reference to a locked-database skill with the troubleshooting page.

Method: documentation only; no commands were run.
