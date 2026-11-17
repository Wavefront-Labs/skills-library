---
id: computing-software.cloud-infrastructure-engineering.talos-linux.machine-config-apply-edit-modes
name: machine-config-apply-edit-modes
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [machine-config, apply-config, edit, patch, staged, try-mode, reboot, talosctl]
level: practitioner
status: docs-checked
description: "Changing live Talos node config: apply-config, edit and patch machineconfig, the auto, staged and try modes, and which settings still need an explicit reboot."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/system-configuration/editing-machine-configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three commands update a running node: `talosctl apply-config` (from a file), `talosctl edit machineconfig` (editor round-trip) and `talosctl patch machineconfig` (patches). In this release config is always applied to the running node without a reboot. Modes: default `--mode=auto` / `no-reboot` (immediate), `--mode=staged` (applied at next reboot; the live config is unchanged so a later `edit --mode=staged` does not show it), and `--mode=try` (applied now, auto-reverted after 1 minute unless a further update arrives). `--mode=reboot` was removed in 1.14 and `--mode=interactive` earlier; reboot yourself with `talosctl reboot` so you can cordon and drain first.

Settings that need a reboot to take effect: `.cluster.etcd` (read at service start; Talos will not restart etcd implicitly); environment variables only for services restarted afterwards; kernel modules (never unloaded, parameters applied on first load); volume encryption key rotation; `SecurityProfileConfig` workloadIsolation. `UnattendedInstallConfig` and `.machine.install` only matter at install or upgrade.

```bash
talosctl get machineconfig v1alpha1 -o jsonpath='{.spec}' > machineconfig.yaml
talosctl -n <IP> apply-config -f config.yaml
talosctl -n <IP> apply machineconfig -f config.yaml --mode=staged
talosctl -n <IP> edit machineconfig
talosctl -n <IP1>,<IP2>,... edit machineconfig
talosctl -n <IP> patch machineconfig -p kubelet-patch.yaml -p manifest-patch.yaml
talosctl -n <IP> reboot
```

The editor comes from `TALOS_EDITOR`, then `EDITOR`, then `vi`. A node in maintenance mode needs `--insecure (-i)`. An empty or unchanged edit applies nothing. A node that fails to boot on a bad config (such as a wrong control plane endpoint) can be fixed by updating the configuration.

## Checked

2026-11-04. Edit Machine Configuration page confirms the modes, the removed options, the reboot-required list and the command forms.

Method: documentation only; no commands were run.
