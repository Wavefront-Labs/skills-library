---
id: computing-software.devops-ci-cd.gitlab-runner.runner-config-toml-global
name: runner-config-toml-global
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [config-toml, concurrent, check-interval, shutdown-timeout, listen-address]
level: practitioner
status: docs-checked
description: "Global settings at the top of config.toml and their defaults."
sources: ["https://docs.gitlab.com/runner/configuration/advanced-configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Global settings in config.toml

The settings above the first `[[runners]]` section apply to the whole runner process.

- `concurrent`: the maximum number of jobs run at once across all runners on the host. `0` is not allowed.
- `check_interval`: seconds between polls for new jobs; default `3`.
- `connection_max_age`: how long a TLS keepalive connection to GitLab stays open before reconnecting; default `15m`.
- `shutdown_timeout`: seconds until the forceful shutdown operation times out and the process exits; default `30`.
- `listen_address`: `<host>:<port>` the Prometheus metrics HTTP server listens on.
- `log_level` (`debug`, `info`, `warn`, `error`, `fatal`, `panic`) and `log_format` (`runner`, `text`, `json`; default `runner`). Command-line arguments take priority over both.

The runner checks the file for changes every 3 seconds and reloads it; `SIGHUP` also forces a reload. `concurrent` together with each runner's `limit` and `request_concurrency` controls job flow; see the concurrency skill.

## Checked

2026-11-03. Confirmed against global settings table and reload behaviour on Advanced configuration. Removed: the unsourced advice to protect the file as a secret; reworded connection_max_age and shutdown_timeout to the page's wording.

Method: documentation only; no commands were run.
