---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-image-preload-and-import
name: node-image-preload-and-import
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, container-runtime, image-preload, ctr-import, air-gapped, kubelet]
level: practitioner
status: docs-checked
description: "Pre-pull or import container images onto nodes (crictl pull, ctr import, DaemonSet pre-pullers, baked node images) and keep them from being garbage-collected."
sources: ["https://github.com/containerd/containerd/blob/main/cmd/ctr/commands/images/import.go", "https://github.com/containerd/containerd/blob/main/docs/namespaces.md", "https://github.com/containerd/containerd/blob/main/internal/cri/constants/constants.go", "https://github.com/containerd/containerd/blob/main/docs/cri/config.md", "https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md", "https://kubernetes.io/docs/concepts/containers/images/", "https://kubernetes.io/docs/concepts/architecture/garbage-collection/#containers-images", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-loading images on nodes

Reasons: air-gapped nodes, large images that slow scale-up, registry rate limits.

## Import a tarball
```bash
docker save registry.example.com/app:1.2.3 -o app.tar
sudo ctr -n k8s.io images import app.tar      # k8s.io is the containerd namespace the CRI plugin uses
sudo crictl images | grep app
```
`ctr images import` reads OCI and Docker archive formats. By default it imports the default
platform; use `--platform linux/amd64` for a specific platform or `--all-platforms` for all.

## Pull through CRI on each node
```bash
sudo crictl pull registry.example.com/app:1.2.3       # uses the runtime's registry config and creds
```

## DaemonSet pre-puller
```yaml
spec:
  template:
    spec:
      initContainers:
      - name: pull-app
        image: registry.example.com/app:1.2.3
        command: ["sh", "-c", "true"]       # needs a shell in the image; else use the image's own no-op
      containers:
      - name: pause
        image: registry.k8s.io/pause:<tag>
```
Runs on every node (and new ones), forcing a pull through the normal path.

## Bake into node images
Node image builds that pull the heavy images (GPU drivers, ML runtimes) give the fastest
scale-up, at the cost of a node image rebuild per version.

## Keep them
Kubelet image GC deletes unused images, oldest-used first, when disk usage passes
`imageGCHighThresholdPercent` (default 85) until it reaches `imageGCLowThresholdPercent`.
- containerd pins the sandbox (pause) image (`pinned_images.sandbox` in the CRI config); other
  images are not pinned by default.
- `imageMaximumGCAge` (default `0s`, disabled) also removes images unused for that long, and
  its timer resets when the kubelet restarts. Set it carefully, and size disks so GC rarely
  triggers.
- Use `imagePullPolicy: IfNotPresent` with immutable tags or digests; `Always` asks the
  registry every time and only works well while the registry is reachable.

## Verify
```bash
kubectl get node <n> -o json | jq -r '.status.images[].names[]' | grep app
```

## Checked
Checked 2026-10-27 against containerd sources and docs (main branch: `ctr images import`
formats, `--platform` and `--all-platforms`; namespaces doc for `ctr -n`; CRI constant
`K8sContainerdNamespace = "k8s.io"`; CRI config `pinned_images.sandbox`), the cri-tools crictl guide (`crictl pull`) and
kubernetes/website (main tree, v1.38 development; latest release v1.37): garbage collection
(high and low thresholds, oldest-first deletion, `imageMaximumGCAge` reset on restart), kubelet
configuration (`imageGCHighThresholdPercent` default 85, `imageMaximumGCAge` default `0s`) and
Images (`IfNotPresent`, `Always`). Replaced the pinned pause tag with a placeholder and removed
the unconfirmed manifest-list import failure and skopeo invocation.

Method: documentation only; no commands were run.
