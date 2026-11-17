---
id: computing-software.systems-network-administration.virtualisation.vlcm-cluster-images
name: vlcm-cluster-images
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vlcm, lifecycle-manager, vlcm-image, desired-state-image, vendor-addon, components, remediation, esxi-patching, vmware, vsphere, image-compliance-check, vlcm-convert-to-image]
level: practitioner
status: draft
description: "Manage ESXi with vLCM cluster images: base image + vendor add-on + components, compliance checks, staged remediation with pre-checks, and switching from baselines."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/managing-host-and-cluster-lifecycle-8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere Lifecycle Manager cluster images

**Goal:** every host in a cluster runs exactly the same ESXi build, vendor drivers and
firmware, declared once and remediated automatically.

## Image composition
| Layer | Example |
|---|---|
| ESXi base image | 8.0 U3x build |
| Vendor add-on | Dell/HPE/Lenovo customisation (drivers, agents) |
| Firmware and drivers add-on | Via a hardware support manager (see HSM skill) |
| Components | Individual drivers or solutions (e.g. a NIC driver newer than the add-on's) |
Solutions such as vSAN witness, NSX and HA agents are added by vCenter automatically.

## Workflow
1. **Sync depots** (online Broadcom depot with download token, or import offline bundles
   to a local depot / UMDS for air-gapped vCenters).
2. Cluster → Updates → Image → **Edit**: pick the new base image and add-on, validate.
   Save; the image is the cluster's desired state.
3. **Check compliance**: per host, shows what would change and whether a reboot is
   needed.
4. **Run pre-check**: HA/DRS state, vSAN health, maintenance mode feasibility, removable
   devices attached to VMs, hardware compatibility (with the HCL check).
5. **Stage** (copies payloads to hosts ahead of the window, 8.0+), then **Remediate**:
   hosts go into maintenance mode one at a time (or in parallel when configured for
   non-vSAN clusters), patch, reboot, exit.

## Remediation settings
- VM power state handling (do not change, suspend, power off) for VMs that cannot migrate.
- Parallel remediation (up to N hosts) for clusters with spare capacity.
- **Quick Boot** to skip firmware POST on supported hardware (much faster reboots).
- Retry and timeout for maintenance mode entry.

## Switching from baselines
Cluster → Updates → "Manage with a single image": vLCM checks whether host software can
be expressed as an image (third-party VIBs not in a depot block conversion). Once a
cluster uses images it cannot go back to baselines. Baselines are deprecated in 8.x.

## Gotchas
- A component newer in the vendor add-on than in your manual component list causes
  version conflicts; read the validation messages.
- Image edits apply to all hosts; test in a small cluster first.
- Removable media (ISO mounted on a VM) blocks maintenance mode: detach first.

## Verify
Cluster → Updates shows all hosts Compliant with the image; `esxcli software profile get`
and `esxcli software component list` match the image on a sample host.
