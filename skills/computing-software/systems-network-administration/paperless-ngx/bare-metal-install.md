---
id: computing-software.systems-network-administration.paperless-ngx.bare-metal-install
name: bare-metal-install
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, bare-metal, manual-install, dependencies, tesseract, linux]
level: advanced
status: docs-checked
description: "Prerequisites and first steps for running Paperless-ngx without Docker: Linux only, Python version support, system packages, broker and a service user."
sources:
  - "https://docs.paperless-ngx.com/setup/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bare metal installation basics

Bare metal is for advanced setups and packaging. Paperless runs on Linux only; Windows is not supported. It needs a supported Python (3.11 to 3.14 per the docs).

## System packages
- Core: `python3`, `python3-pip`, `python3-dev`, `fonts-liberation`, `gnupg`, `libpq-dev`, `default-libmysqlclient-dev`, `pkg-config`, `libmagic-dev`, `poppler-utils`.
- For OCRmyPDF: `unpaper`, `ghostscript`, `icc-profiles-free`, `qpdf`, `liblept5`, `libxml2`, `pngquant`, `zlib1g`, and `tesseract-ocr` 4.0.0 or newer plus the language packs you need (for example `tesseract-ocr-deu`).
- For building Python wheels: `build-essential`, `python3-setuptools`, `python3-wheel`.

## Services
Install a Redis-compatible broker (Valkey or Redis) and enable it at boot. Optionally install PostgreSQL and create a database, user and password. With SQLite, make sure the JSON1 extension is enabled.

## User and release
```bash
adduser paperless --system --home /opt/paperless --group
curl -O -L https://github.com/paperless-ngx/paperless-ngx/releases/download/vX.Y.Z/paperless-ngx-vX.Y.Z.tar.xz
tar -xf paperless-ngx-vX.Y.Z.tar.xz
```
Use the release archive, not a git clone, so the compiled frontend is included; a missing frontend leaves the UI stuck on "Loading".

Run it under systemd. The docs list four services: `webserver`, `consumer` (watches the input folder), `taskqueue` (background workers) and `scheduler` (periodic tasks such as email checking). The example service files are in the release's `scripts` folder.

## Checked
2026-11-04. Compared with the Bare Metal Install section of setup and the "stuck at Loading" entry of troubleshooting (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: Linux only, Python 3.11 to 3.14, both package lists, broker, optional PostgreSQL, SQLite JSON1 note, adduser command, release download and extract commands, git clone needing a compiled frontend and the Loading symptom. Corrected the closing line: the docs list four services (webserver, consumer, taskqueue, scheduler), not three.

Method: documentation only; no commands were run.
