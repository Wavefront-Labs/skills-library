---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kind-and-minikube-local-and-ci-clusters
name: kind-and-minikube-local-and-ci-clusters
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kind, kind-config, kind-load, minikube, minikube-addons, minikube-driver, ci, local-development]
level: practitioner
status: docs-checked
description: "Run throwaway clusters for CI and laptops: kind configs (multi-node, versions, ports, mirrors), kind load, and minikube drivers, profiles and addons."
sources: ["https://kind.sigs.k8s.io/docs/user/configuration/", "https://kind.sigs.k8s.io/docs/user/quick-start/", "https://kind.sigs.k8s.io/docs/user/loadbalancer/", "https://minikube.sigs.k8s.io/docs/drivers/", "https://minikube.sigs.k8s.io/docs/commands/start/", "https://minikube.sigs.k8s.io/docs/handbook/pushing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kind and minikube for local and CI clusters

## kind (Kubernetes in Docker) — best for CI
```yaml
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: ci
nodes:
- role: control-plane
  image: kindest/node:<tag>@sha256:<digest-from-release-notes>   # tags and digests are listed in each kind release's notes
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration: {kubeletExtraArgs: {node-labels: "my-label=true"}}
  extraPortMappings:
  - {containerPort: 80, hostPort: 8080}
- role: worker
- role: worker
networking:
  disableDefaultCNI: false           # true to install another CNI such as Calico (power-user feature, limited support)
  podSubnet: 10.244.0.0/16
containerdConfigPatches:
- |-
  [plugins."io.containerd.grpc.v1.cri".registry]
    config_path = "/etc/containerd/certs.d"     # with extraMounts for a local registry mirror
```
```bash
kind create cluster --config kind-config.yaml --wait 120s
docker build -t myapp:ci .
kind load docker-image myapp:ci --name ci      # side-load; use imagePullPolicy IfNotPresent / Never
kind export logs ./kind-logs --name ci          # on failure, upload as CI artifact
kind delete cluster --name ci
```
Notes: kind v0.24.0 and later enforce NetworkPolicy out of the box (via kube-network-policies); older
releases need another CNI installed with `disableDefaultCNI: true`. LoadBalancer Services work with Cloud
Provider KIND (`sigs.k8s.io/cloud-provider-kind`). Find node image tags for your kind version in its release
notes. With `kind load`, avoid the `:latest` tag and set `imagePullPolicy: IfNotPresent` or `Never`.

## minikube — best for laptops
```bash
minikube start --driver=docker --kubernetes-version=<version> --cpus=4 --memory=8g -p dev
# Linux drivers: docker and kvm2 (preferred), virtualbox, qemu, none (bare metal), podman (experimental), ssh
# macOS: docker, vfkit (preferred), virtualbox, parallels, vmware, qemu, podman, krunkit; Windows: hyperv, docker (preferred), virtualbox, vmware, qemu, podman
minikube addons list -p dev
minikube addons enable ingress -p dev; minikube addons enable metrics-server -p dev
minikube image load myapp:dev -p dev            # or: eval $(minikube docker-env) and build inside (needs --container-runtime=docker)
minikube service web --url -p dev; minikube tunnel -p dev    # LoadBalancer IPs
minikube profile list; minikube delete -p dev
```
Multiple profiles (`-p`) = multiple clusters. The default container runtime is containerd; `--container-runtime`
accepts docker, cri-o or containerd.

## Choosing
kind: multi-node clusters in containers, reproducible in CI. minikube: addons, VM and container drivers,
and `--gpus` (Docker driver with the Docker container runtime) for GPU access.

## Verify
- [ ] CI job creates cluster, loads image, runs tests, exports logs on failure, deletes cluster.

## Checked

Checked on 2026-10-26 against `kubernetes-sigs/kind` docs (configuration, quick-start, known-issues, loadbalancer, local-registry; latest release v0.33.0) and `kubernetes/minikube` docs (drivers, commands start/addons/image/service/tunnel/profile, handbook/pushing; latest release v1.39.0).
Confirmed: `kind.x-k8s.io/v1alpha4` config keys `extraPortMappings`, `kubeadmConfigPatches`, `networking.disableDefaultCNI` and `podSubnet`, the containerd `config_path = "/etc/containerd/certs.d"` patch from the local-registry guide, `kind load docker-image`, `kind export logs`, `--wait` with units, node image tags in release notes, built-in NetworkPolicy since v0.24.0, Cloud Provider KIND; minikube driver lists per OS, `--cpus`, `--memory`, `--kubernetes-version`, `--container-runtime` options and containerd default, `--gpus`, `addons enable`, `image load`, `service --url`, `tunnel`, `profile list`.
Wrong in the draft: the minikube driver list (podman is experimental, hyperkit is not listed) and the claim that older kindnet-only clusters lack NetworkPolicy without a version cutoff.
Removed as unconfirmed: the `v1.31.4` pins, the `ingress-ready` label, the 5 minute CI target and the k3d comparison.

Method: documentation only; no commands were run.
