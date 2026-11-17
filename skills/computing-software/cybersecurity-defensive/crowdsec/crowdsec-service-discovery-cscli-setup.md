---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-service-discovery-cscli-setup
name: crowdsec-service-discovery-cscli-setup
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [cscli-setup, service-discovery, detect-yaml, acquis-d, unattended]
level: practitioner
status: docs-checked
description: "Auto-detect services and generate acquisition files with cscli setup, and avoid clobbering hand-managed acquisition files."
sources: ["https://docs.crowdsec.net/docs/log_processor/service-discovery-setup/intro"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Service discovery detects supported services on the machine, installs the matching Hub items and generates acquisition configuration. Use `cscli setup interactive` or `cscli setup unattended`. It reads the detection file shipped with CrowdSec (`/var/lib/crowdsec/data/detect.yaml`). Interactive mode asks for confirmation before each change; Linux deb and rpm packages call `cscli setup unattended` at install time.

## Generated files

It writes one file per service, `setup.<name>.yaml`, in the acquisition directory (typically `/etc/crowdsec/acquis.d`), with a header holding a checksum.

- A file with a valid checksum is treated as generated and may be overwritten later.
- A file without one is treated as manually edited. Interactive mode shows a diff and asks; unattended mode refuses to proceed.
- cscli asks for confirmation if an `acquis.yaml` exists, there is any non-generated file in `acquis.d`, or generated files were modified. In unattended mode it skips service detection instead.

Do not edit generated files. Delete the generated `setup.<name>.yaml` and write your own, or use a custom `detect.yaml`.

## Gotcha

`cscli setup` validates syntax but does **not** detect duplicate acquisition. With a custom `detect.yaml`, make sure no log is read twice with the same `type`, because that causes false positives.

## Options

`--acquis-dir` targets another directory, `--dry-run` prints what would be created, and `cscli setup detect --detect-config /path/to/detect.yaml` (or the `CROWDSEC_SETUP_DETECT_CONFIG` variable) selects a custom detect file; `--yaml` renders the plan as YAML instead of JSON.

## Checked

2026-11-03. Confirmed against the Service Discovery page: setup interactive/unattended, detect.yaml path, setup.<name>.yaml files and checksum rules, confirmation conditions, unattended skip, duplicate-acquisition warning, --acquis-dir, --dry-run, --detect-config, CROWDSEC_SETUP_DETECT_CONFIG, --yaml. Removed: nothing.

Method: documentation only; no commands were run.
