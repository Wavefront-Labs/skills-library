---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-systemd-unit-and-extra-args
name: kubelet-systemd-unit-and-extra-args
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet-config, kubelet-extra-args, 10-kubeadm-conf, kubelet, systemd]
level: practitioner
status: docs-checked
description: "Understand how the kubelet systemd unit, 10-kubeadm.conf, kubeadm-flags.env and KUBELET_EXTRA_ARGS combine, and change kubelet flags safely."
sources: ["https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/kubelet-integration/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubelet systemd unit and extra args

## Files (kubeadm, packages from pkgs.k8s.io)
| File | Role |
|---|---|
| `/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf` | drop-in shipped with the package (kubeadm never touches it): sets `--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf`, `--kubeconfig=/etc/kubernetes/kubelet.conf`, `--config=/var/lib/kubelet/config.yaml`, sources env files |
| `/var/lib/kubelet/kubeadm-flags.env` | `KUBELET_KUBEADM_ARGS`, written by kubeadm init/join (flags plus dynamic parameters such as the cgroup driver) |
| `/etc/default/kubelet` (deb) or `/etc/sysconfig/kubelet` (rpm) | `KUBELET_EXTRA_ARGS`, yours |
| `/var/lib/kubelet/config.yaml` | KubeletConfiguration (preferred place for most settings) |

The drop-in's `ExecStart` is:
`/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS`
so `KUBELET_EXTRA_ARGS` comes last and has the highest priority. To override unit settings, add your own
drop-in such as `/etc/systemd/system/kubelet.service.d/local-overrides.conf`.

## Change a setting
Prefer the config file for anything that has a field (`registerWithTaints`, `containerRuntimeEndpoint` and
most others do). Flags such as `--node-ip`, `--hostname-override` and `--node-labels` are documented as
plain kubelet flags.
```bash
echo 'KUBELET_EXTRA_ARGS="--node-ip=10.0.1.21"' | sudo tee /etc/default/kubelet
sudo systemctl daemon-reload && sudo systemctl restart kubelet
```
`/etc/default/kubelet` is meant for overrides "as a last resort"; kubeadm prefers
`nodeRegistration.kubeletExtraArgs` in the `InitConfiguration`/`JoinConfiguration` so new nodes get them.
kubeadm itself runs `systemctl daemon-reload && systemctl restart kubelet` after writing its files.

## Inspect what is running
```bash
systemctl cat kubelet                    # unit + drop-ins merged
journalctl -xeu kubelet
```

## Gotchas
- Many kubelet flags are marked DEPRECATED in the reference (for example `--container-runtime-endpoint`, whose
  config field is `containerRuntimeEndpoint`); migrate them to `config.yaml` and check the
  kubelet reference for each flag's status before upgrading.
- Restart the kubelet after any change; run `systemctl daemon-reload` after editing unit files.

## Checked

2026-10-26: kubernetes.io kubeadm kubelet-integration page and kubelet command-line reference (v1.37 docs, kubernetes/website main 2026-10-25) plus the kubelet config API source. Confirmed: drop-in path and contents, environment files, ExecStart ordering, DEB/RPM override files, kubeadm daemon-reload and restart, flag deprecations and config fields. Removed the unconfirmed base-unit row, upgrade behaviour claim and the ps pipeline.

Method: documentation only; no commands were run.
