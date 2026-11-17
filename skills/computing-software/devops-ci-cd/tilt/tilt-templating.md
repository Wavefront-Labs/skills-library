---
id: computing-software.devops-ci-cd.tilt.tilt-templating
name: tilt-templating
category: computing-software
field: devops-ci-cd
product: tilt
tags: [templating, tilt]
level: practitioner
status: docs-checked
description: "Adapt prod Kubernetes YAML for dev in Tilt using Tiltfile YAML patches, kustomize, helm, or k8s_custom_deploy, and inspect applied YAML with tilt get."
sources:
  - "https://docs.tilt.dev/templating.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modifying YAML for dev

Goal: tweak prod Kubernetes YAML for dev (set `DEBUG=true`, exactly one replica, a dev label) with a few lines of Tiltfile or an existing tool like helm, kustomize, or ytt.

## What Tilt does automatically

When Tilt deploys YAML it applies the label `app.kubernetes.io/managed-by: tilt` to every resource, ensures containers have `pullPolicy: IfPresent` or `pullPolicy: Never` on a local cluster, and injects a fully-resolved image tag.

Inspect what Tilt knows:

```
tilt get kubernetesapply
tilt get kubernetesapply docs-site -o yaml
```

The second prints `spec.yaml` (what you gave Tilt) and `status.resultYAML` (what came back from the cluster).

## Small patches in a Tiltfile

`read_yaml_stream` reads a file and decodes it to a list of objects; `decode_yaml_stream` decodes a YAML string; `encode_yaml_stream` encodes a list of objects to a string.

```python
objects = read_yaml_stream('deployment.yaml')
for o in objects:
  o['metadata']['namespace'] = 'my-ns'
k8s_yaml(encode_yaml_stream(objects))
```

## Connecting existing YAML tools

```python
k8s_yaml(local('./generate-yaml.sh'))
```

Tilt runs the script on startup, registers and deploys the YAML. Built-ins: `kustomize('.')` invokes `kustomize` on the directory; `helm('./path/to/chart')` invokes `helm template`. Both return YAML for `k8s_yaml`, are wrappers around `local()`, and handle arguments and dependency watching. Other tools can be packaged as Tilt Extensions.

## When YAML is not enough

Tools like Pulumi, or Helm packages with chart hooks, deploy in order, wait on health checks, or add post-deploy hooks, then output YAML at the end. The page recommends `k8s_custom_deploy` instead of `k8s_yaml` for these; the `helm_resource` extension is an example.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Modifying YAML for Dev page in full. Confirmed the automatic label, pull policy and image tag injection, the `tilt get kubernetesapply` commands and the `spec.yaml` and `status.resultYAML` fields, the three YAML stream functions, `kustomize` and `helm` as wrappers around `local()`, and `k8s_custom_deploy` for tools that deploy in order. Not opened: the linked blog posts and the helm_resource extension. Softened: "use `k8s_custom_deploy`" to the page's "we recommend". 

Method: documentation only; no commands were run.
