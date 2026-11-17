---
id: computing-software.devops-ci-cd.kustomize.images-task-example
name: images-task-example
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [images, newname, newtag, registry]
level: intro
status: docs-checked
description: "Swap an image for a private registry copy and pin a tag with the images field, using the Kubernetes task page example."
sources:
  - https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/images/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The task page changes the image used inside containers without creating a patch.

```yaml
# deployment.yaml container: image: nginx
resources:
- deployment.yaml
images:
- name: nginx
  newName: my.image.registry/nginx
  newTag: "1.4.0"
```

`kubectl kustomize ./` then shows the container as `image: my.image.registry/nginx:1.4.0`.

Steps for a registry migration:

1. List all images in your resources.
2. Add an `images` entry per image with `name` as the old image name.
3. Set `newName` to the new location, and `newTag` or `digest`.
4. Build with `kubectl kustomize ./` and check the `image:` lines.

The images reference page describes the fields: `name` matches images with this image name, `newTag` overrides the image tag or digest (`nginx:old` becomes `nginx:new`), and `newName` overrides the image name (`nginx:old` becomes `nginx-special:old`). Its example uses a registry-qualified name (`mycontainerregistry/myimage` renamed to `differentregistry/myimage`) and a `digest: sha256:...` entry that produces `alpine@sha256:...`.

The task page also says kustomize can inject field values from other objects into containers without patches using `replacements`; when a Service name may change through `namePrefix` or `nameSuffix`, hard coding it in a command argument is not recommended.

## Checked

2026-11-08: confirmed against the Kubernetes kustomize task page (images example and output, replacements note) and the kustomize images reference page (field table, name, tag and digest examples). Removed the statement that `nginx` matches both `nginx:old` and `nginx:1.7.9` as a rule beyond the table, the advice to include the registry when names collide, and the immutability remark about digests.

Method: documentation only; no commands were run.
