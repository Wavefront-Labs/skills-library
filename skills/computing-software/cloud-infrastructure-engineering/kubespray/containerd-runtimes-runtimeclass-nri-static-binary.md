---
id: computing-software.cloud-infrastructure-engineering.kubespray.containerd-runtimes-runtimeclass-nri-static-binary
name: containerd-runtimes-runtimeclass-nri-static-binary
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [containerd, runtimeclass, runc, rlimit, nri, static-binary]
level: sme
status: docs-checked
description: "Set containerd runtime classes via containerd_runc_runtime and containerd_additional_runtimes, raise nofile with base specs, enable NRI, use a static binary on old glibc."
sources:
  - https://kubespray.io/docs/CRI/containerd.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
containerd supports several runtime configurations for the Kubernetes RuntimeClass feature. Kubespray's default runtime is `runc`, configured by the `containerd_runc_runtime` dictionary:

```yaml
containerd_runc_runtime:
  name: runc
  type: "io.containerd.runc.v2"
  options:
    Root: ""
    SystemdCgroup: "false"
    BinaryName: /usr/local/bin/my-runc
  base_runtime_spec: cri-base.json
```

Add runtimes with `containerd_additional_runtimes` (a list of such dictionaries) and change the default with `containerd_default_runtime`.

**Base specs.** `base_runtime_spec` names a runtime spec JSON file. For runc it is `cri-base.json`, generated with `ctr oci spec` and updated with a custom maximum number of file descriptors per container. Change that limit via `containerd_base_runtime_spec_rlimit_nofile`. For more control, provide your own files in `containerd_base_runtime_specs` (written to `/etc/containerd` by default) and reference the file name in the runtime's `base_runtime_spec`.

**NRI.** Node Resource Interface is disabled by default; with containerd v1.7.0 or above enable it with `nri_enabled: true`.

**Static binary.** On hosts with glibc older than 2.34 (Debian 11, RHEL/Rocky/Alma/Oracle Linux 8), the default dynamically linked containerd 2.1+ binaries fail with `version GLIBC_2.34 not found`. Set `containerd_static_binary: true`; it defaults to `false`.

## Checked

All variables, the runc dictionary, NRI and the glibc caveat were confirmed against the containerd page.

Method: docs-checked 2026-11-09 against the Kubespray docs/CRI/containerd.md page (full file read).
