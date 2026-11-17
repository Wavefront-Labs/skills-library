---
id: computing-software.devops-ci-cd.tilt.tilt-resource-dependencies
name: tilt-resource-dependencies
category: computing-software
field: devops-ci-cd
product: tilt
tags: [resource-dependencies, tilt]
level: practitioner
status: docs-checked
description: "Control Tilt startup order with resource_deps, readiness checks, pod_readiness, and parallelism settings in update_settings and local_resource."
sources:
  - "https://docs.tilt.dev/resource_dependencies.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource dependencies

Goal: control the startup order of Tilt resources when it depends on application logic Tilt cannot guess (e.g. `frontend` needs a running `database`).

List resources with `tilt get uiresources`.

## Default startup heuristic

- Run the Tiltfile to create resources.
- Run `local_resource` definitions first, one at a time so they cannot step on each others' output.
- Run up to 3 image build and deploys at a time in parallel (Kubernetes and Docker Compose resources), guessing order from the YAML.
- Continue until all resources are built.

## resource_deps

`local_resource`, `dc_resource`, and `k8s_resource` all take `resource_deps`:

```python
k8s_resource('frontend', resource_deps=['database'])
```

Effects: `frontend` is not deployed until `database` has been ready at least once since Tilt started; and `tilt up frontend` also brings up all of frontend's transitive dependencies.

## Readiness

By default a resource is ready when:

- `k8s_resource`: the pod is running and all its containers are ready (Tilt uses the Kubernetes readiness probe when available). A job is ready when completed.
- `dc_resource`: the container is started (Tilt does not currently observe docker-compose health checks).
- `local_resource`: the command has succeeded at least once.

If an object creates no pods, tell Tilt not to use pods for readiness; it then shows ready once applied:

```python
k8s_resource('frontend', pod_readiness='ignore')
```

`local_resource` supports readiness probes borrowed from the Kubernetes API.

## Parallelism

```python
update_settings(max_parallel_updates=10)
update_settings(max_parallel_updates=1)  # serial deploys
local_resource(name, cmd, allow_parallel=True)
```

## Limits

`resource_deps` only affects the first build after `tilt up`: once any version of `database` has run, its dependents are unblocked for the rest of Tilt's lifetime. It ensures some instance exists, not a current one.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Resource Dependencies page in full. Confirmed the startup heuristic (including up to 3 parallel builds), `resource_deps` on the three resource functions and its two effects, the default readiness rules, `pod_readiness='ignore'`, `max_parallel_updates`, `allow_parallel=True` and the first-build-only limit. Nothing removed. 

Method: documentation only; no commands were run.
