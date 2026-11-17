---
id: computing-software.devops-ci-cd.tilt.tilt-personal-registry
name: tilt-personal-registry
category: computing-software
field: devops-ci-cd
product: tilt
tags: [personal-registry, tilt, default-registry, docker-build]
level: practitioner
status: docs-checked
description: "Set up a dev image registry for Tilt: usual defaults, ttl.sh via default_registry, per-developer registries, host_from_cluster and ECR single_name."
sources:
  - "https://docs.tilt.dev/personal_registry.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dev image registries in Tilt

Goal: give the cluster somewhere to pull your dev images from.

## Usually nothing to do

Choose a cluster. Docker for Desktop has no registry (builds go into the container runtime); local clusters like Kind get a registry from the setup scripts; remote clusters (AKS, EKS, GKE, DigitalOcean) have a colocated one.

Tilt never talks to a registry itself: it tells the image builder to push, so log in with the builder (`docker login`, `docker login quay.io`, or a credential helper for Amazon ECR, Google Artifact Registry or Google Container Registry).

`docker_build('my-image', '.')` takes an image selector matching the image name in your YAML. For a local cluster the host does not matter; Tilt injects the registry name. For a remote cluster use the registry name in both, such as `gcr.io/my-project/my-image-name`.

## No registry: ttl.sh

```
default_registry('ttl.sh/[my-user-name]-[random-string]')
```

Tilt first tries loading directly into the cluster; otherwise it renames the image under ttl.sh, pushes and pulls. ttl.sh is HTTPS but unauthenticated and deletes images after an hour.

## Registry per developer

Content-based tags mean a shared registry is normally fine. For a personal one, read an ignored settings file:

```python
settings = read_json('tilt_option.json', default={})
default_registry(settings.get('default_registry', 'gcr.io/shared-project-registry'))
```

with `{"default_registry": "gcr.io/my-personal-project"}` in `tilt_option.json`, which goes in `.gitignore`.

## Special cases

Different laptop and cluster URLs:

```python
default_registry('localhost:5000', host_from_cluster='registry:5000')
```

ECR needs a repository per image name; push everything to one with `single_name`:

```python
default_registry(
  'aws_account_id.dkr.ecr.region.amazonaws.com',
  single_name='my-team-name/dev')
```

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Setting up any Image Registry page in full. Confirmed the default registry situation per cluster type, the login commands and credential helpers, the `docker_build` image selector rule, `default_registry` with ttl.sh (HTTPS, unauthenticated, deleted after an hour), the `tilt_option.json` pattern, `host_from_cluster` and ECR `single_name`. Nothing removed. 

Method: documentation only; no commands were run.
