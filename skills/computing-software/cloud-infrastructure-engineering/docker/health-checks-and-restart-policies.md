---
id: computing-software.cloud-infrastructure-engineering.docker.health-checks-and-restart-policies
name: health-checks-and-restart-policies
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, healthcheck, docker-healthcheck, restart-policy, restart-always, restart-on-failure, restart-unless-stopped, backoff, depends_on-condition, service_healthy, compose-healthcheck, liveness-vs-readiness, flapping-container]
level: practitioner
status: docs-checked
description: "Writing a Dockerfile HEALTHCHECK and restart policy pair that catches real failures: interval/timeout/retries tuning, Compose depends_on condition wiring, and the backoff/flapping trap."
sources: ["https://docs.docker.com/reference/dockerfile/#healthcheck", "https://docs.docker.com/reference/cli/docker/container/run/#restart", "https://docs.docker.com/reference/compose-file/services/#depends_on", "https://docs.docker.com/reference/api/engine/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Health checks and restart policies

**Goal:** `docker ps` says `healthy`/`unhealthy` based on something that actually
correlates with "can serve a request," and a crash loop fails loudly instead of quietly
restarting forever and burning CPU/log volume.

## HEALTHCHECK — what it's actually for
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/healthz || exit 1
```
- Exit `0` healthy, `1` unhealthy, `2` reserved (Docker says not to use it).
- `--start-period` is grace time during which failures don't count toward `--retries` —
  useful for anything with real startup time (JVM warmup, migrations-on-boot). A success during the start period ends it, after which consecutive failures count.
- `--retries` consecutive failures (not total) before the container flips to `unhealthy` —
  tune against your actual failure latency tolerance, not a default guess.
- A container's health status is informational for the engine: restart policies react to the container exiting, not to health (see the autoheal skill for a restart helper). Compose's `depends_on: condition: service_healthy` uses health only to gate start order. This surprises people expecting automatic self-healing from `HEALTHCHECK` alone.

## Liveness vs readiness — one check, two different questions
A single `/healthz` endpoint conflating "is the process alive" (liveness) with "can it
currently serve traffic" (readiness — DB connection up, cache warm) causes two failure
modes: restarting a container that's alive but briefly can't reach its DB (making the
outage worse by resetting connections/in-flight work), or never restarting a genuinely
hung process because the liveness-style check only pings the HTTP listener, not the actual
work loop. Plain Docker only gives you one `HEALTHCHECK`; if you need both concepts, make
the check itself distinguish fast-recoverable dependency failures (return healthy, let it
retry internally) from the process actually being stuck (return unhealthy).

## Compose `depends_on` with a health condition
```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 10
```
The short `depends_on` form is equivalent to `condition: service_started`, which only waits for the dependency to be started, not ready. With `service_healthy`, Compose waits for the dependency's healthcheck to pass before creating the dependent service.

## Restart policies and the backoff/flapping trap
`--restart=on-failure:5` stops trying after the container exits non-zero more than 5 times in a row (the limit is valid only for `on-failure`; by default Docker never stops trying). `always` and `unless-stopped` restart indefinitely. A delay that starts at 100 ms and doubles each time (100, 200, 400, 800 ms, ...) up to a maximum of 1 minute is added before each restart, and it resets to 100 ms once a restarted container has run for at least 10 seconds. A container crash-looping under `always` shows as `Restarting`/`Up` in `docker ps`; watch `docker inspect --format '{{.RestartCount}}'` or `docker events` rather than only the current state.
- `on-failure` restarts only after a non-zero exit. `always` restarts a manually stopped container when the daemon restarts, whereas `unless-stopped` does not restart a container that was stopped, even after a daemon restart. `docker update --restart=no` changes the policy of an existing container.

## Gotchas
- The check command runs inside the container, so `curl` or `wget` must exist in the image; distroless and scratch images need a different check, such as a small static binary in exec form.
- Keep the check cheap and side-effect-free; a check that exceeds `--timeout` is killed with SIGKILL and counts as a failure.

## Verify
`docker inspect --format '{{json .State.Health}}' <id>` shows the expected
`Status`, `FailingStreak` and a `Log` of recent check results with exit codes and output.

## Checked

Checked against the Dockerfile reference (`HEALTHCHECK`), the `docker container run` reference ("Restart policies"), the `docker container update` reference, the Engine API swagger (`Health`, `FailingStreak`, `Log`, `RestartCount`) and the Compose Specification (`depends_on` conditions, `healthcheck`) (docker/docs latest commit 2026-10-23, Engine 29).

- Exit codes 0/1/2, start-period semantics, restart policy names and `on-failure[:max-retries]` behaviour, 100 ms doubling delay with a 1 minute maximum and reset after 10 seconds of running, `unless-stopped` versus `always`, `service_started` and `service_healthy`.
- Removed as unconfirmed: tooling-specific remarks about exit code 2, the claim about Compose being the most common cause of flaky local setups, the engine-version backoff remark and the file-descriptor exhaustion anecdote.

Method: documentation only; no commands were run.
