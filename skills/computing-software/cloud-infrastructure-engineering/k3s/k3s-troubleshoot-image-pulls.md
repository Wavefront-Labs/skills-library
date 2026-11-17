---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-troubleshoot-image-pulls
name: k3s-troubleshoot-image-pulls
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, containerd-log, image-pull-error, k3s-images-txt]
level: practitioner
status: docs-checked
description: "Find the real cause of image pull failures in K3s and mirror the K3s images into your own registry."
sources:
  - https://docs.k3s.io/installation/private-registry
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Troubleshooting: the kubelet error may show only the terminal error from the pull against the default endpoint, which makes it look as if configured endpoints are unused. Read the containerd log on the node where the pod was scheduled:

```
/var/lib/rancher/k3s/agent/containerd/containerd.log
```

Find the node with `kubectl get pod -o wide -n NAMESPACE POD` and read the NODE column.

Mirroring K3s images into a private registry (needs a host with Docker or other tooling that can pull and push, and access to both docker.io and your registry):

1. Get k3s-images.txt for your release from GitHub.
2. Pull each listed image from docker.io, for example `docker pull docker.io/rancher/mirrored-pause:3.6`.
3. Retag: `docker tag docker.io/rancher/mirrored-pause:3.6 registry.example.com:5000/rancher/mirrored-pause:3.6`.
4. Push: `docker push registry.example.com:5000/rancher/mirrored-pause:3.6`.

## Checked

2026-11-08. Read the full K3s Private Registry Configuration page (docs/installation/private-registry.md in the k3s-io/docs repo). Confirmed: the kubelet error reflecting only the default endpoint, the containerd log path, finding the node with kubectl get pod -o wide, and the four mirroring steps with k3s-images.txt. Removed the FAQ log locations line (not on the page).

Method: documentation only; no commands were run.
