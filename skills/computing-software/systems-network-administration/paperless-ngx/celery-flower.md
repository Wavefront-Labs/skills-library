---
id: computing-software.systems-network-administration.paperless-ngx.celery-flower
name: celery-flower
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, celery, flower, monitoring, task-queue, custom-container-init]
level: advanced
status: docs-checked
description: "Monitor Celery workers with Flower, understand the webserver, consumer and task processor split, and run custom init scripts in the container."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/usage/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Architecture, Flower and init scripts

## Components
- Webserver: UI, API and admin, run with granian.
- Consumer: `document_consumer` watches the folder and only notifies the task processor.
- Task processor: Celery. It consumes documents (including uploads and mail), checks mail, and maintains the search index and classifier on a schedule.

## Flower
Flower shows running, queued and completed tasks and timing, and exports Prometheus metrics. Enable it in Docker by defining the variable and exposing its port (default 5555):
```yaml
environment:
  - PAPERLESS_ENABLE_FLOWER
ports:
  - 5555:5555
volumes:
  - /path/to/flowerconfig.py:/usr/src/paperless/src/paperless/flowerconfig.py:ro
```
Put extra configuration in `flowerconfig.py` (placed in `src/paperless`). Flower runs on port 5555 by default, but this can be configured. The `:ro` flag mounts the file read-only.

## Custom initialisation
Mount scripts into `/custom-cont-init.d` to run them at startup, for example to install tools.
```yaml
volumes:
  - /path/to/scripts:/custom-cont-init.d:ro
```
- The folder must be owned by root with permissions `a=rx`; scripts must be writable only by root.
- They run as root just before the webserver finishes starting. Use `gosu` to drop privileges.
- If something breaks, disable them first before filing a bug.

Parser plugins can be installed the same way: a Python package under the `paperless_ngx.parsers` entry point group. They are not officially supported.

## Checked
2026-11-04. Compared with the Architecture section of usage, Celery Monitoring, Custom Container Initialization and parser plugin sections of advanced_usage, and PAPERLESS_ENABLE_FLOWER in configuration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: webserver, consumer and task processor roles, Flower features and Prometheus export, the compose snippet, port 5555 default, /custom-cont-init.d ownership and permission rules, root execution and gosu, the disable-before-reporting advice, parser plugin entry point group and unsupported status. Removed: the "do not publish the port publicly" warning (not on the pages).

Method: documentation only; no commands were run.
