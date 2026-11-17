---
id: computing-software.devops-ci-cd.gitlab-ci.gitlab-runners-and-executors
name: gitlab-runners-and-executors
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, gitlab-runner, runner, executor, docker-executor, kubernetes-executor, shell-executor, docker-autoscaler, instance-executor, fleeting, docker-machine, config-toml, concurrent, limit, request-concurrency, runner-tags, run-untagged, protected-runner, runner-authentication-token, glrt, distributed-cache, s3-cache, privileged, docker-in-docker, dind, helm-chart, autoscaling]
level: advanced
status: docs-checked
description: "Pick, register and tune GitLab Runner executors (docker, kubernetes, docker-autoscaler, shell): config.toml concurrency, token registration, distributed cache, privileged risk."
sources: ["https://docs.gitlab.com/runner/", "https://docs.gitlab.com/runner/executors/", "https://docs.gitlab.com/runner/configuration/advanced-configuration/", "https://docs.gitlab.com/runner/executors/kubernetes/", "https://docs.gitlab.com/ci/runners/new_creation_workflow/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitLab runners and executors

**Goal:** a runner fleet that picks up jobs in seconds, scales with load, shares cache
across hosts, and can't be used by an untrusted branch to reach production secrets.

## 1. Choose the executor
| Executor | Use for | Watch out |
|---|---|---|
| `docker` | container per job on a Docker host (Podman also supported) | needs Docker on the runner host |
| `kubernetes` | an existing cluster; a new Pod per job | pod resource requests |
| `docker-autoscaler` / `instance` (fleeting plugins) | autoscaled instances on cloud providers; Docker Autoscaler wraps the Docker executor | the Instance executor does not support `image` or `services` |
| `shell`, `ssh`, `virtualbox`, `parallels`, `custom` | niche; in maintenance mode (critical security updates only) | shell: runner file system access is not protected |

Docker Machine (`docker+machine`) is deprecated; GitLab recommends moving to a fleeting-based
executor (Docker Autoscaler or Instance) for the full range of runner features.

## 2. Register (authentication-token flow)
1. Create the runner in the UI; tags, run-untagged and similar settings are set there. You get
   a token with the `glrt-` prefix.
2. On the host: `gitlab-runner register --token <RUNNER_AUTH_TOKEN>` plus the connection
   options (`--url`, `--executor`, ...).
3. Those settings are now owned by the UI object, not by CLI flags.
The legacy registration-token flow (`--registration-token`) is not recommended; from GitLab
17.0 instance admins and group owners can disable it, and registration then fails with
`410 Gone - runner registration disallowed`. Migrate any automation that uses it.

## 3. config.toml concurrency knobs
```toml
concurrent = 20            # global: max jobs across all registered runners
check_interval = 3         # seconds between job checks (default 3)

[[runners]]
  name = "docker-linux"
  url = "https://<gitlab-host>"
  token = "<RUNNER_AUTH_TOKEN>"
  executor = "docker"
  limit = 10               # per-[[runners]] cap (0 = unlimited, the default)
  request_concurrency = 4  # concurrent job requests to GitLab (default 1)
  [runners.docker]
    image = "alpine:3.20"
    privileged = false
    pull_policy = ["if-not-present", "always"]
    volumes = ["/cache"]
  [runners.cache]
    Type = "s3"
    Shared = true
    [runners.cache.s3]
      ServerAddress = "s3.amazonaws.com"
      BucketName = "<cache-bucket>"
      BucketLocation = "<region>"
```
- `concurrent` is the maximum for all `[[runners]]` sections combined; `0` is forbidden.
  Effective parallelism is bounded by `concurrent`, each section's `limit`, and host resources.
- `[runners.cache]` with `Type` (`s3`, `gcs` or `azure`) gives a distributed cache, and
  `Shared = true` (default false) lets runners share cache entries.
- `privileged` defaults to false; the docs call privileged mode insecure.
- `pull_policy` values are `never`, `if-not-present` and `always` (default); a list tries them in order.
- The runner checks `config.toml` for changes every 3 seconds and reloads (or on SIGHUP);
  no restart needed for most settings.

## 4. Kubernetes executor essentials
```toml
[runners.kubernetes]
  namespace = "gitlab-runners"
  cpu_request = "500m"
  memory_request = "1Gi"
  memory_limit = "4Gi"
  helper_cpu_request = "100m"
  poll_timeout = 600
  service_account = "ci-job"
```
- `poll_timeout` is how many seconds the runner waits when connecting to the container it
  just created; raise it when more builds queue than the cluster can run at once (default 180).
- `cpu_request_overwrite_max_allowed` is the maximum a job may raise the CPU request to via
  `KUBERNETES_CPU_REQUEST`; when empty, the overwrite feature is disabled.
- `service_account` is the default service account job pods use for the Kubernetes API; give
  job pods minimal RBAC.

## 5. Routing and isolation
- A job's `tags:` select runners; keep deploy-capable runners (network or cloud access to
  production) separate and restricted, with protected variables.
- Disable instance runners on projects that must not use them.

## 6. Docker-in-Docker
DinD needs `privileged = true` on the runner, which the docs flag as insecure. Prefer
rootless build tools without privilege; if you must use DinD, confine it to dedicated runners.
See the Docker build page for the Docker-in-Docker service setup (`services: [docker:dind]`)
and its TLS configuration.

## 7. Operations
- Keep the runner major.minor version in sync with GitLab. Older runners may still work with
  newer GitLab, but features may be missing.
- Set `log_level` (`debug`, `info`, `warn`, `error`, `fatal`, `panic`) in `config.toml`; the
  `--debug` and `--log-level` flags take priority.
- `listen_address = ":9252"` style (`<host>:<port>`) enables the embedded Prometheus metrics
  server.

## Verify
- [ ] `concurrent`/`limit` sized deliberately; no jobs pending while runners idle.
- [ ] Distributed cache configured for any multi-host or autoscaled fleet.
- [ ] Deploy-capable runners are restricted; shared runners not privileged.
- [ ] No automation uses the legacy registration token.
- [ ] Kubernetes jobs have requests/limits and a least-privilege service account.

## Checked

2026-10-28. Confirmed against the GitLab Runner pages (overview and versions, executors, advanced configuration, Kubernetes executor) and the runner creation workflow page: executor list, maintenance-mode executors, Docker Machine deprecated, Instance executor lacks `image` and `services`, `glrt-` tokens, `gitlab-runner register --token`, 410 Gone behaviour, `concurrent`, `check_interval`, `limit`, `request_concurrency`, `privileged`, `pull_policy`, cache `Type`/`Shared`/S3 keys, 3-second reload, Kubernetes `poll_timeout` (default 180), `cpu_request_overwrite_max_allowed`, `service_account`, log levels, `listen_address`, version-sync advice. Removed: `DOCKER_TLS_CERTDIR` (the identifier does not appear in the fetched Docker build page, so the sentence now points at that page instead of naming the variable), the default `concurrent = 1` claim, `shm_size`, the Helm chart name, the protected-runner paragraph, the hardware example list, metric names, and the exact poll_timeout value of 600 (an example only; the documented default is 180).

Method: documentation only; no commands were run.
