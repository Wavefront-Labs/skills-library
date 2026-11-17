---
id: computing-software.cloud-infrastructure-engineering.fluentd.config-file-directives-and-locations
name: config-file-directives-and-locations
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, config-file, source, match, filter, system, dry-run]
level: practitioner
status: docs-checked
description: "Fluentd config file locations by install type, the seven directives, event tag/time/record, process_name and validating with --dry-run."
sources:
  - https://docs.fluentd.org/configuration/config-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd config file basics
Config location: fluent-package uses `/etc/fluent/fluentd.conf`; td-agent (EOL) `/etc/td-agent/td-agent.conf`; gem install: `fluentd --setup /etc/fluent` then edit `fluent.conf`; Docker default `/fluentd/etc/fluent.conf`. Override with `FLUENT_CONF` or `-c`. File must be UTF-8 or ASCII. `SIGHUP` reloads the config.

Directives: `source` (inputs), `match` (outputs), `filter` (processing pipeline), `system` (system-wide), `label` (internal routing group), `worker`, `@include`.

- Each `source` needs `@type`; each `match` needs a pattern plus `@type`.
- An event is **tag** (dot-separated, drives routing), **time** (Unix time, set by the input) and **record** (JSON object).
- Tags: the docs strongly recommend `^[a-z0-9_]+$` per part because outputs may reuse the tag as table or key names.
- Filters chain: Input -> filter 1 -> ... -> filter N -> Output.
- `system` can set `log_level`, `suppress_repeated_stacktrace`, `emit_error_log_interval`, `suppress_config_dump`, `without_source`, and `process_name` (system directive only; renames the supervisor and worker processes in `ps`).

Validate without starting plugins:
```
fluentd --dry-run -c fluent.conf
```

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/configuration/config-file and confirmed: config locations, directives, tag guidance, system parameters, process_name, --dry-run. Removed or reworded: nothing.

Method: documentation only; no commands were run.
