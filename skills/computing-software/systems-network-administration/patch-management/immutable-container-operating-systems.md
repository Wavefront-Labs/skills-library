---
id: computing-software.systems-network-administration.patch-management.immutable-container-operating-systems
name: immutable-container-operating-systems
category: computing-software
field: systems-network-administration
product: patch-management
tags: [bottlerocket, flatcar, immutable-os, talos, container-image-patching, patch-management]
level: practitioner
status: docs-checked
description: "Patch immutable container hosts (Bottlerocket, Flatcar, Talos): A/B image updates, update operators for Kubernetes, reboot coordination and why you never patch them in place."
sources:
  - https://github.com/bottlerocket-os/bottlerocket
  - https://github.com/bottlerocket-os/bottlerocket-update-operator
  - https://www.flatcar.org/docs/latest/setup/releases/update-strategies/
  - https://github.com/flatcar/flatcar-linux-update-operator
  - https://github.com/siderolabs/talos/blob/main/website/content/v1.15/reference/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Immutable container operating systems

Bottlerocket, Flatcar Container Linux and Talos have read-only root filesystems and no package manager. You patch by moving the whole OS image forward, typically with A/B partitions and a reboot.

## Bottlerocket (AWS)
- Two partition sets; update downloads into the inactive set, reboot switches; automatic rollback if boot fails.
- Commands (control or admin container): `apiclient update check`, then `apiclient update apply --check --reboot`; `signpost rollback-to-inactive` is the documented manual rollback if the update does not work for a workload.
- In Kubernetes use **Bottlerocket Update Operator (brupop)**: Helm-installed, labels nodes `bottlerocket.aws/updater-interface-version=2.0.0`, drains and updates nodes (one at a time by default; the Helm value `max_concurrent_updates` changes this).
- EKS managed node groups: update the AMI release version instead (rolling replace).

## Flatcar
- `update-engine` installs the update from the release channel onto the passive partition and waits for a reboot.
- Reboot coordination: `locksmithd` with `REBOOT_STRATEGY` set to `reboot`, `etcd-lock` or `off` in `/etc/flatcar/update.conf`, or **Flatcar Linux Update Operator (FLUO)** in Kubernetes, which replaces locksmithd and drains the node before rebooting.
```sh
update_engine_client -status
update_engine_client -check_for_update
```

## Talos Linux
API-only; `talosctl upgrade --nodes <node-ip> --image <installer-image>:<version>` upgrades Talos on a node (it drains the Kubernetes node first by default, `--drain`), and Kubernetes is upgraded separately with `talosctl upgrade-k8s --to <version>`.

## Practice
- Treat nodes as cattle: in auto-scaling setups, replacing nodes with the new AMI/image is often simpler than in-place A/B updates.
- Scan the node image version, not packages; vulnerability reporting maps to OS release.
- Respect PDBs; one node at a time per failure domain.

## Gotchas
- Configuration lives in user-data/machine config; changes need the same rollout discipline as updates.
- Disabling updates "for stability" on immutable OSes recreates the old patch debt problem without tools to fix it.

## Verify
All nodes report the target OS version (`kubectl get nodes -o wide` OS-IMAGE column); update operator logs show no failed nodes; no pods stuck in drain.

## Checked
Date: 2026-10-27. Documentation checked: Bottlerocket README (update, `apiclient update apply --check --reboot`, automatic rollback on boot failure, `signpost rollback-to-inactive`), Bottlerocket Update Operator README (label `bottlerocket.aws/updater-interface-version=2.0.0`, Helm install, `max_concurrent_updates` default "1"), Flatcar update strategies page (locksmithd `reboot`, `etcd-lock`, `off`, `update_engine_client -status`, FLUO replaces locksmithd), Flatcar Linux Update Operator README, Talos `talosctl` CLI reference (`upgrade`, `--image`, `--drain` default true, `upgrade-k8s --to`). Removed the Nebraska, release-channel list and Talos rollback claims, which were not confirmed.

Method: documentation only; no commands were run.
