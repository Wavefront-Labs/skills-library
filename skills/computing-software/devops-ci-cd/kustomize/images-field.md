---
id: computing-software.devops-ci-cd.kustomize.images-field
name: images-field
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [images, newname, newtag, digest]
level: practitioner
status: docs-checked
description: "Change image names, tags or digests across all containers with the images field instead of writing patches."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/images/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `images` field modifies name, tag and/or digest without patches. It matches on `name` and overrides what you set.

| Field | Meaning | Example |
|---|---|---|
| `name` | Match images with this name | `nginx` |
| `newTag` | Override tag or digest | `nginx:old` becomes `nginx:new` |
| `newName` | Override image name | `nginx:old` becomes `nginx-special:old` |
| `digest` | Pin to a digest | `alpine@sha256:...` |

```yaml
images:
- name: postgres
  newName: my-registry/my-postgres
  newTag: v1
- name: nginx
  newTag: "1.8.0"
- name: my-demo-app
  newName: my-app
- name: alpine
  digest: sha256:24a0c4b4a4c0eb97a1aabb8e29f18e917d05abfe1b7a7c07857230879ce7d3d3
```

Results from the page's build output: `postgres:8` becomes `my-registry/my-postgres:v1`, `nginx:1.7.9` becomes `nginx:1.8.0`, `my-demo-app:latest` becomes `my-app:latest`, and `alpine:3.7` becomes `alpine@sha256:...`.

Quote numeric-looking tags such as `"1.8.0"`. To move an image to a different registry keep `name` as the old full name (for example `mycontainerregistry/myimage`) and set `newName`. Setting only `newName` keeps the existing tag.

Tip: after changing a tag or digest, run kustomize build and search the output for image: to confirm every container was rewritten as intended.

## Checked

2026-11-03. Confirmed against: the images reference page.
Removed or reworded: the init-container claim.

Method: documentation only; no commands were run.
