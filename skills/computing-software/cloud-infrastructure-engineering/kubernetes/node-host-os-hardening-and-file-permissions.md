---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-host-os-hardening-and-file-permissions
name: node-host-os-hardening-and-file-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, node-hardening, attack-surface, kubelet-file-permissions, cis-benchmark, sysctl, apparmor, selinux, file-permissions]
level: practitioner
status: docs-checked
description: "Harden node hosts: minimal OS, SSH and package reduction, sysctls, AppArmor/SELinux, and CIS ownership/permissions for kubelet and PKI files."
sources: ["https://kubernetes.io/docs/concepts/security/security-checklist/", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.9/node.yaml", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.9/master.yaml", "https://kubernetes.io/docs/tutorials/security/apparmor/", "https://kubernetes.io/docs/reference/networking/ports-and-protocols/", "https://kubernetes.io/docs/setup/production-environment/container-runtimes/", "https://kubernetes.io/docs/tasks/debug/debug-cluster/kubectl-node-debug/", "https://raw.githubusercontent.com/kubernetes/kubernetes/master/staging/src/k8s.io/component-helpers/node/util/sysctl/sysctl.go"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Node host OS hardening and file permissions

## Reduce the host
- Prefer a minimal, container-focused OS image that you replace rather than patch in place; keep nothing
  on the node that is not needed to run the kubelet and runtime, and run no other workloads on
  Kubernetes nodes.
- On a general-purpose distribution, list enabled services and remove what is unused
  (compilers, extra daemons).
- **SSH**: disable it or restrict it to a bastion or a cloud session service; no root login, keys
  only, an allow-list of groups. Use `kubectl debug node/<node> -it --image=<image>` for most debugging
  instead of SSH.
- Roll kernel security updates by replacing nodes, not by in-place upgrades on long-lived nodes.
- Keep **AppArmor or SELinux** enabled on nodes that support it; the Kubernetes security checklist lists
  it as a node control, and the AppArmor tutorial shows how profiles are applied to pods.
- Kernel settings. `net.ipv4.ip_forward=1` is a documented prerequisite for container runtimes in the
  Kubernetes setup docs. With `protectKernelDefaults: true` the kubelet errors if these differ, so set
  them first (values from the kubelet source):
```
vm.overcommit_memory=1
vm.panic_on_oom=0
kernel.panic=10
kernel.panic_on_oops=1
kernel.keys.root_maxkeys=1000000
kernel.keys.root_maxbytes=25000000
net.ipv4.ip_forward=1
```
- Firewall the node using the Kubernetes ports-and-protocols list: the kubelet API (10250) only from the
  control plane and monitoring, NodePort services (default range 30000-32767) only from load balancers,
  and keep the unauthenticated kubelet read-only port off (`readOnlyPort: 0`).

## Kubelet and PKI file permissions (CIS 4.1.x and 1.1.x, kube-bench `cis-1.9`)
```bash
stat -c '%a %U:%G %n' /etc/systemd/system/kubelet.service.d/10-kubeadm.conf \
  /etc/kubernetes/kubelet.conf /var/lib/kubelet/config.yaml /etc/kubernetes/pki/ca.crt \
  /etc/kubernetes/manifests/*.yaml /etc/kubernetes/pki/*.key /etc/kubernetes/admin.conf
```
| File | Mode (or stricter) | Owner |
|---|---|---|
| kubelet service file, kubelet `--kubeconfig` file (`kubelet.conf`), kubelet `config.yaml` (4.1.1-4.1.2, 4.1.5-4.1.6, 4.1.9-4.1.10) | 600 | root:root |
| client CA file (4.1.7-4.1.8, Manual) | 600 | root:root |
| control-plane static pod manifests (1.1.1-1.1.8) | 600 | root:root |
| Kubernetes PKI directory and files (1.1.19) | owner root:root; certificates 600 or stricter (1.1.20), keys 600 (1.1.21) | root:root |
| etcd data directory (1.1.11-1.1.12) | 700 | etcd:etcd |
| `admin.conf`, and `super-admin.conf` if present (Kubernetes 1.29+) (1.1.13-1.1.14), `scheduler.conf` (1.1.15-1.1.16), `controller-manager.conf` (1.1.17-1.1.18) | 600 | root:root |
```bash
chmod 600 /var/lib/kubelet/config.yaml /etc/kubernetes/kubelet.conf
chown root:root /var/lib/kubelet/config.yaml /etc/kubernetes/kubelet.conf
```
Bake these into the node image or configuration management so replaced nodes stay compliant.

## Verify
- [ ] `kube-bench run --targets node` shows 4.1.x PASS on a fresh node.
- [ ] No inbound SSH from the internet; AppArmor or SELinux enabled on every node.

## Checked
2026-10-28. Confirmed: modes, owners and check ids against kube-bench `cfg/cis-1.9` `master.yaml` and
`node.yaml` (including `super-admin.conf` for 1.29+ and `etcd:etcd`); the six kernel tunables and their
values against the Kubernetes source (`container_manager_linux.go`, component-helpers `sysctl.go`) and the
`protectKernelDefaults` behaviour against the KubeletConfiguration reference; `net.ipv4.ip_forward`
against the container-runtimes setup page; port 10250 and the NodePort range against the kube-apiserver and
kubelet references; AppArmor or SELinux as a node control against the security checklist; `kubectl debug
node/` against the kubectl node-debug page. Removed: distribution names (Bottlerocket, Flatcar, Talos,
COS, AL2023), the `aa-status`/`getenforce` commands, `PermitRootLogin`/`AllowGroups` directives and the
package-manager commands (not on the pages read), the earlier "600/644 per benchmark version" for the CA
file (4.1.7 says 600 or more restrictive) and port 10255.
Method: documentation only; no commands were run.
