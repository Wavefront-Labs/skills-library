---
id: computing-software.cloud-infrastructure-engineering.kubernetes.air-gapped-cluster-bootstrap-and-upgrades
name: air-gapped-cluster-bootstrap-and-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, air-gapped, offline-cluster, private-registry, image-mirroring, kubeadm-config-images, disconnected-cluster, skopeo, harbor, binary-mirror, regulated-environments, kubeadm-imagerepository]
level: advanced
status: docs-checked
description: "Bootstrap and upgrade a kubeadm cluster with no outbound internet: mirror images and packages into private registries and repos, and know what breaks offline."
sources: ["https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/#without-internet-connection", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/#custom-images", "https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Air-gapped cluster operations

**Goal:** run the same bootstrap and upgrade procedures as
`computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-cluster-bootstrap`
and
`computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-cluster-upgrade-sequencing`
in an environment with no outbound internet. Every image, binary, and package has to
be mirrored in deliberately, and anything that pulls from the public internet by
default is a latent failure waiting for the next upgrade.

## 1. Enumerate what the cluster needs, before you need it
```bash
kubeadm config images list --kubernetes-version=v<major>.<minor>.<patch>
```
Prints the control-plane image set kubeadm needs for a version (`kube-apiserver`,
`kube-controller-manager`, `kube-scheduler`, `kube-proxy`, `pause`, `etcd`, CoreDNS). The
`--config` flag accepts a kubeadm configuration file to control `kubernetesVersion` and
`imageRepository`. This is the minimum, not the whole list. Also needed: the CNI's own
images, CSI driver images, metrics-server and any other add-ons, and the OS packages for
`kubeadm`/`kubelet`/`kubectl` and the container runtime (these come from a package repo,
not a container image, so they need their own mirror path).

## 2. Mirroring images
```bash
skopeo copy --all --preserve-digests docker://registry.k8s.io/<path>:<tag> docker://internal-registry.example.local/<path>:<tag>
```
- Point kubeadm at the mirror with `imageRepository` in `ClusterConfiguration` (or
  `kubeadm config images pull --image-repository <mirror>`); this changes every image
  reference kubeadm generates. The same `--config` file must be passed to
  `kubeadm init`.
- Paths under a custom repository can differ from `registry.k8s.io` for backwards
  compatibility. Do not guess the destination paths: pull from the default paths with
  `kubeadm config images list`, then push to the paths printed by
  `kubeadm config images list --config=config.yaml` where that file holds the custom
  `imageRepository` (and any `imageTag` for etcd or CoreDNS).
- The pause (sandbox) image is not set through kubeadm: configure it in the container
  runtime (see the runtime's documentation).
- `skopeo copy --all` copies every architecture in a manifest list, and
  `--preserve-digests` keeps the manifest digests identical, so what you tested is what
  you mirrored.
- CNI/CSI/add-on Helm charts reference images by their own values; the kubeadm
  `imageRepository` setting does **not** rewrite those, so check each chart's image
  values individually.

## 3. Mirroring binaries and packages
- `kubeadm`, `kubelet`, `kubectl`, and the container runtime ship as OS packages (deb/rpm)
  from package repos that also need internal mirrors (a local APT/YUM mirror synced from
  outside the air gap, or packages transferred in per release). See
  `computing-software.cloud-infrastructure-engineering.kubernetes.offline-os-package-mirrors-for-kubernetes-nodes`.
- CNI plugin binaries (default `/opt/cni/bin`) and the CNI manifest's image references are
  separate from the CNI's own container images.
- Helm, `crictl` and any other operational tooling used inside the air-gapped network
  need their own pre-staged copies; anything that would normally download a release from
  the internet must be staged in advance.

## 4. What breaks without connectivity
- **NTP**: with no outbound internet there is often no public NTP pool either. Clock drift
  across nodes breaks certificate validation; run an internal time source deliberately.
- **DNS**: CoreDNS forwards names outside the cluster domain to the resolver it is
  configured with (see the Corefile in the `coredns` ConfigMap). If the node's resolver
  has no path out, external lookups fail; confirm this is the deliberate posture.
- Add-ons and operators with built-in update checks or external endpoints will retry and
  log noisily; find them while testing in a gapped staging cluster.

## 5. Upgrades in an air gap
Same sequence as `kubeadm-cluster-upgrade-sequencing`, with every image and package
pre-mirrored for the target version **before** starting. Build the full mirror set for the
target version, verify it is complete (`kubeadm config images list` against the mirror,
confirmed reachable from a cluster node), then run the upgrade exactly as the connected
procedure, pointed at the mirror throughout.

## Gotchas
- A registry mirror that is reachable from the bastion used to set it up but not from the
  cluster nodes' network segment is a common air-gap bootstrap failure; verify reachability
  from a cluster node specifically.
- `imageRepository` must be in the configuration passed to `kubeadm init` before it pulls
  anything; after a failed init against the public registry, run `kubeadm reset` first.
- Exact add-on image-override mechanics vary per chart or operator; confirm each one's
  override path rather than assuming one setting covers everything.

## Verify
- [ ] `kubeadm config images list --image-repository <mirror>` resolves and every image is
      confirmed pullable from an actual cluster node, not just the bastion.
- [ ] Every add-on (CNI, CSI, metrics-server, any operators) has its image registry
      overridden explicitly.
- [ ] Internal NTP and DNS resolution work with no outbound path, verified deliberately.
- [ ] The next upgrade's full image/package set is mirrored and verified reachable before
      the upgrade procedure begins.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm source: kubeadm-init page (running without an Internet connection, custom images and path differences, pause image set in the runtime), kubeadm config images list/pull flags (--kubernetes-version, --image-repository, --config) in the kubeadm source, and skopeo-copy flags --all and --preserve-digests. Removed unconfirmed claims about revocation checks, telemetry, init hang behaviour and pinned versions.

Method: documentation only; no commands were run.
