---
id: computing-software.cloud-infrastructure-engineering.fluentd.storage-section-and-local-plugin
name: storage-section-and-local-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, storage-section, storage-local, persistent, autosave, state, pos-file]
level: practitioner
status: docs-checked
description: "Persist plugin state with the Fluentd storage section and the local JSON storage plugin: persistent, autosave, save_at_shutdown, path and root_dir."
sources:
  - https://docs.fluentd.org/configuration/storage-section
  - https://docs.fluentd.org/storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd storage section and storage_local
`<storage>` under `<source>`, `<match>` or `<filter>` lets plugins that support it keep internal state as key-value pairs. Some storage plugins take an argument, as in `<storage awesome_path>`. Core plugin using it: `in_sample`; third-party examples include `fluent-plugin-storage-redis` and `-mongo`.

Common parameters:
- `persistent` (default false): reload before and save after every operation, costing I/O each time. `local` raises a configuration error unless `@id` or `path` is given.
- `autosave` (default true) with `autosave_interval` (default 10); ignored when `persistent` is true.
- `save_at_shutdown` (default true).

`local` is the only built-in storage plugin; its own parameters are on its plugin page, which this skill does not cover.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/configuration/storage-section, https://docs.fluentd.org/storage and confirmed: storage section placement, common parameters and defaults, built-in local plugin, core and third-party plugin lists. Removed or reworded: the local plugin parameters (mode, dir_mode, pretty_print, conf.arg, multi-worker note) and the sample example, which neither page documents.

Method: documentation only; no commands were run.
