---
id: computing-software.cloud-infrastructure-engineering.kubernetes.talos-linux-immutable-kubernetes-nodes
name: talos-linux-immutable-kubernetes-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, talos, talosctl, immutable-os, bare-metal, cluster-bootstrap, edge-lightweight-distros]
level: advanced
status: docs-checked
description: "Build and run clusters on Talos Linux: generate machine configs, bootstrap etcd once, patch config, upgrade OS and Kubernetes with talosctl, and debug nodes with no SSH."
sources: ["https://docs.siderolabs.com/talos/v1.13/getting-started/getting-started", "https://docs.siderolabs.com/talos/v1.13/configure-your-talos-cluster/lifecycle-management/upgrading-talos", "https://docs.siderolabs.com/kubernetes-guides/advanced-guides/upgrading-kubernetes", "https://factory.talos.dev/", "https://docs.siderolabs.com/talos/v1.13/networking/advanced/vip"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Talos Linux immutable nodes

Talos is a minimal, immutable OS that only runs Kubernetes. There is no SSH or shell: every
change goes through the Talos API with `talosctl` and a declarative machine configuration.

## Create a cluster
```bash
talosctl gen config prod https://10.0.0.10:6443 --config-patch @patches/common.yaml --config-patch-control-plane @patches/cp.yaml --config-patch-worker @patches/worker.yaml
# -> controlplane.yaml, worker.yaml, talosconfig  (contain secrets: store encrypted, e.g. SOPS)
talosctl apply-config --insecure -n 10.0.0.11 --file controlplane.yaml   # node booted from ISO, maintenance mode
talosctl apply-config --insecure -n 10.0.0.21 --file worker.yaml
export TALOSCONFIG=$PWD/talosconfig
talosctl config endpoint 10.0.0.11 10.0.0.12 10.0.0.13
talosctl bootstrap -n 10.0.0.11          # ONCE, on a SINGLE control-plane node
talosctl kubeconfig -n 10.0.0.11
talosctl health -n 10.0.0.11
```
The getting-started guide stresses running `bootstrap` once on a single control-plane node. The
maintenance API is unauthenticated by design: anyone with network access can apply a machine config,
so do not expose it publicly. Use `talosctl get disks --insecure -n <ip>` to pick the install disk
(`--install-disk` on `gen config`).

A shared control-plane virtual IP without a load balancer (Talos v1.13 documentation) is a
`Layer2VIPConfig` document applied to the control-plane nodes only, which must share a layer 2
network:
```yaml
apiVersion: v1alpha1
kind: Layer2VIPConfig
name: 10.0.0.10
link: eth0
```
The VIP relies on etcd elections, so it does not come alive until Kubernetes is bootstrapped, and
the docs say not to use it as a `talosconfig` endpoint.

## Change configuration
```bash
talosctl patch machineconfig -n 10.0.0.21 --patch @patches/kubelet-extra.yaml
talosctl get machineconfig -n 10.0.0.21 -o yaml
```
`patch` and `edit` default to automatic mode: they reboot only if the change cannot be applied
without one. `--mode=no-reboot` fails if a reboot is needed, `--mode=staged` applies on next reboot,
`--mode=try` reverts after a minute. Keep patches in Git and regenerate; avoid hand-edited node
configs (`talosctl edit machineconfig`) drifting. From Talos v1.13 the machine configuration is
multi-document and strategic-merge patches are preferred over RFC 6902 patches.

## Upgrades
```bash
# OS: pass the installer image; A/B image scheme, a failed boot rolls back
talosctl upgrade --nodes 10.0.0.21 --image factory.talos.dev/installer/<schematic-id>:<talos-version>
talosctl rollback -n 10.0.0.21            # manual rollback to the previous image
# Kubernetes components across the cluster
talosctl -n 10.0.0.11 upgrade-k8s --to <kubernetes-version> --dry-run
talosctl -n 10.0.0.11 upgrade-k8s --to <kubernetes-version>
```
- An OS upgrade does not upgrade Kubernetes; use `upgrade-k8s` separately.
- Migration is tested between adjacent minor releases: upgrade to the latest patch of each
  intermediate minor.
- Talos v1.13's upgrade command can run on several nodes in parallel, but the docs warn that
  other cluster components may not cope with more than one node rebooting at once; go one node
  at a time.
- Reboots use `kexec`. System extensions are baked into the installer image built by the Image
  Factory (schematic ID); the installer image decides the extension set, so use the same
  schematic on upgrade or the extensions change.

## Debugging without SSH
```bash
talosctl -n 10.0.0.21 service
talosctl -n 10.0.0.21 logs kubelet
talosctl -n 10.0.0.21 dmesg -f
talosctl -n 10.0.0.11 etcd members
talosctl -n 10.0.0.11 etcd snapshot db.snapshot     # backups
talosctl -n 10.0.0.21 read /proc/meminfo
```

## Gotchas
- `talosctl reset` wipes the node; it is graceful by default (cordon/drain and leave etcd), and
  a single-node cluster needs `--graceful=false` because etcd cannot be left. Resetting cloud VMs
  can leave them unable to boot because the whole disk is wiped.
- Check time sync and the install disk first when an install fails.

## Verify
- [ ] `talosctl health` passes; an etcd snapshot is taken and stored off-cluster; nodes report the
      expected Talos and Kubernetes versions (`kubectl get nodes -o wide`).

## Checked

Checked 2026-10-27 against Talos documentation v1.13 (siderolabs/docs repository, docs.siderolabs.com) and Kubernetes documentation (release v1.37.1): getting-started guide (gen config, apply-config --insecure, bootstrap once on one control-plane node, kubeconfig, health, unauthenticated maintenance API), patching page (--config-patch flags), editing page (apply modes), VIP page (Layer2VIPConfig, etcd dependency, not as talosconfig endpoint), upgrading-talos page (installer image, A/B rollback, rollback command, adjacent minor releases, parallel upgrade warning, kexec), upgrading-kubernetes page (upgrade-k8s --to --dry-run), Image Factory page (installer image path and extensions), resetting page (graceful reset) and the CLI reference (command names). Replaced the older machine.network.interfaces vip form, the pinned versions and removed the unconfirmed split-brain claim, the drain claim and the netshoot debug tip.

Method: documentation only; no commands were run.
