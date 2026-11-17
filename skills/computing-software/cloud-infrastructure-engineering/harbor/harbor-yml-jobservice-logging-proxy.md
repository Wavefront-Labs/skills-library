---
id: computing-software.cloud-infrastructure-engineering.harbor.harbor-yml-jobservice-logging-proxy
name: harbor-yml-jobservice-logging-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [harbor-yml, jobservice-workers, rsyslog, proxy-settings, redis-cache]
level: practitioner
status: docs-checked
description: "Tune jobservice workers, job loggers, webhook retries, rsyslog retention, outbound proxy and the Redis cache layer in harbor.yml."
sources:
  - https://goharbor.io/docs/main/install-config/configure-yml-file/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Other required `harbor.yml` blocks:

**jobservice**
- `max_job_workers`: concurrent replication workers, default 10. Each worker consumes network, CPU and IO, so size it to the host.
- `job_loggers`: any of `STD_OUTPUT`, `FILE`, `DB`. It is required: `prepare` fails with `KeyError: 'job_loggers'` if missing. The template enables `STD_OUTPUT` and `FILE`.
- `logger_sweeper_duration`: days job logs are kept; applies to the `FILE` and `DB` loggers. The template sets 1.

**notification**
- `webhook_job_max_retry`: default 10.
- `webhook_job_http_client_timeout`: seconds; the template sets 3.

**log** (rsyslog collects each container log)
- `level`: debug, info, warning, error or fatal; default info.
- `local.rotate_count` (default 50; 0 removes rather than rotates), `local.rotate_size` (default 200M; accepts k, M, G) and `local.location` (default `/var/log/harbor`).
- `external_endpoint` with `protocol` (default TCP), `host` and `port` forwards to a syslog server.

**proxy**: `http_proxy`, `https_proxy`, `no_proxy` for trivy-adapter, replication jobservice and Harbor. With Trivy, whitelist `github.com`, `github-releases.githubusercontent.com` and `*.s3.amazonaws.com`.

**cache**: `enabled` (default false) and `expire_hours` (default 24). It caches artifacts, projects and metadata in Redis and is recommended for high concurrent pull rates.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Configure the Harbor YML File.
Method: documentation only; no commands were run.
