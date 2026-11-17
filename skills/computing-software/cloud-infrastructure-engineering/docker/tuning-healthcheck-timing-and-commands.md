---
id: computing-software.cloud-infrastructure-engineering.docker.tuning-healthcheck-timing-and-commands
name: tuning-healthcheck-timing-and-commands
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, healthcheck, healthcheck-options, start-period, start-interval, healthcheck-command, healthcheck-without-curl, dockerfile]
level: practitioner
description: "Pick HEALTHCHECK --interval, --timeout, --start-period, --start-interval and --retries values and write probes that work in slim images without curl."
sources: ["https://docs.docker.com/reference/dockerfile/#healthcheck", "https://github.com/compose-spec/compose-spec/blob/main/spec.md#healthcheck"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tuning HEALTHCHECK timing and commands

## The options
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --start-interval=2s --retries=3 \
  CMD ["/app/healthcheck"]
```
| Option | Default | Meaning |
|---|---|---|
| `--interval` | 30s | time between checks once running |
| `--timeout` | 30s | a check taking longer counts as failed |
| `--start-period` | 0s | grace window: failures don't count toward retries; first success ends it |
| `--start-interval` | 5s | check frequency **during** start-period (Engine 25+) |
| `--retries` | 3 | consecutive failures to flip to `unhealthy` |

The first check runs `interval` after the container starts and then `interval` after each previous check completes; during the start period checks run every `start-interval` instead. A check that exceeds `timeout` counts as failed and the check process is killed with SIGKILL. The container becomes `healthy` whenever one check passes and `unhealthy` after `retries` consecutive failures. A success during the start period ends it, so a short `--start-interval` with a long `--start-period` gives fast readiness without frequent checks later.

Keep `timeout` well under `interval`, and size `start-period` for your slowest cold start.

## Exit codes
`0` healthy, `1` unhealthy. Exit `2` is reserved; never return it. Docker's example uses `|| exit 1`.

## Commands without curl
- **Whatever the image already has**: the check runs inside the container, so use a client that is present in the image (for example `wget` or `nc` where available) and end shell-form commands with `|| exit 1`.
- **App-native**: the database's own client, such as `pg_isready`, `redis-cli ping` or `mysqladmin ping`, or a `healthcheck` subcommand of your own binary. For distroless or scratch images ship a small static binary and use exec form.
- **Python images**: `CMD ["python", "-c", "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2)"]`

## Gotchas
- Shell form runs the command through the container's shell, which distroless and scratch images lack. Use exec form.
- Probe `127.0.0.1`, not `localhost` (may resolve to `::1` while the app binds IPv4 only).
- A health endpoint that checks the database makes every app container unhealthy when the DB
  blips; health should mean "this process works".
- Output the check writes to stdout or stderr is stored in the health status and shown by `docker inspect`; only the first 4096 bytes are kept, so keep it short.
- A `health_status` event is generated whenever the status changes.
- Compose: the same keys under `healthcheck:` (`test`, `interval`, `timeout`, `retries`, `start_period`, `start_interval`), durations as `"10s"`; `test` may be `["CMD", ...]`, `["CMD-SHELL", ...]`, a string (implies CMD-SHELL) or `NONE`, and `disable: true` turns off an image's check.

## Verify
```sh
docker inspect --format '{{json .State.Health}}' app
```

## Checked

Checked against the Dockerfile reference (`HEALTHCHECK`, from moby/buildkit `frontend/dockerfile/docs/reference.md`, current main) and the Compose Specification `healthcheck` section; docker/docs latest commit 2026-10-23, Engine 29.

- Option defaults (`--interval` 30s, `--timeout` 30s, `--start-period` 0s, `--start-interval` 5s needing Engine 25.0, `--retries` 3), start-period semantics, SIGKILL on timeout, exit codes 0/1/2, 4096-byte output limit, `health_status` event, Compose keys and `test` forms.
- Removed as unconfirmed: the worst-case timing formula, p99 and interval rules of thumb, the `wget`, bash `/dev/tcp` and `nc` command lines, the "last 5 results" claim and the `jq` pipeline.

Method: documentation only; no commands were run.
