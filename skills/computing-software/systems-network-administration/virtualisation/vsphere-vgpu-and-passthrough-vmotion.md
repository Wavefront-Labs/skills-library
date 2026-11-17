---
id: computing-software.systems-network-administration.virtualisation.vsphere-vgpu-and-passthrough-vmotion
name: vsphere-vgpu-and-passthrough-vmotion
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vgpu-vmotion, vgpu, directpath-io, vmotion, nvidia, vmware, vsphere]
level: advanced
status: draft
description: "Plan and run vMotion for NVIDIA vGPU VMs, set the vCenter hot-migrate setting, estimate stun time, and handle DirectPath passthrough VMs that cannot move."
sources:
  - https://docs.nvidia.com/vgpu/latest/grid-vgpu-user-guide/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vMotion of vGPU and passthrough VMs

**Goal:** keep GPU-accelerated VMs mobile for host maintenance, and know which ones are not.

## What can move
| VM GPU type | vMotion |
|---|---|
| NVIDIA vGPU (mediated, profile like `grid_a40-8q`) | Yes, vSphere 6.7 U1 and later, when enabled |
| DirectPath I/O / Dynamic DirectPath (whole device passthrough) | No; power off and cold migrate |
| vSGA (shared graphics) | Yes |

## Enable vGPU vMotion
vCenter -> Configure -> Advanced Settings: set `vgpu.hotmigrate.enabled` = `true`. Without it the compatibility check reports that the VM has a PCI device that cannot migrate.

## Prerequisites
- Destination host has a compatible GPU with free capacity for the same profile and the same or compatible NVIDIA host driver (VIB) branch.
- Host graphics set to *Shared Direct*; vMotion network fast (25 GbE recommended).

## Stun time
The GPU framebuffer is copied during the stun phase. The Migrate wizard shows an estimated stun time for vGPU VMs. Large profiles over 10 GbE can stun for many seconds, which drops VDI sessions. Reduce it with faster vMotion networks, multiple vMotion vmks, or smaller profiles.

## Maintenance mode
DRS may not evacuate vGPU VMs automatically. Migrate them manually, or power them off, before the host enters maintenance mode. For passthrough VMs, plan a power-off window; set HA restart priority knowing they can only restart on hosts with a free device.

## Verify
After migration, `nvidia-smi` in the guest shows the GPU and the host `nvidia-smi vgpu` on the destination lists the VM.
