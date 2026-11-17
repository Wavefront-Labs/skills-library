---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-migrate-from-promtail
name: grafana-alloy-migrate-from-promtail
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [migrate-promtail, lokisourcejournal, lokirelabel, localfile-match, positions-file, configformat-promtail]
level: practitioner
status: docs-checked
description: "Migrate Promtail to Alloy with alloy convert, including a systemd journal config using loki.source.journal and loki.relabel, and the limitations."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/set-up/migrate/from-promtail.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating from Promtail to Alloy

Promtail reached end of life on March 2, 2026, so migrate.

```shell
alloy convert --source-format=promtail --output=/path/to/config.alloy /path/to/promtail.yaml
```
Use `--report` for diagnostics and `--bypass-errors` for best-effort output. `alloy run --config.format=promtail` runs a Promtail file directly as a temporary step. A `static_configs` job with `__path__: /var/log/*.log` converts to `local.file_match` (`path_targets`), `loki.source.file` and `loki.write`.

## systemd journal
A Promtail `journal` job with `relabel_configs` mapping `__journal__systemd_unit` to `unit` becomes:

```alloy
loki.relabel "journal" {
  forward_to = []
  rule {
    source_labels = ["__journal__systemd_unit"]
    target_label  = "unit"
  }
}
loki.source.journal "read" {
  max_age       = "12h"
  relabel_rules = loki.relabel.journal.rules
  forward_to    = [loki.write.default.receiver]
  labels        = { job = "systemd-journal", host = "my-hostname" }
}
```
Add the `alloy` user to the `adm` and `systemd-journal` groups so it can read the journal.

## Limitations
- Tracing setup is not migrated; Alloy metrics and logs differ from Promtail's, so adjust alerts and dashboards.
- Extra command-line flags (for example `-max-line-size`) and environment variables (`JAEGER_AGENT_HOST`) are not carried over.
- The positions file lives in a different place; update any Persistent Volume setup.
- The converter assumes `pod` discovery is a DaemonSet, so adjust `discovery.kubernetes` for single-node discovery if you deploy differently.

## Checked
2026-11-04: confirmed against the Migrate from Promtail page. Removed: nothing.
Method: documentation only; no commands were run.
