---
id: computing-software.cloud-infrastructure-engineering.zot.kind-local-registry
name: kind-local-registry
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, kind-cluster, local-registry, containerd-patches, kep-1755, dev-environment]
level: practitioner
status: docs-checked
description: "Run Zot as the local registry for a kind cluster: registry container, containerd mirror patch, network connect, KEP-1755 ConfigMap, deploy and clean up."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/kind-deploy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: docker, kubernetes, kind, containerd, skopeo. If a proxy is set, add `kind-registry` to `no_proxy`.

1. Registry container from the minimal image, bound to host port 5001:
   ```
   docker run -d --restart=always -p "127.0.0.1:5001:5000" --name kind-registry ghcr.io/project-zot/zot-minimal:latest
   ```
2. Create the cluster with a containerd patch mapping `localhost:5001` to the registry:
   ```
   containerdConfigPatches:
   - |-
     [plugins."io.containerd.grpc.v1.cri".registry.mirrors."localhost:5001"]
       endpoint = ["http://kind-registry:5000"]
   ```
   passed to `kind create cluster --config=-` (with `apiVersion: kind.x-k8s.io/v1alpha4`).
3. Join the registry to the kind network: `docker network connect "kind" kind-registry` (only if not already connected).
4. Apply a `local-registry-hosting` ConfigMap in `kube-public` with `localRegistryHosting.v1` and `host: "localhost:5001"` (KEP-1755).
5. Test:
   ```
   skopeo copy --format=oci --dest-tls-verify=false docker://gcr.io/google-samples/hello-app:1.0 docker://localhost:5001/hello-app:1.0
   kubectl create deployment hello-server --image=localhost:5001/hello-app:1.0
   ```
6. Clean up: `kind delete cluster`, `docker stop kind-registry`, `docker rm kind-registry`.

## Checked

2026-11-04. Confirmed against the zot kind install guide; commands and values match the page.

Method: documentation only; no commands were run.
