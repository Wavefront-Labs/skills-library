---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-detached-steps
name: woodpecker-detached-steps
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [detach, background-steps, startup-order]
level: advanced
status: docs-checked
description: "Start long-running Woodpecker containers in the background with detach."
sources:
  - https://woodpecker-ci.org/docs/usage/services
  - https://woodpecker-ci.org/docs/administration/configuration/backends/kubernetes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker detached steps

`detach: true` on a step starts a long-running container without blocking later steps. Use it when you need explicit control over startup order, which plain `services` do not give.

```yaml
steps:
  - name: build
    image: golang
    commands:
      - go build

  - name: database
    image: redis
    detach: true

  - name: test
    image: golang
    commands:
      - go test
```

The `database` step starts after `build`, stays running, and `test` runs while it is up. Containers from detached steps terminate when the pipeline ends.

Compare the two mechanisms:

- `services` are defined in a separate `services` section of the workflow file.
- Detached steps sit in the `steps` section and start at their position in the step order.

The Kubernetes backend page shows a Docker-in-Docker step with `detach: true` and `privileged: true`; on that backend a headless service is created per workflow, so any step can be reached by step name as hostname.

Service containers need time to initialize and accept connections; the page suggests waiting a few seconds or implementing a backoff.

## Checked

2026-11-08. Read the Woodpecker Services page (woodpecker-ci.org/docs/usage/services) in full, and the Kubernetes backend page only around the headless service and the dind example. Removed the claims that services start at the workflow start, that detached steps follow `depends_on` ordering and that a detached step is the way to run dind (the page only shows it as an example).

Method: documentation only; no commands were run.
