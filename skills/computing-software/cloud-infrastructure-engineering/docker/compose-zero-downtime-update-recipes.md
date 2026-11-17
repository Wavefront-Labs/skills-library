---
id: computing-software.cloud-infrastructure-engineering.docker.compose-zero-downtime-update-recipes
name: compose-zero-downtime-update-recipes
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, docker-compose, zero-downtime, compose-production, rolling-update, healthcheck, compose-wait, scale, one-at-a-time, reverse-proxy, blue-green, rollback, single-host-deploy, compose-scale, no-downtime]
level: advanced
status: gated
description: "Update Compose services without downtime: scale past one instance, healthchecks with --wait, staggered recreation behind a proxy, and Compose limits versus Swarm."
sources: ["https://docs.docker.com/reference/cli/docker/compose/up/", "https://docs.docker.com/compose/how-tos/production/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zero-downtime updates with Compose

**Goal:** push a new image of a service on a single Compose host without a window where nothing
serves.

**State the constraint first, because the ecosystem soft-pedals it:** Compose has no rolling-update
mechanism. The `up` reference documents no sequencing or concurrency semantics for recreation - it
"picks up the changes by stopping and recreating the containers (preserving mounted volumes)", and
that is all. A single-instance service therefore has a real gap between old-container-stop and
new-container-healthy. Everything below exists to manufacture redundancy around that gap; if you
need true rolling updates, the documented path is Swarm or Kubernetes.

## The recipe
1. **Run at least two instances** of the service being updated. `--scale` "scales SERVICE to NUM
   instances" and overrides the Compose file's `scale:`:
   ```bash
   docker compose up -d --scale web=2
   ```
2. **Make healthchecks real** - they are what makes `--wait` meaningful:
   ```yaml
   services:
     web:
       image: app:1.4.2
       healthcheck:
         test: ["CMD", "/app/healthcheck"]
         interval: 5s
         timeout: 3s
         retries: 3
   ```
3. **Front the instances with a proxy** that health-checks and drops unhealthy backends (any
   reverse proxy with active checks; the existing
   `frontend-development` / proxy skills cover the proxy side). One instance can then go away while
   the other serves.
4. **Update one instance at a time**, explicitly, since `up -d` will not do it for you:
   ```bash
   docker compose pull web                       # fetch first so the swap is fast
   docker stop app-web-2 && docker rm app-web-2  # remove ONE instance
   docker compose up -d --no-deps web            # recreates what is missing
   docker compose up -d --wait --wait-timeout 120  # until healthy
   # repeat for the other instance
   ```
   `--no-deps` avoids dragging dependencies into the churn. `--pull always|missing|never` sets the
   pull policy explicitly rather than relying on the default.
5. **Rollback is a tag change**: point the image back at the previous tag and re-run `up -d`.

`--wait` "waits for services to be running|healthy", `--wait-timeout` bounds it, `--no-recreate`
prevents Compose picking up changes, `--force-recreate` forces recreation even without changes, and
`--remove-orphans` cleans services no longer defined. `--always-recreate-deps` exists but is
incompatible with `--no-recreate`.

## Failure modes
- **Downtime anyway** - still running one instance; `up -d` stopped it before starting the new one.
  The redundancy has to exist *before* the update starts.
- **Proxy keeps sending to a dead backend** - no active health-checking between proxy and
  containers; the gap you manufactured redundancy for is re-opened at the proxy layer.
- **`--wait` passes instantly on a broken app** - the healthcheck is trivial (`true`) or missing, so
  "running" satisfies the wait without "healthy".
- **Both instances replaced at once** - running plain `up -d` on a changed image rather than the
  one-at-a-time sequence; Compose recreates them together.
- **Old containers linger** - no `--remove-orphans`, or the manual `stop`/`rm` step was skipped and
  the proxy round-robins onto a stale instance.
- **Hung shutdown** - no `-t/--timeout` on the stop path for a service that ignores SIGTERM; the
  proxy marks it down long before the container actually exits.

## Verify
- [ ] A continuous request stream against the proxy stays green through a full update cycle of the
      service - that is the actual definition of zero-downtime, so measure it, do not assume it.
- [ ] At every moment of the cycle, at least one healthy instance is behind the proxy.
- [ ] The healthcheck fails fast enough that `--wait --wait-timeout` catches a bad image within the
      timeout, and the rollback tag swap has been rehearsed.
- [ ] Scale is back to the intended steady-state count after the update.
- [ ] The moment you need real rolling updates across hosts, the handoff is planned (Swarm or
      Kubernetes) rather than improvised on this single-host recipe.

*`--scale`, `--wait`, `--wait-timeout`, `--no-deps`, `--no-recreate`, `--force-recreate`, `--pull`
and the recreation semantics verified against the Compose CLI reference on 2026-11-01. The
two-instance-behind-a-proxy recipe is engineering practice built on those primitives, not a
Docker-documented procedure. Nothing was executed, so `status: draft`.*

## Checked

- Date: 2026-11-02.
- Confirmed against: docker compose up flags --scale, --wait, --wait-timeout, --no-recreate, --force-recreate, --no-deps and the production how-to (Docker docs: compose up reference, production guide).
- Not confirmed: the healthcheck command in the example and the exact wording of the -t/--timeout flag (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
