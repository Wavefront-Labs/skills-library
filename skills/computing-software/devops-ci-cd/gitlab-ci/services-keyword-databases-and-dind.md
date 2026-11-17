---
id: computing-software.devops-ci-cd.gitlab-ci.services-keyword-databases-and-dind
name: services-keyword-databases-and-dind
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, gitlab-services, services-keyword, service-alias, service-variables, service-command, service-entrypoint, ci-debug-services, postgres-service, mysql-service, redis-service, docker-dind-service, feature-flag-network-per-build, kubernetes-executor-services, integration-tests]
level: practitioner
status: docs-checked
description: "Attach Postgres, Redis or docker:dind to GitLab CI jobs with services: alias rules, per-service variables and command, readiness behaviour, CI_DEBUG_SERVICES."
sources: ["https://docs.gitlab.com/ci/services/", "https://docs.gitlab.com/ci/services/postgres/", "https://docs.gitlab.com/ci/docker/using_docker_build/", "https://docs.gitlab.com/ci/yaml/#services"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# services: databases, brokers and docker:dind

**Goal:** sidecar containers the job can reach by a predictable hostname, started healthy,
with logs you can see when they aren't.

## 1. Basic shape and hostname rule
```yaml
test:
  image: python:3.12
  services:
    - name: postgres:16
      alias: db
      variables:                  # passed only to this service container
        POSTGRES_DB: app_test
        POSTGRES_USER: app
        POSTGRES_PASSWORD: app
    - name: redis:7
      alias: cache
      command: ["redis-server", "--appendonly", "no"]   # like Dockerfile CMD; entrypoint: is like ENTRYPOINT
  variables:
    FF_NETWORK_PER_BUILD: "true"  # container-to-container networking
    DATABASE_URL: postgres://app:app@db:5432/app_test
  script: pytest
```
- `services:variables` go only to that service, not the job container; they do not support
  expansion and cannot reference themselves. Job or pipeline variables are passed to services
  automatically.
- Default alias from the image name: everything after `:` is stripped, `/` becomes `__`
  (primary alias) and `-` (secondary alias). So `registry.example.com/team/pg:16` is reachable
  as `registry.example.com__team__pg` and `registry.example.com-team-pg`. Underscore hostnames
  are not RFC valid and can break third-party apps, so set `alias:` and use it.
- Two services from the same image need distinct aliases, or one becomes unreachable.
- GitLab says to set `FF_NETWORK_PER_BUILD` to true for inter-service networking; without it
  services may not work properly.
- A service image adds no software to the job container: a `php` or `node` service does not give
  the job a `php` command. Use an image with the tools, or build one.
- Kubernetes executor (GitLab and Runner 17.9+): service containers are named after the first
  alias not already used and valid as a Kubernetes label name; otherwise `svc-i`. An alias that is
  not valid lowercase RFC 1123 DNS (for example `alpine_edge`) fails the job.

## 2. Waiting for readiness
The runner checks which ports the image exposes and starts a helper container that waits for
them. If that fails it prints `*** WARNING: Service XYZ probably didn't start properly`; the job
may still pass. Services start before `before_script`, so the script can query them, and they
stop at job end even if the job fails. An open port is not proof the database accepts queries, so
poll in `before_script`:
```bash
for i in $(seq 1 30); do pg_isready -h db -U app && break; sleep 1; done
```
Services share the `/builds` directory with the job. The job checks out into
`/builds/$CI_PROJECT_PATH` after services are running, so a service that touches project files
immediately can fail with `No such file or directory`; wait for the checkout.

## 3. docker:dind
Use `docker:dind` as a service when the job needs `docker run` or `docker build`. It needs a
runner with privileged mode (the Docker-in-Docker section of the GitLab Docker build page says
so). Docker socket binding is the alternative, but with it you cannot use a `dind` service and
the host daemon is exposed. Take the exact `DOCKER_HOST`, TLS and volume settings for your
GitLab version from the Docker-in-Docker section of the Docker build page rather than from
memory; they changed across versions. A job running `docker run` side by side with other
services also needs `FF_NETWORK_PER_BUILD`.

## 4. Debugging services
- `CI_DEBUG_SERVICES: "true"` streams every service container's logs into the job log, each
  line prefixed with the container's aliases. Accepted values: `TRUE`/`true`/`True` to enable,
  `FALSE`/`false`/`False` to disable; anything else errors and disables it. It can expose masked
  variables (service output is interleaved into the masked log), so enable it only while
  debugging.
- Private-registry service images: see "Access an image from a private container registry" in
  the services page.
- `services:pull_policy` accepts `always`, `if-not-present` and `never`, or an array; if the
  runner's allowed policies exclude it the job fails with `the configured PullPolicies ... are not
  allowed by AllowedPullPolicies`.
- Privileged mode applies to service containers too, so use only trusted service images.

## 5. Defaults
Use `default: services:` to apply to every job.

## Verify
- [ ] `getent hosts db` resolves inside the job; the app connects on first try.
- [ ] `CI_DEBUG_SERVICES` shows the database finishing init before tests begin.
- [ ] Rerunning the job 5 times has no startup races.

## Checked
2026-10-31. Confirmed against the GitLab Services page, the CI/CD YAML reference (services:entrypoint,
command, variables, pull_policy) and the Docker build page: alias rules, per-service variables,
FF_NETWORK_PER_BUILD, readiness check and warning, /builds sharing, CI_DEBUG_SERVICES values and
masking warning, Kubernetes alias naming (17.9), pull_policy values, socket binding versus dind.
Removed as unconfirmed: dind TLS variables and certificate volumes, runner config.toml volumes,
Kubernetes localhost and port-collision claims, HEALTHCHECK_TCP_PORT and 30 s timeout, DOCKER_AUTH_CONFIG for
services, default-services override rule, Testcontainers and compose advice.
Method: documentation only; no commands were run.
