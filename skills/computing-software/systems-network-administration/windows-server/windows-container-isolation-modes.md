---
id: computing-software.systems-network-administration.windows-server.windows-container-isolation-modes
name: windows-container-isolation-modes
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-containers, hyper-v-isolation, process-isolation, isolation-flag, security-boundary, multi-tenant, utility-vm, kubernetes-runtimeclass]
level: practitioner
status: docs-checked
description: "Pick process vs Hyper-V isolation for Windows containers: security boundary, version flexibility, overhead, --isolation flag, defaults per OS, and Kubernetes support."
sources:
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/hyperv-container
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/system-requirements
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows container isolation modes

| | Process isolation | Hyper-V isolation |
|---|---|---|
| Kernel | shared with the host and other containers | each container runs in a highly optimized VM with its own kernel |
| Isolation | namespaces (file system, registry, network ports, process and thread IDs, Object Manager) and resource controls | hardware-level isolation between containers and the host |
| Host/container versions | must be a combination the compatibility matrix supports | works with mismatched versions that Hyper-V isolation supports |
| Requires | Containers feature | Hyper-V role; nested virtualization if the host is itself a VM |
| Default | Windows Server | Windows 10 Pro and Enterprise client |

## Choose
- Trusted workloads on a host and image combination the matrix supports for process isolation: **process**.
- When you need stronger isolation or the image and host versions do not match: **Hyper-V**.

## Use
```powershell
docker run --isolation=process -d mcr.microsoft.com/windows/servercore:ltsc2022 ping localhost -t
docker run --isolation=hyperv  -d mcr.microsoft.com/windows/servercore:ltsc2019 ping localhost -t
```
Process isolation on Windows 10 Pro or Enterprise is for development and testing only (build 17763 or later and Docker
Engine 18.09 or later); use Windows Server hosts for production. Piercing the boundary (host volumes, named pipes, ports,
shared network namespace, device visibility) is supported but weakens the container's security posture; shared memory,
shared synchronization objects and shared process namespaces are not supported.

## Verify
- [ ] A process started in the container is visible with `Get-Process` on the host for process isolation, but not for Hyper-V
  isolation, where a `vmwp` process is visible instead.
- [ ] Image and host version mismatch errors disappear with the chosen isolation.

## Checked

2026-10-26 against the Windows containers docs (isolation modes, system requirements, version compatibility; Virtualization-Documentation last commit 2026-10-20): both modes' descriptions, the --isolation flag, defaults per host type, Windows 10 requirements, Hyper-V role and nested virtualization requirements, boundary-piercing list. Removed unconfirmed claims about default utility VM memory, the daemon.json exec-opts isolation setting, the Kubernetes runtime class handler and hcsdiag or Get-ComputeProcess verification.

Method: documentation only; no commands were run.
