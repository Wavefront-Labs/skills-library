---
id: computing-software.cloud-infrastructure-engineering.talos-linux.performance-tuning-kernel-args
name: performance-tuning-kernel-args
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [performance, kernel-args, cpufreq, amd-pstate, intel-idle, mitigations, iommu, image-factory]
level: advanced
status: docs-checked
description: "Tune Talos for latency and throughput via kernel arguments: performance governor, AMD and Intel sleep states, CPU mitigations, microcode extensions, IOMMU, and how to apply them."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/system-configuration/performance-tuning.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos balances performance against security and efficiency. Measure every change and check it introduces no vulnerability. Most advice targets bare metal.

**Applying kernel parameters.** A one-time change can be made at the bootloader console (not on Secure Boot systems). Permanent changes go into the boot assets and installer image through an Image Factory schematic using `customization.extraKernelArgs`; on an installed machine, boot the new asset or upgrade to the installer built from the schematic.

CPU scaling: the default governor is `schedutil`. For maximum performance:

```text
cpufreq.default_governor=performance
```

Sleep states add wake-up latency. On AMD use the `amd-pstate` driver in active mode; on Intel disable the `intel_idle` driver:

```text
amd_pstate=active
intel_idle.max_cstate=0
```

Hardware vulnerability mitigations cost performance. First install the `amd-ucode` and `intel-ucode` system extensions (and a current Talos), since early microcode loading can lessen the cost for some CPUs. Mitigations can be disabled wholesale, which is not recommended security-wise, or individually per the kernel documentation:

```text
mitigations=off
```

I/O: before Talos 1.8.2, `iommu.strict=0` improved I/O performance; later versions default to it. Bypassing the IOMMU for DMA improves it further at some cost to security:

```text
iommu.passthrough=1
```

The page also links a separate NUMA topology and VM placement guide for host NUMA discovery.

## Checked

2026-11-04. Each kernel argument, the Image Factory extraKernelArgs route and the microcode extension advice confirmed on the Performance Tuning page.

Method: documentation only; no commands were run.
