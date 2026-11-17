---
id: computing-software.devops-ci-cd.tilt.tilt-tiltfile-authoring
name: tilt-tiltfile-authoring
category: computing-software
field: devops-ci-cd
product: tilt
tags: [tiltfile-authoring, tilt]
level: intro
status: docs-checked
description: "Write a first Tiltfile iteratively: deploy with k8s_yaml, build with docker_build, and add port forwards with k8s_resource."
sources:
  - "https://docs.tilt.dev/tiltfile_authoring.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing your first Tiltfile

Goal: configure Tilt for a project you can already build and deploy to Kubernetes (assumes Tilt is installed; about 15 minutes). A Tiltfile is written in Starlark, a simplified dialect of Python.

## Iterate interactively

Run `tilt up` in the project directory. Tilt offers to create a starter Tiltfile; the tutorial declines with `n`. Hit `space` to open the browser. Each time you save the Tiltfile, Tilt re-executes it. Create a file named `Tiltfile` (note the capitalization) with `print('Hello Tiltfile')` and save; the output shows in the UI, along with a warning that no resources are declared.

## The finished shape

```python
# Deploy: tell Tilt what YAML to deploy
k8s_yaml('app.yaml')

# Build: tell Tilt what images to build from which directories
docker_build('companyname/frontend', 'frontend')
docker_build('companyname/backend', 'backend')
# ...

# Watch: tell Tilt how to connect locally (optional)
k8s_resource('frontend', port_forwards=8080)
```

## Step 1: Deploy

`k8s_yaml` registers Kubernetes objects:

```python
# multiple YAML files; can be either a list or multiple calls
k8s_yaml(['foo.yaml', 'bar.yaml'])

# run a command to generate YAML
k8s_yaml(local('gen_k8s_yaml.py')) # a custom script
k8s_yaml(kustomize('config_dir')) # built-in support for popular tools
k8s_yaml(helm('chart_dir'))
```

Tilt displays the registered objects when it works.

## Step 2: Build

`docker_build` tells Tilt how to build an image; Tilt builds it, injects the ID into the Kubernetes objects and deploys. Use one `docker_build` call per image you are developing. Edit a source file and Tilt builds and deploys on save.

```python
# docker build -t companyname/frontend ./frontend
docker_build('companyname/frontend', 'frontend')
```

## Step 3: Watch (optional)

`k8s_resource('frontend', port_forwards='9000')` gives consistent port forwards. The first parameter must match the name of a pod-having k8s object passed to `k8s_yaml`; use the `new_name` parameter to rename it. `k8s_resource` can also forward multiple ports (see the Resources section of Tiltfile concepts).

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Writing Your First Tiltfile page in full (Example Tiltfile, Hello World, Steps 1 to 3). Confirmed the starter-Tiltfile prompt and `n`, the `space` key, re-execution on save, the Hello Tiltfile output and no-resources warning, the `k8s_yaml` variants, `docker_build` behaviour and the `k8s_resource` name and `new_name` rule. Trimmed: "forward multiple ports with a list", which this page does not show (it points to Tiltfile concepts, where the list form was confirmed). 

Method: documentation only; no commands were run.
