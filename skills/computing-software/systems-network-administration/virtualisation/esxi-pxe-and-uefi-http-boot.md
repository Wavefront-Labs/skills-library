---
id: computing-software.systems-network-administration.virtualisation.esxi-pxe-and-uefi-http-boot
name: esxi-pxe-and-uefi-http-boot
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-pxe, uefi-http-boot, esxi-installation, esxi-kickstart, ipxe, vmware, esxi, vsphere]
level: advanced
status: docs-checked
description: "Network-boot the ESXi installer with PXE/TFTP or UEFI HTTP boot: DHCP options, boot.cfg prefix edits, kickstart URL, and the usual failure points."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0/esx-installation-and-setup/installing-esxi/network-booting-the-esxi-installer/boot-the-esxi-installer-by-using-pxe-and-tftp.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0/esx-installation-and-setup/installing-esxi/installing-esxi-by-using-a-script/installation-and-upgrade-scripts-used-for-esxi-installation/about-the-boot-cfg-file.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Network booting the ESXi installer (PXE and UEFI HTTP)

**Goal:** boot many hosts into the installer (usually with a kickstart) without media.

## Choose the method
| Method | Firmware | Loader | Transport |
|---|---|---|---|
| Legacy PXE | BIOS | `pxelinux.0` + `mboot.c32` | TFTP |
| UEFI PXE | UEFI | `mboot.efi` | TFTP (slow for the large installer image) |
| UEFI HTTP | UEFI with HTTP boot support | `mboot.efi` | HTTP, faster and routable |
| iPXE | either | chain to `mboot.efi` | HTTP |

## Server layout (UEFI)
```sh
mkdir -p /srv/tftp/esxi80u3 && mount -o loop VMware-VMvisor-Installer-8.0U3.iso /mnt
cp -r /mnt/* /srv/tftp/esxi80u3/
cp /srv/tftp/esxi80u3/efi/boot/bootx64.efi /srv/tftp/mboot.efi
```
Edit `/srv/tftp/esxi80u3/boot.cfg`:
- remove the leading `/` from every module path (`kernel=b.b00`, `modules=jumpstrt.gz --- ...`),
- add `prefix=esxi80u3` (or `prefix=http://10.0.0.5/esxi80u3` for HTTP),
- append `kernelopt=ks=http://10.0.0.5/ks/host01.cfg` for a scripted install.
Per-MAC boot.cfg: place it at `/srv/tftp/01-aa-bb-cc-dd-ee-ff/boot.cfg` (mboot.efi checks the MAC directory first).

## DHCP (ISC dhcpd)
```
class "pxeclients" {
  match if substring (option vendor-class-identifier, 0, 9) = "PXEClient";
  next-server 10.0.0.5;
  if option arch = 00:07 { filename = "mboot.efi"; } else { filename = "pxelinux.0"; }
}
class "httpclients" {
  match if substring (option vendor-class-identifier, 0, 10) = "HTTPClient";
  option vendor-class-identifier "HTTPClient";
  filename "http://10.0.0.5/esxi80u3/efi/boot/bootx64.efi";
}
```

## Failure points
- Hangs at "Loading /b.b00": prefix wrong or leading slashes left in boot.cfg.
- TFTP timeouts on UEFI: block size; prefer HTTP boot or iPXE.
- Secure Boot with iPXE: unsigned iPXE fails; use mboot.efi directly over HTTP.
- Kickstart not found: the installer needs a DHCP address on its boot NIC.

## Verify
Watch the TFTP/HTTP access log for `boot.cfg` then `b.b00` and the module list; the
installer reads the kickstart (check the install logs).

## Checked
2026-10-31: Confirmed pxelinux.0, mboot.efi, mboot.c32, the PXELINUX per-MAC configuration
and /tftpboot/pxelinux.cfg against the "Boot the ESXi Installer by Using PXE and TFTP"
page; boot.cfg structure, `prefix=`, `kernel=`/`modules=` and `kernelopt` (including the
kickstart script location) against the "About the boot.cfg File" page. Replaced the dead
KB 2041325 source, removed the 400 MB image size, the UEFI 2.5/vSphere 7 version claim,
the ksdevice option and the weasel.log path.
Method: documentation only; no commands were run.
