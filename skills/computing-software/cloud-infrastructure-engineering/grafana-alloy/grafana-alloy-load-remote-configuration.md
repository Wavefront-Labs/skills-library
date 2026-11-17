---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-load-remote-configuration
name: grafana-alloy-load-remote-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [importhttp, poll-frequency, importgit, pull-frequency, remote-configuration, modules-remote]
level: practitioner
status: docs-checked
description: "Load Alloy config from remote sources: a local root file importing modules via import.http, import.git or import.file, versus remotecfg."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/configure/load-remote-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Loading configuration from remote sources

Alloy never starts from a bare URL. You always have a local config file, which either imports modules or connects to a remote config API.

| Method | Use |
| --- | --- |
| `import.http` | static module files on an HTTP server |
| `import.git` | versioned modules, supports private repos |
| `import.file` | local file or directory, watched for changes |
| `remotecfg` | server picks config by collector id and attributes |

## import.http
Alloy polls the URL (`poll_frequency`) and treats the body as a module, not a full config. Modules may hold only top-level `declare` and nested `import.*` blocks; `logging` or `remotecfg` inside a module is invalid, and CLI flags cannot be set in modules. Imported components run only if you instantiate them locally.

```alloy
import.http "remote" {
  url            = "http://CONFIG_SERVER/prometheus_scrape.alloy"
  poll_frequency = "5m"
}
remote.scrape "app" {
  targets    = [{"__address__" = "localhost:8080"}]
  forward_to = [prometheus.remote_write.default.receiver]
}
```
with the remote module declaring `declare "scrape" { argument "targets" {} argument "forward_to" {} prometheus.scrape "default" { ... } }`.

## import.git
```alloy
import.git "modules" {
  repository     = "https://github.com/ORG/REPO.git"
  revision       = "main"
  path           = "modules/prometheus.alloy"
  pull_frequency = "5m"
}
```

Use multiple import blocks for multiple modules. Choose `remotecfg` only for a compatible management server, never for static files.

## Checked

2026-11-08. Read the Load configuration from remote sources page in full. Confirmed: the local-file-first rule, the four methods and their uses, import.http module semantics and requirements (declare and nested import only, no logging or remotecfg, no CLI flags), the scrape module example, the import.git example with `pull_frequency`, import.file watching, and the remotecfg guidance.

Method: documentation only; no commands were run.
