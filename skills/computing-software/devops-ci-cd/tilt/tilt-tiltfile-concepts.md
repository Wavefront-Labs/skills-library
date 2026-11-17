---
id: computing-software.devops-ci-cd.tilt.tilt-tiltfile-concepts
name: tilt-tiltfile-concepts
category: computing-software
field: devops-ci-cd
product: tilt
tags: [tiltfile-concepts, tilt, tiltfile, k8s-resource]
level: practitioner
status: docs-checked
description: "Tiltfile execution model, k8s_yaml and local usage, Blob type, docker_build mapping, resource assembly, k8s_resource options and object selectors."
sources:
  - "https://docs.tilt.dev/tiltfile_concepts.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tiltfile concepts

## Execution model

A Tiltfile is Starlark (a Python dialect), executed on startup. Functions like `k8s_yaml` and `docker_build` register information; at the end Tilt uses the resulting configuration. Tilt records file accesses and re-executes the Tiltfile when those files change. Relative paths are relative to the Tiltfile.

## Deploy

```python
k8s_yaml('app.yaml')
k8s_yaml(['foo.yaml', 'bar.yaml'])
k8s_yaml(kustomize('config_dir'))
k8s_yaml(helm('chart_dir'))
```

For custom generators use `local`, which returns stdout as a `Blob`. Tilt cannot see files a command reads, so call `read_file('config/base.yaml')` for each dependency or the Tiltfile will not re-run when it changes. Plain strings are file paths; wrap YAML text with `blob(yaml_str)` so it is treated as data.

## Build

```python
# docker build -t companyname/frontend -f frontend/Dockerfile.dev frontend
docker_build("companyname/frontend", "frontend", dockerfile="frontend/Dockerfile.dev")
# --build-arg target=local
docker_build("companyname/frontend", "frontend", build_args={"target": "local"})
```

## Resources

A resource is a bundle of work (image build plus YAML apply, or a local command). For Kubernetes, Tilt scans loaded YAML for workloads (objects that create pods); each becomes a resource, with matching image builds and Services attached. Configure on top with `k8s_resource`:

```python
k8s_resource(workload='redis:deployment', new_name='redis')
k8s_resource(workload='frontend', port_forwards=['9000:8000', '9001:8001'])
k8s_resource(workload='frontend', port_forwards=[port_forward(9000, 8000, "app")])
k8s_resource(workload='frontend', objects=['frontend:secret', 'frontend:volume'])
k8s_resource(objects=['my-ns:namespace', 'kafka:crd'], new_name='cluster-setup')
```

A new resource built from `objects` requires `new_name`.

## Object selectors

Format `$NAME[:$KIND[:$NAMESPACE]]`, e.g. `redis:deployment:default`. A selector must identify exactly one object; add kind or namespace if the name is ambiguous. The `workload` arg is an identifier, not a selector.

## Labels

Add `labels` to `k8s_resource`, `local_resource` or `dc_resource` to group resources in the UI.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Tiltfile Concepts page in full (Execution Model, Deploy, Custom Commands, Blob type, Build, Workloads, Resources, Configuring Kubernetes Resources, object selectors, Resource Groups). Confirmed the execution model, `local` and `read_file`, the Blob rule, the docker_build mapping, workload assembly (only Services are attached), the `k8s_resource` examples, `new_name` being required for an objects-only resource and the selector format. Nothing removed. 

Method: documentation only; no commands were run.
