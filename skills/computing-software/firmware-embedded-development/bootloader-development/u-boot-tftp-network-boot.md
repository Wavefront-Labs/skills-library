---
id: computing-software.firmware-embedded-development.bootloader-development.u-boot-tftp-network-boot
name: u-boot-tftp-network-boot
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [tftp-boot, u-boot, nfs-root, dhcp-boot, pxe, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Boot a board over the network from U-Boot for fast kernel/rootfs iteration: TFTP server setup, ipaddr/serverip variables, dhcp vs static, NFS root, and PXE."
sources:
  - https://docs.u-boot.org/en/latest/usage/cmd/tftpput.html
  - https://docs.u-boot.org/en/latest/usage/environment.html
  - https://docs.kernel.org/admin-guide/nfs/nfsroot.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TFTP and network boot

During kernel and driver development, rebuilding and copying to SD cards wastes minutes per
iteration. Network boot loads kernel and DTB over TFTP and mounts the rootfs over NFS.

## Host side
Run a TFTP server and an NFS server on the host (see your distro's documentation for the
export options). Copy the kernel `Image` and board `.dtb` into the TFTP directory, and extract the
rootfs tarball (from Yocto/Buildroot) as root into the NFS-exported directory to preserve
ownership and device nodes.

## U-Boot side
```
=> setenv ipaddr 192.168.1.50; setenv serverip 192.168.1.10; setenv netmask 255.255.255.0
   (or: => dhcp   with autoload disabled: setenv autoload no)
=> ping ${serverip}
=> tftp ${kernel_addr_r} Image
=> tftp ${fdt_addr_r} imx8mp-acme.dtb
=> setenv bootargs console=ttymxc1,115200 root=/dev/nfs nfsroot=${serverip}:/srv/nfs/rootfs ip=dhcp rw
=> booti ${kernel_addr_r} - ${fdt_addr_r}
```
Save as a command: `setenv netboot 'tftp ...; tftp ...; setenv bootargs ...; booti ...'` then
`run netboot`. Don't `saveenv` dev settings onto production units.

## PXE / extlinux over the network
The extlinux-over-PXE bootmeth (`CONFIG_BOOTMETH_EXTLINUX_PXE`) looks for `extlinux/extlinux.conf`
on the TFTP server, an extlinux-style menu describing kernel, FDT and append lines. Standard boot
(bootstd) can do this automatically with network bootdevs (`bootflow scan -lb`).

## Troubleshooting
| Symptom | Cause |
|---|---|
| TFTP timeouts | firewall on host (TFTP uses UDP port 69 by default, `tftpdstp` overrides it), wrong `serverip`, link not up or wrong active interface (`ethact`); tune `tftptimeout` / `tftptimeoutcountmax` on lossy networks |
| no MAC address | set `ethaddr` (from fuses/EEPROM in board code for production) |
| kernel waits forever for NFS root | kernel lacks NFS-root or IP autoconfiguration support, or the NFS options in `nfsroot=` do not match the server |
| slow TFTP | set `tftpblocksize` and `tftpwindowsize` (RFC 7440 window); unset, the server's default block size is used |

## Verify
- [ ] `run netboot` boots a freshly built kernel without touching the SD card.
- [ ] `mount` on target shows `/` on NFS; module installs to the NFS root are visible immediately.

## Checked
2026-10-31. Confirmed against the U-Boot environment page (ipaddr, serverip, netmask, autoload, ethact, tftpblocksize, tftptimeout, tftptimeoutcountmax, tftpwindowsize, tftpdstp default port 69), the tftpput page, Kconfig BOOTMETH_EXTLINUX_PXE and the kernel NFS-root page (root=/dev/nfs, nfsroot=, ip=dhcp). Removed the host package and export commands, the `pxe get`/`pxe boot` and pxelinux.cfg claims, the example block size, `mdio list`, the literal error strings, CONFIG_ROOT_NFS/CONFIG_IP_PNP and the NFS v3 advice, which the fetched pages do not state.
Method: documentation only; no commands were run.
