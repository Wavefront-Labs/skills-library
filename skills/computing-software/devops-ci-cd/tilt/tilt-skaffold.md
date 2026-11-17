---
id: computing-software.devops-ci-cd.tilt.tilt-skaffold
name: tilt-skaffold
category: computing-software
field: devops-ci-cd
product: tilt
tags: [skaffold, tilt, migration, tiltfile]
level: intro
status: docs-checked
description: "Translate a Skaffold build and kubectl deploy configuration into an equivalent Tiltfile with k8s_yaml and docker_build."
sources:
  - "https://docs.tilt.dev/skaffold.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating from Skaffold to Tilt

Goal: translate a Skaffold configuration into a Tiltfile. Skaffold concepts map almost directly into Tilt.

## Why Tilt

- The Tilt UI shows status at a glance, so errors cannot scroll off-screen. You can navigate the UI in the terminal and read the logs of just one service; a global log is available if you want the full firehose.
- Configuration is Starlark, a subset of Python, so simple configs are shorter and complex configs are possible.

## Example translation

A Skaffold config with two images and two deployments:

```yaml
apiVersion: skaffold/v1alpha5
kind: Config
build:
  artifacts:
  - image: gcr.io/windmill-public-containers/servantes/snack
    context: snack
  - image: gcr.io/windmill-public-containers/servantes/spoonerisms
    context: spoonerisms
deploy:
  kubectl:
    manifests:
      - deployments/snack.yaml
      - deployments/spoonerisms.yaml
```

becomes this `Tiltfile`:

```python
k8s_yaml(['deployments/snack.yaml', 'deployments/spoonerisms.yaml'])
docker_build('gcr.io/windmill-public-containers/servantes/snack', 'snack')
docker_build('gcr.io/windmill-public-containers/servantes/spoonerisms', 'spoonerisms')
```

In this example the `deploy.kubectl.manifests` entries go into one `k8s_yaml` call and each `build.artifacts` entry (image, context) becomes a `docker_build` call.

After translating, continue with the Write a Tiltfile guide (tiltfile_authoring).

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the From Skaffold to Tilt page in full. Confirmed both comparison bullets and the example Skaffold config with its Tiltfile translation. Reworded: the mapping sentence, which generalised from the single example the page shows. The skill is thin (one worked example). 

Method: documentation only; no commands were run.
