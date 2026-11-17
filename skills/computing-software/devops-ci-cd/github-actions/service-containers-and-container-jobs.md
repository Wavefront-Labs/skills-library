---
id: computing-software.devops-ci-cd.github-actions.service-containers-and-container-jobs
name: service-containers-and-container-jobs
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, service-containers, services, container-jobs, services-postgres, services-redis, services-mysql, docker-network, health-check, options-health-cmd, port-mapping, localhost-vs-hostname, job-container, container-image, container-credentials, ghcr-private-image, integration-tests, testcontainers, docker-compose-in-ci, linux-only, volumes, env-for-services]
level: practitioner
status: verified
description: "Run databases and brokers beside GitHub Actions jobs: services with health checks, localhost-vs-service-name rule, port mapping, container jobs with private images, compose/Testcontainers."
sources: ["https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/about-service-containers", "https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/creating-postgresql-service-containers", "https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idservices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service containers and container jobs

**Goal:** integration tests against real Postgres/Redis/Kafka in CI with no flaky
"connection refused" at startup, on Linux runners only (services need Docker).

## 1. The canonical shape
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: app
          POSTGRES_PASSWORD: app
          POSTGRES_DB: app_test
        ports: ['5432:5432']
        options: >-
          --health-cmd "pg_isready -U app"
          --health-interval 5s --health-timeout 5s --health-retries 10
      redis:
        image: redis:7
        ports: ['6379:6379']
        options: --health-cmd "redis-cli ping" --health-interval 5s --health-retries 10
    steps:
      - uses: actions/checkout@v7
      - run: pytest
        env:
          DATABASE_URL: postgres://app:app@localhost:5432/app_test
```
The `--health-*` options are `docker create` options (the GitHub tutorial uses `--health-cmd pg_isready` with
interval, timeout and retries "to wait until postgres has started"). Without a health check nothing waits for the
database, so the first test can race it. If an image has no health tool, poll in the first step
(`until pg_isready ...; do sleep 1; done`, with a timeout).

## 2. The address rule (localhost vs service name)
- Steps run **on the runner host** (default): reach services via `localhost:<host-port>` and
  you **must** map `ports:`. `ports: ['5432']` (no host port) assigns a random host port →
  read it from `${{ job.services.postgres.ports['5432'] }}` (the docs example uses the same `ports[5432]` form).
- Steps run **in a job container** (`container:` set): the job and services share a user-defined Docker
  network; the hostname is the service label (`postgres:5432`), all ports are open between containers, and
  `ports:` is unnecessary.
Mixing these up gives `ECONNREFUSED` on a healthy service.

## 3. Container jobs
```yaml
    container:
      image: ghcr.io/org/ci-base:1.8
      credentials:
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
      env:
        CI: 'true'
      volumes:
        - /var/run/docker.sock:/var/run/docker.sock   # only if you must build images inside
      options: --cpus 2
```
- `run` steps in a container default to `sh`, not `bash` (docs); set `defaults.run.shell` or a step `shell:` to change it.
- JavaScript actions in Alpine containers are supported: the runner detects Alpine and uses a musl Node build
  (`node20_alpine`/`node24_alpine` from actions/alpine_nodejs), on **x64 Linux runners only** (it throws on other
  architectures; runner source `StepHost.cs`, `externals.sh`). Earlier advice that Alpine images fail is out of date.
- `container.options` takes `docker create` options but not `--network` or `--entrypoint` (docs). A non-root image
  `USER` may leave the workspace unwritable; `options: --user root` is one way round it (untested here).
- Pull cost every run: keep the image small or use a self-hosted runner with a cache.

## 4. Service details
- `services.<id>.env`, `volumes:` (`<source>:<destinationPath>`, source a volume name or absolute host path),
  `options:` (`docker create` options, except `--network`), and on GitHub.com also `command:` / `entrypoint:`
  (override the image CMD / ENTRYPOINT).
- Private service images: `credentials:` per service (docs example uses `github.actor` and a token).
- Images that advertise an address (Kafka-style brokers) must advertise one that matches the rule in §2.
- For ad-hoc debugging of a failed service: `docker logs "${{ job.services.postgres.id }}"`
  (`job.services.<id>.id` is the container ID).
- The runner creates the network and manages the services' life cycle; they are removed after the job.

## 5. When not to use services
- Need multi-container orchestration, init order or config files → `docker compose up -d --wait` in a step
  (`--wait` waits for services to be running|healthy and implies detached mode, per the compose CLI reference) and
  `docker compose down -v` in an `if: always()` step.
- Tests that manage their own containers (for example Testcontainers) need access to a Docker daemon: fine in host
  steps on `ubuntu-latest`, but inside a job container you must mount the Docker socket (not tested here).
- Service containers and container jobs need a Linux runner (the GitHub docs say so); use a Linux job.

## 6. Speed
Pin image tags to avoid surprise majors (`postgres:16-alpine` and `redis:7` exist on Docker Hub); pre-pull in a
self-hosted runner image. For throwaway test databases, `options: --tmpfs /var/lib/postgresql/data` (a `docker
create` flag) moves the data to RAM; measure before and after, since no speed-up figure was verified here.

## Verify
- [ ] Every service has `--health-cmd`; no sleep-based waits in steps.
- [ ] Connection strings use `localhost` for host steps / service name for container jobs.
- [ ] Job container image can write the workspace and has the shell your `run:` steps expect (`sh` by default).
- [ ] Re-running the job 5× shows no startup-race failures.
