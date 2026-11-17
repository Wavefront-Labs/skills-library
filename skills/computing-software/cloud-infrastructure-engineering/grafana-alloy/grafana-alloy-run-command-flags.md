---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-run-command-flags
name: grafana-alloy-run-command-flags
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [alloy-run, serverhttplisten-addr, storagepath, stabilitylevel, config-reload, disable-reporting, ui-path-prefix]
level: practitioner
status: docs-checked
description: "Reference for alloy run: config path or directory, HTTP listen address, storage path, stability levels, reload via SIGHUP or /-/reload, and key flags."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/cli/run.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# alloy run

```shell
alloy run [FLAG ...] /path/to/config.alloy
```
The path argument is required. A directory loads all `*.alloy` files (nested directories ignored) as one configuration; component names must be unique across files and blocks must not repeat. Alloy exits on an unloadable initial config, but keeps running its last valid state if a later reload fails.

## Key flags
- `--server.http.listen-addr` (default `127.0.0.1:12345`) serves metrics and the debug UI at `/`.
- `--server.http.ui-path-prefix` (default `/`), `--server.http.enable-pprof` (default `true`), `--server.http.disable-support-bundle` (default `false`).
- `--server.http.memory-addr` (default `alloy.internal:12345`) for in-memory traffic.
- `--storage.path` (default `data-alloy/`): component data directory.
- `--disable-reporting`: turn off usage reporting.
- `--feature.community-components.enabled` (default `false`) and `--feature.component-shutdown-deadline` (default `10m`).
- `--windows.priority`: public preview, Windows only.

## Stability
`--stability.level` accepts `generally-available` (default), `public-preview`, `experimental`. Raising it can enable experimental behaviour even on otherwise GA items. Experimental flags such as `--server.http.enable-graphql` require `experimental`.

## Reload
POST to `/-/reload` or send `SIGHUP`. Removed components stop, new ones start, all are reevaluated.

## Convert on the fly
`--config.format` (`alloy`, `otelcol`, `prometheus`, `promtail`, `static`) converts a foreign config and runs it; `--config.bypass-conversion-errors` and `--config.extra-args` adjust conversion.

## Checked
2026-11-04: confirmed against the alloy run CLI reference. Removed: nothing.
Method: documentation only; no commands were run.
