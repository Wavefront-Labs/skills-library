---
id: computing-software.systems-network-administration.virtualisation.ovf-ova-deploy-and-export
name: ovf-ova-deploy-and-export
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ovf, ova, ovftool, ovf-properties, vapp-options, virtual-appliance, vsphere-vm-administration, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Deploy and export OVF/OVA appliances with the vSphere client and ovftool: OVF properties, network mapping, thin disks, manifest/cert checks and fixing hardware-version errors."
sources:
  - https://developer.broadcom.com/tools/open-virtualization-format-ovf-tool/latest
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-virtual-machine-administration-guide-8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying and exporting OVF/OVA templates

**Goal:** move appliances and VMs between environments in a portable format, scriptably.

## Formats
- **OVF**: a descriptor (`.ovf`), disks (`.vmdk`, stream-optimised), optional manifest
  (`.mf`, SHA hashes) and certificate (`.cert`).
- **OVA**: the same files in one tar archive.
- **OVF properties** (vApp options) carry appliance settings (IP, hostname, passwords) that
  the guest reads at first boot.

## Deploy with ovftool
```sh
ovftool [options] appliance.ova 'vi://<user>@<vcenter>/<DC>/host/<Cluster>/'
```
See the OVF Tool documentation for the option set (probing the source, EULA acceptance,
network mapping, disk mode, OVF properties, power-on). Quote passwords in the vi://
locator via URL-encoding or let ovftool prompt.

## Export
```sh
ovftool 'vi://<user>@<vcenter>/<DC>/vm/<folder>/app01' ./export/app01.ova
```
VM must be powered off; detach ISOs first. Export from the client: VM → Template →
Export OVF Template.

## Common errors
- "Unsupported hardware family" errors: the OVF targets a newer hardware version than
  the host supports; deploy on a newer host, or edit the `.ovf` for lab use only.
- Manifest/cert validation failure: file changed after signing or a corrupt download;
  re-download, compare vendor checksums.
- Networks not mapped: deployment uses the first port group, often the wrong one.
- Chunked uploads over slow links time out in the web client; ovftool is more reliable.

## Gotchas
- OVF properties containing secrets are visible to vCenter users with read access to
  vApp options; change them after deployment.
- Exported VMs from vSphere may carry VMware-specific extensions that other hypervisors
  ignore; for cross-platform moves see the V2V skills.

## Verify
Probe the exported file with ovftool to list the expected disks and networks; a test
deploy powers on and the appliance picks up its OVF properties.

## Checked
2026-10-31: OVF Tool existence and its compatibility statement (released with VCF 9.1.1, backward compatible) confirmed on the Broadcom OVF Tool product page. Removed the specific ovftool flag examples (the option reference is not readable as HTML), the `VirtualSystemType` edit instructions and other unverified error strings; the OVF/OVA format description was kept as conceptual DMTF-standard structure only.
Method: documentation only; no commands were run.
