---
id: computing-software.devops-ci-cd.tilt.tilt-custom-resource
name: tilt-custom-resource
category: computing-software
field: devops-ci-cd
product: tilt
tags: [custom-resource, tilt, k8s-kind, crd]
level: practitioner
status: docs-checked
description: "Teach Tilt to recognise Kubernetes custom resources: make them independent, find images, handle pods, and install their operators."
sources:
  - "https://docs.tilt.dev/custom_resource.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom resources in Tilt

Goal: Tilt knows built-in kinds (Deployment, Job, StatefulSet). For your own CRDs it needs three answers.

## 1. Independent resource?

By default custom resources land in one "uncategorized" bucket. Give one its own status and log pane:

```python
k8s_resource(new_name='my-postgres-server',
             objects=['postgres-name'])
```

## 2. Contains images?

Tell Tilt where the image field lives:

```python
k8s_kind('UselessMachine', image_json_path='{.spec.image}')
```

## 3. Creates pods?

Wait for pods to become healthy, or declare there are none:

```python
k8s_kind('UselessMachine', image_json_path='{.spec.image}', pod_readiness='wait')
k8s_kind('UselessMachine', image_json_path='{.spec.image}', pod_readiness='ignore')
```

Tilt follows owner references to find pods. If the resource sets none, give a label selector:

```
k8s_resource(new_name='postgres',
             extra_pod_selectors=[{'kubedb.com/name': 'quick-postgres'}])
```

After that Tilt fetches logs and creates port-forwards as for built-ins.

## Installing the operator

- `local('./install-my-crd-operator.sh')` is easiest but runs on every Tiltfile reload and blocks startup.
- `local_resource(name='my-crd-operator', cmd='./install-my-crd-operator.sh', allow_parallel=True)` parallelises; add `resource_deps=['my-crd-operator']` on dependents via `k8s_resource`.
- `k8s_custom_deploy(name=..., apply_cmd=..., delete_cmd=...)` lets Tilt monitor operator health and logs; the script must print the resulting YAML to stdout.

## Pods that create pods

Either use `k8s_kind` with `image_json_path='{.spec.imageToDeploy}'` (any field works), or put an env var in the container spec (`IMAGE_TO_DEPLOY` = `my-image`) and build with:

```
docker_build('my-image', '.', match_in_env_vars=True)
```

Tilt replaces `my-image:latest` with the content-based image reference it built.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/custom_resource.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
