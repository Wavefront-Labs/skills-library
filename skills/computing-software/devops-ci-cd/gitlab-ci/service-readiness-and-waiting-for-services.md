---
id: computing-software.devops-ci-cd.gitlab-ci.service-readiness-and-waiting-for-services
name: service-readiness-and-waiting-for-services
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, service-health-check, wait-for-service, services, readiness, healthcheck]
level: practitioner
status: docs-checked
description: "Make GitLab CI jobs wait for service containers (databases, brokers) to be ready: port checks, the start-failed warning, and explicit wait loops."
sources: ["https://docs.gitlab.com/ci/services/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service readiness in GitLab CI

**Goal:** tests never start before the database or broker accepts connections.

## What the runner does
The runner finds the ports the service image exposes and starts a helper container that waits for them to accept connections, before `before_script` runs. If the port check fails you see `*** WARNING: Service ... probably didn't start properly`; this usually affects the job, but the job can still succeed (for example if the service starts shortly afterwards or the job does not use it). Services start before `before_script` runs and stop at the end of the job.

## Make readiness explicit
Do not rely on the port check alone. Poll in `before_script`:
```yaml
test:
  services:
    - name: postgres:16
      alias: db
  variables:
    POSTGRES_PASSWORD: ci-only-secret
  before_script:
    - for i in $(seq 1 30); do pg_isready -h db -U postgres && break; sleep 2; done
    - pg_isready -h db -U postgres || { echo "db not ready"; exit 1; }
```
- Use the service's native probe (`pg_isready`, `mysqladmin ping`, `redis-cli -h redis ping`, `curl -f http://es:9200/_cluster/health`).
- The hostname is the service alias; the job container reaches it over the network, not `localhost` (in the Docker executor).
- A service with no exposed port is the documented cause of the warning; use the explicit loop for those.

## Failure modes
- Warning then connection refused: slow startup; extend the loop or pin a lighter image.
- Wrong alias or missing `command:`/`entrypoint:` for services that need arguments.
- Service needs memory: raise runner limits or use a smaller dataset.

## Verify
The job log shows the probe succeeding before the test step; rerun 10 times for flakiness.

## Checked

2026-11-02. Confirmed: runner checks the image's exposed ports and starts a helper container that waits for them; the warning text and its two causes; services start before `before_script`; services reachable by hostname/alias rather than localhost (GitLab Services docs). Removed: HEALTHCHECK_TCP_PORT variable (not found). Not checked: client probe commands (pg_isready etc.) are generic examples.

Method: documentation only; no commands were run.
