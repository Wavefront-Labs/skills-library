---
id: computing-software.cloud-infrastructure-engineering.kubespray.gvisor-and-kata-containers-runtimes
name: gvisor-and-kata-containers-runtimes
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [gvisor, kata-containers, runtimeclass, qemu, pod-overhead, sandbox]
level: advanced
status: docs-checked
description: "Enable sandboxed runtimes on containerd: gvisor_enabled for runsc, and kata_containers_enabled with the kata-qemu RuntimeClass, pod overhead, cgroup driver and version options."
sources:
  - https://kubespray.io/docs/CRI/gvisor.md
  - https://kubespray.io/docs/CRI/kata-containers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both runtimes need a container manager that supports RuntimeClass, such as containerd.

**gVisor** is an application kernel in Go with an OCI runtime called `runsc`:

```yaml
container_manager: containerd
gvisor_enabled: true
```

**Kata Containers** runs pods in lightweight VMs. Qemu is the only supported hypervisor.

```yaml
container_manager: containerd
kata_containers_enabled: true
etcd_deployment_type: host
```

By default pods use runc. Kubespray generates the RuntimeClass `kata-qemu`; a pod opts in with `runtimeClassName: kata-qemu` in its spec.

**Pod Overhead** is recommended, and mandatory for Kata pods with resource limits. It needs a kubelet cgroup driver: `cgroupfs` works best, though with cgroups v2 `systemd` also works.

```yaml
kubelet_cgroup_driver: cgroupfs
kata_containers_qemu_overhead: true
kata_containers_qemu_overhead_fixed_cpu: 10m
kata_containers_qemu_overhead_fixed_memory: 290Mi
```

Optional: select the release with `kata_containers_version: 2.2.2` and enable debug with `kata_containers_qemu_debug: 'true'` (debug is off by default for all Kata components).

## Checked

2026-11-04. Both enablement snippets and the Kata overhead settings were confirmed on the gVisor and Kata Containers pages.

Method: documentation only; no commands were run.
