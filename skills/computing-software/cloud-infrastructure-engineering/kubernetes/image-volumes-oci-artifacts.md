---
id: computing-software.cloud-infrastructure-engineering.kubernetes.image-volumes-oci-artifacts
name: image-volumes-oci-artifacts
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ephemeral-volumes, image-volume, oci-artifacts, imagevolume, ml-models]
level: practitioner
status: docs-checked
description: "Mount an OCI image or artifact read-only into a pod with an image volume, for models, data or tools, including runtime requirements and pull policy."
sources: ["https://kubernetes.io/docs/concepts/storage/volumes/#image", "https://kubernetes.io/docs/tasks/configure-pod-container/image-volumes/", "https://github.com/kubernetes/website/blob/main/content/en/docs/reference/command-line-tools-reference/feature-gates/ImageVolume.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image volumes

An `image` volume mounts the content of an OCI image or artifact directly, without running it.
Useful for ML model weights, static datasets, or tooling binaries shipped separately from the app
image. Feature gate `ImageVolume`: alpha in 1.31 (off), beta in 1.33 (off by default), beta on by
default in 1.35, stable in 1.36. The container runtime must support it; check your runtime's release notes.

```yaml
apiVersion: v1
kind: Pod
metadata: {name: llm}
spec:
  containers:
  - name: server
    image: acme/inference:2.3
    volumeMounts:
    - {name: weights, mountPath: /models, readOnly: true}
    # subPath into an image volume is supported from 1.33
  volumes:
  - name: weights
    image:
      reference: registry.internal/models/llama-8b:v1
      pullPolicy: IfNotPresent
```

## Behaviour
- Mounted read-only in a single directory (the container's `mountPath`).
- Pull secrets are assembled like for container images: node credentials, service account image
  pull secrets and the Pod spec's image pull secrets.
- `pullPolicy` is `Always`, `IfNotPresent` or `Never`; the default is `Always` for a `:latest`
  tag, otherwise `IfNotPresent`. With `Always` or `Never` a failed resolution sets the Pod to
  `Failed`; a failure to resolve or pull at startup blocks the containers, is retried with
  normal volume backoff and is reported in the Pod reason and message.
- The volume is re-resolved if the Pod is deleted and recreated.
- `subPath`/`subPathExpr` mounts are supported from 1.33; `fsGroupChangePolicy` has no effect.
- Which object types can be mounted is up to the runtime; at minimum, valid container image types.

## Packaging
Build a `FROM scratch` image with `COPY weights/ /` and push it. Non-image OCI artifacts depend on runtime support.

## Verify
`kubectl exec llm -- ls /models` shows the files; writing to `/models` fails because the mount is read-only.

## Checked

2026-10-25, against the Kubernetes website pages for the `image` volume source and the image-volume task, and the `ImageVolume` feature-gate stages file (main). Confirmed: gate stages (alpha 1.31, beta 1.33 off, beta on by default 1.35, stable 1.36), read-only mount, `reference` and `pullPolicy` fields and defaults, pull-secret assembly, failure behaviour, `subPath` from 1.33, `fsGroupChangePolicy` having no effect. Removed as unconfirmed: runtime minimum versions (containerd, CRI-O), `noexec`, image garbage collection, the `oras push` packaging command.

Method: documentation only; no commands were run.
