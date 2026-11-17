---
id: computing-software.devops-ci-cd.skaffold.custom-actions-exec
name: custom-actions-exec
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [exec, customactions, containers, timeout]
level: advanced
status: docs-checked
description: "Define named one-off container tasks in customActions and run them with skaffold exec."
sources:
  - "https://skaffold.dev/docs/custom-actions/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`customActions` define named, completable tasks that run containers on demand. They are not meant to run your main application. Each action and container needs a name that is unique across modules and configurations (two profiles may each define an action with the same name). `name` and `containers` are required on an action.

```yaml
customActions:
  - name: update-infra
    timeout: 10        # seconds; default is no timeout
    failFast: true     # default; false makes it fail-safe
    containers:
      - name: update-db-schema
        image: gcr.io/my-registry/db-updater:latest
      - name: setup-external-proxy
        image: gcr.io/my-registry/proxy:latest
```

Run it:

```bash
skaffold exec update-infra
```

Behaviour per the docs:

- The containers of an action run in parallel and Skaffold streams their logs. By default (`executionMode` unset) they run as local Docker containers; the other mode creates one Kubernetes Job per container (`restartPolicy: Never`, `backoffLimit: 0`), extendable with `executionMode.kubernetesCluster.overrides` or `jobManifestPath`.
- The action succeeds only if every container ends without error. Skaffold then returns exit code 0, otherwise 1.
- By default an action is fail-fast: when one container fails, Skaffold stops the others and returns 1. Set `failFast: false` to let all containers run to completion before the failure is reported.
- `timeout` is the maximum run time in seconds. If it expires, Skaffold stops running containers and returns status 1 (the output shows "context deadline exceeded").
- To use images Skaffold builds, run `skaffold build --file-output=build.json` and then `skaffold exec update-infra --build-artifacts=build.json`.

Use cases include database migrations or other one-off infrastructure steps beside build and deploy. In CI, treat a non-zero exit code as a failed step.

## Checked

2026-11-04. Read the Skaffold Custom Actions page and the `Action` definition in the v4beta14 config schema (`name` and `containers` required, `failFast` default true, `timeout` in seconds). Confirmed all behaviour listed above; added the Kubernetes Job mode and the build-then-exec flow from the same page.
Method: documentation only; no commands were run.
