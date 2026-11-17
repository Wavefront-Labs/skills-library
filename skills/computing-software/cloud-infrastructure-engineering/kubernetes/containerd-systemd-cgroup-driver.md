---
id: computing-software.cloud-infrastructure-engineering.kubernetes.containerd-systemd-cgroup-driver
name: containerd-systemd-cgroup-driver
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, container-runtime, systemdcgroup, containerd-config, cgroup-driver, containerd]
level: practitioner
status: docs-checked
description: "Set SystemdCgroup in containerd's runc options to match the kubelet's systemd cgroup driver, for containerd 1.x and 2.x config formats, and verify."
sources: ["https://kubernetes.io/docs/setup/production-environment/container-runtimes/#containerd-systemd", "https://github.com/containerd/containerd/blob/main/docs/cri/config.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# containerd SystemdCgroup

The kubelet's own default driver is `cgroupfs`; the Kubernetes docs recommend `systemd` on systemd
hosts (and for cgroup v2), for both kubelet and runtime. The two must match.

## containerd 1.6/1.7 (config version 2)
```bash
containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
```
Resulting section:
```toml
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
  SystemdCgroup = true
```

## containerd 2.x (config version 3)
```toml
version = 3
[plugins.'io.containerd.cri.v1.runtime'.containerd.runtimes.runc.options]
  SystemdCgroup = true
```
Set it explicitly. Alpha feature gate `KubeletCgroupDriverFromCRI` (from Kubernetes 1.28) lets the
kubelet read the driver from the runtime; containerd 1.x does not support the needed RPC, and the
Kubernetes docs say the fallback to the kubelet's own setting is dropped in 1.38. containerd reads
`SystemdCgroup` from the default runtime class and falls back to detecting whether systemd runs.

## Apply
```bash
sudo systemctl restart containerd
sudo systemctl restart kubelet
```

## Verify
```bash
sudo containerd config dump | grep -n SystemdCgroup
sudo crictl info                  # runtime options under config.containerd.runtimes
grep cgroupDriver /var/lib/kubelet/config.yaml
```

## Gotchas
- Packaged containerd may ship with `cri` in `disabled_plugins`; Kubernetes needs CRI enabled.
  Regenerate the default config with `containerd config default` if needed.
- Changing the cgroup driver of a node that has already joined is sensitive: pods created under
  one driver can fail to re-create their sandbox under another. Replace the node if you can.
- Configure every runtime class with the same driver.

## Checked

2026-10-26, against containerd docs on main (latest commit 2026-10-21; RELEASES.md lists config versions up to 4 and containerd 2.3) and the Kubernetes website container-runtimes page. Confirmed: kubelet default `cgroupfs`, systemd recommendation, config snippets for containerd 1.x (version 2) and 2.x (version 3), `KubeletCgroupDriverFromCRI` behaviour and the 1.38 fallback note, `disabled_plugins` note, node cgroup driver change caution. Removed the unconfirmed claim that kubeadm defaults to systemd since 1.22 (not found in the current docs), the exact error string, jq and systemd-cgls checks.

Method: documentation only; no commands were run.
