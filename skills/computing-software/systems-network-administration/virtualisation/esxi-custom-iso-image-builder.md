---
id: computing-software.systems-network-administration.virtualisation.esxi-custom-iso-image-builder
name: esxi-custom-iso-image-builder
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-image-builder, custom-esxi-iso, esxi-installation, image-profile, vib, offline-bundle, powercli, vmware, vsphere]
level: practitioner
status: draft
description: "Build a custom ESXi installer ISO or offline bundle with vendor drivers using PowerCLI Image Builder: clone a profile, add or remove VIBs, export, and verify."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esxi-installation-and-setup-8-0.html
  - https://developer.broadcom.com/powercli
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom ESXi ISO with Image Builder

**When:** the stock ISO lacks a NIC/storage driver (installer says "No network adapters"),
or you must match a vendor (Dell/HPE/Lenovo) add-on and firmware baseline on new hardware.
Prefer the vendor's custom ISO first; build your own only when you need a newer async
driver or to strip unused VIBs.

## Steps (PowerCLI, VMware.ImageBuilder module; Windows PowerShell 5.1 or PS 7 + Python for 8.x)
```powershell
Add-EsxSoftwareDepot .\VMware-ESXi-8.0U3-depot.zip          # base offline bundle
Add-EsxSoftwareDepot .\Dell-Addon-depot.zip, .\nic-driver.zip
Get-EsxImageProfile | Sort Name | Select Name, CreationTime  # pick *-standard (with Tools)
New-EsxImageProfile -CloneProfile "ESXi-8.0U3-24022510-standard" `
    -Name "ESXi-8.0U3-corp" -Vendor "corp" -AcceptanceLevel PartnerSupported
Add-EsxSoftwarePackage    -ImageProfile "ESXi-8.0U3-corp" -SoftwarePackage "i40en"   # newer driver wins by version
Remove-EsxSoftwarePackage -ImageProfile "ESXi-8.0U3-corp" -SoftwarePackage "unused-vib"
Export-EsxImageProfile -ImageProfile "ESXi-8.0U3-corp" -ExportToIso    -FilePath .\ESXi-corp.iso
Export-EsxImageProfile -ImageProfile "ESXi-8.0U3-corp" -ExportToBundle -FilePath .\ESXi-corp-depot.zip
```
Keep the bundle: it is what you feed to vLCM, Auto Deploy or `esxcli software profile update`.

## Acceptance levels
VMwareCertified > VMwareAccepted > PartnerSupported > CommunitySupported. The profile's
level must be at or below the lowest VIB's level. CommunitySupported VIBs are unsupported
and fail Secure Boot hosts.

## Gotchas
- Depots must be the **offline bundle zip**, not an ISO.
- Driver VIB names differ from module names (`i40en` vs `intel-nic`); check with
  `Get-EsxSoftwarePackage -Name *i40*`.
- ESXi 8 deprecates some legacy (vmklinux-era) drivers entirely; a driver built for 6.7
  will not install.
- On vLCM image-managed clusters, use a vendor add-on + component instead of a custom ISO,
  or remediation will flag drift.

## Verify
Boot the ISO in a lab VM or one host, then `esxcli software vib list | grep <driver>`,
`esxcli network nic list` shows all ports, and `esxcli software profile get` reports your
profile name.
