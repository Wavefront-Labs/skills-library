---
id: computing-software.cloud-infrastructure-engineering.kubernetes.k3s-rke2-airgap-image-tarballs
name: k3s-rke2-airgap-image-tarballs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, k3s, rke2, k3s-airgap, air-gapped, image-tarball]
level: practitioner
status: docs-checked
description: "Install and upgrade k3s or rke2 with no internet using the release image tarballs, the install script skip flags and a private registry mirror."
sources: ["https://docs.k3s.io/installation/airgap", "https://docs.rke2.io/install/airgap", "https://docs.k3s.io/installation/private-registry"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k3s and rke2 air-gap installs

## Artifacts to carry in (match the exact release)
k3s: `k3s` binary, `k3s-airgap-images-amd64.tar.zst`, `install.sh`.
rke2: `rke2.linux-amd64.tar.gz`, `rke2-images.linux-amd64.tar.zst`, `sha256sum-amd64.txt`, `install.sh`.
RKE2 also publishes `sha256sum-amd64.txt`, which its install script uses to verify artifacts.

## k3s
```bash
sudo mkdir -p /var/lib/rancher/k3s/agent/images/
sudo cp k3s-airgap-images-amd64.tar.zst /var/lib/rancher/k3s/agent/images/
sudo install -m 755 k3s /usr/local/bin/k3s
INSTALL_K3S_SKIP_DOWNLOAD=true ./install.sh
```
Image archives are imported every time k3s starts (kubelet waits for this). Agents need the same
images directory populated; for an agent, run the install with `INSTALL_K3S_SKIP_DOWNLOAD=true K3S_URL=https://<server>:6443 K3S_TOKEN=<token> ./install.sh`.
To skip re-import on restart, `touch /var/lib/rancher/k3s/agent/images/.cache.json`; the docs warn
that pruned images are then not restored automatically.

## rke2
The full images tarball includes Canal; the docs offer `rke2-images-core.linux-amd64.tar.zst` plus a
CNI-specific tarball (for example `rke2-images-cilium...`) as an alternative.
```bash
sudo mkdir -p /var/lib/rancher/rke2/agent/images/
sudo cp rke2-images.linux-amd64.tar.zst /var/lib/rancher/rke2/agent/images/
INSTALL_RKE2_ARTIFACT_PATH=/root/rke2-artifacts sh install.sh   # offline mode; creates the systemd units
```

## Private registry instead of tarballs
```yaml
# /etc/rancher/k3s/registries.yaml (rke2: /etc/rancher/rke2/registries.yaml)
mirrors:
  docker.io:
    endpoint: ["https://registry.internal"]
  registry.k8s.io:
    endpoint: ["https://registry.internal"]
configs:
  registry.internal:
    tls: {ca_file: /etc/ssl/internal-ca.pem}
```
Containerd always tries the registry's default endpoint last, even when `registries.yaml` lists
other endpoints, and rewrites are not applied to it.

## Upgrades
k3s manual upgrade (docs): put the new images tar in `/var/lib/rancher/k3s/agent/images/` on each node and delete the old tar; replace the binary in `/usr/local/bin` and re-copy the install script; re-run it with the same environment variables; restart k3s if the installer did not.
Automated air-gap upgrades need the matching `rancher/k3s-upgrade` image in your private registry (the `+` in the version becomes `-` in the tag).

## Verify
`k3s crictl images` lists the images; pods in kube-system reach Running with no
`ErrImagePull` events.

## Checked

2026-10-26, against k3s-io/docs and rancher/rke2-docs on main (latest commits 2026-10-23/24; docs mention RKE2 v1.37 and containerd 2.0 era releases). Confirmed: image directories and tarball names, `INSTALL_K3S_SKIP_DOWNLOAD`, `INSTALL_RKE2_ARTIFACT_PATH` offline mode, per-start import and `.cache.json`, `registries.yaml` mirrors/configs layout and default-endpoint fallback, k3s manual upgrade steps. Removed unconfirmed `k3s crictl rmi --prune`, `system-default-registry` and `systemctl enable` line.

Method: documentation only; no commands were run.
