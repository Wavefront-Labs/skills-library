---
id: computing-software.systems-network-administration.virtualisation.esxi-auto-deploy-image-profiles
name: esxi-auto-deploy-image-profiles
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [auto-deploy, image-profile, image-builder, esxi-installation, stateless-esxi, stateful-install, deploy-rule, pxe, powercli, vmware, esxi, vsphere]
level: advanced
status: draft
description: "PXE-boot ESXi fleets with vSphere Auto Deploy: image profiles from depots, deploy rules, host profiles, stateless vs stateful installs and boot failure triage."
sources:
  - https://developer.broadcom.com/powercli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi Auto Deploy and image profiles

**Goal:** hosts that boot an approved ESXi image over the network, pick up their
configuration from a host profile, and land in the right cluster without hands on keys.

## Pieces
| Component | Role |
|---|---|
| Image profile | A named set of VIBs (base image + vendor add-on + drivers), built from software depots |
| Deploy rule | Matches hosts by `vendor`, `model`, `mac`, `ipv4`, `asset` etc. and assigns image profile, host profile and folder/cluster |
| Active rule set | The ordered rules actually evaluated at boot |
| TFTP/DHCP | DHCP options 66/67 (BIOS `undionly.kpxe.vmw-hardwired`, UEFI `snponly64.efi.vmw-hardwired`) point at the TFTP bundle downloaded from vCenter |

Enable the **Auto Deploy** and **Image Builder** services in vCenter (Administration →
Services, or the Auto Deploy page in the client), then download the TFTP Boot Zip.

## Build an image profile (PowerCLI)
```powershell
Add-EsxSoftwareDepot https://<depot-url>/index.xml        # or a local offline bundle .zip
Get-EsxImageProfile | Sort-Object Name | Select Name, CreationTime
New-EsxImageProfile -CloneProfile "ESXi-8.0U3-<build>-standard" -Name "corp-8.0U3" -Vendor corp
Add-EsxSoftwarePackage -ImageProfile corp-8.0U3 -SoftwarePackage <vendor-driver-vib>
Export-EsxImageProfile -ImageProfile corp-8.0U3 -ExportToBundle -FilePath corp-8.0U3.zip
```

## Rules
```powershell
New-DeployRule -Name prod-r650 -Item corp-8.0U3, "prod-hostprofile", "Cluster-Prod" `
    -Pattern "model=PowerEdge R650", "ipv4=10.10.20.10-10.10.20.60"
Add-DeployRule prod-r650          # adds to the active working set
Test-DeployRuleSetCompliance -VMHost (Get-VMHost <host>) | Repair-DeployRuleSetCompliance
```
Rule order matters: the first match per item type wins. Changing a rule only affects
hosts after `Repair-DeployRuleSetCompliance` and a reboot.

## Stateless vs stateful
- **Stateless:** image streams to RAM every boot; config comes from the host profile.
  Auto Deploy, DHCP and vCenter become boot dependencies; a vCenter outage stops cold
  boots (use the reverse proxy/caching or keep enough hosts up).
- **Stateful install:** first boot via Auto Deploy writes ESXi to local disk; later boots
  are local. Set in the host profile (System Image Cache Configuration).

## Failure triage
- Host boots to "no rule matched": check `Get-DeployRuleSet` patterns against the host's
  attributes on the iPXE screen.
- Host boots but sits in maintenance mode: host profile needs answers (customisation);
  fill them and remediate.
- Image mismatches after an upgrade: you edited the profile but not the rule; rebuild the
  rule to point at the new profile and repair compliance.

## Verify
`Get-VMHost | Select Name, @{n='Image';e={(Get-EsxCli -VMHost $_ -V2).software.profile.get.Invoke().name}}`
lists the profile each host runs; every host should show the intended name.
