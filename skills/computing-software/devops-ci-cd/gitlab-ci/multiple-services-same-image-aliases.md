---
id: computing-software.devops-ci-cd.gitlab-ci.multiple-services-same-image-aliases
name: multiple-services-same-image-aliases
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, multiple-service-aliases, gitlab-services, service-alias]
level: practitioner
status: docs-checked
description: "Run two containers from the same service image (e.g. two Postgres or Redis instances) using alias and per-service variables, plus networking caveats."
sources: ["https://docs.gitlab.com/ci/services/#define-services-with-aliases", "https://docs.gitlab.com/ci/services/#using-services-with-docker-run-docker-in-docker-side-by-side"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running the same service image twice with aliases

```yaml
test:
  image: python:3.12
  services:
    - name: postgres:16
      alias: db-primary
      variables: { POSTGRES_PASSWORD: pw, POSTGRES_DB: app }
    - name: postgres:16
      alias: db-analytics
      variables: { POSTGRES_PASSWORD: pw, POSTGRES_DB: analytics }
    - name: redis:7
      alias: cache,redis-alt        # multiple aliases, comma separated
  script:
    - pg_isready -h db-primary && pg_isready -h db-analytics
```

## Details
- Without `alias`, the hostname is derived from the image name (text after `:` is dropped, `/` becomes `__` for the primary alias and `-` for the secondary);
  give each copy of the same image its own alias.
- Per-service `variables:` set environment for that service.
- Docker executor: to enable inter-service networking set `FF_NETWORK_PER_BUILD` to `true`; without it services may not work properly.
- Kubernetes executor: since GitLab and Runner 17.9 a service alias can be used as the service container name (see the services docs for the naming rules).

## Verify
- [ ] Both hosts accept connections from the job script.

## Checked

2026-10-28. Confirmed on the GitLab services page: alias accepts several aliases separated by commas, default hostname rules from the image name, FF_NETWORK_PER_BUILD for inter-service networking, aliases as Kubernetes container names from 17.9. Removed: the Runner 14.5 version gate, the secret-leak claim about job variables, legacy-links claim, and the Kubernetes shared-port claims and port override.
Method: documentation only; no commands were run.
