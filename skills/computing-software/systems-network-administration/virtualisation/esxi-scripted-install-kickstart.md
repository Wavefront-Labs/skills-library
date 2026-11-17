---
id: computing-software.systems-network-administration.virtualisation.esxi-scripted-install-kickstart
name: esxi-scripted-install-kickstart
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-installation, esxi-install, esxi-kickstart, ks-cfg, scripted-install, pxe, vmware, esxi, vsphere, automation]
level: practitioner
status: docs-checked
description: "Install ESXi unattended with a kickstart ks.cfg: install/network/rootpw directives, %firstboot scripts, delivery by USB, HTTP or PXE, and how to debug failures."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/7-0/esx-upgrade/upgrading-esxi-hosts-upgrade/installing-upgrading-or-migrating-hosts-using-a-script-upgrade/installing-esxi-by-using-a-script-upgrade/installation-and-upgrade-script-commands-upgrade.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ESXi scripted install with kickstart

**Goal:** identical ESXi hosts in minutes, with the management network, root password and
baseline settings applied before anyone touches the DCUI.

## 1. Minimal ks.cfg
```
vmaccepteula
install --firstdisk=local --overwritevmfs
# or: install --disk=naa.<id> --novmfsondisk
rootpw --iscrypted <SHA512_HASH>
keyboard 'US Default'
network --bootproto=static --device=vmnic0 --ip=<IP> --netmask=<MASK> \
        --gateway=<GW> --nameserver=<DNS1>,<DNS2> --hostname=<FQDN> --vlanid=<VLAN>
reboot

%firstboot --interpreter=busybox
# set NTP, DNS search domain and other baseline settings with the esxcli equivalents
esxcli system syslog config set --loghost='udp://<SYSLOG>:514' && esxcli system syslog reload
```
- `--firstdisk` takes an ordered preference list of disk types and models (for example
  `--firstdisk=ST3120814A,mptsas,local`). Use `--disk=naa.<id>` when a host sees SAN LUNs: a wrong
  `--firstdisk` guess can wipe a shared VMFS datastore. Safest is to present no LUNs during
  install.
- `--overwritevmfs` is required when the target disk already holds VMFS (reinstalls).
- Generate the hash with `openssl passwd -6`. Plain `rootpw <pw>` works but leaves the
  password readable on your web server.
- `%pre` runs before install (busybox), `%post` after install in the installer
  environment, `%firstboot` once on first boot of the installed system. Most `esxcli`
  configuration belongs in `%firstboot`.

## 2. Delivering the script
| Method | How |
|---|---|
| Boot prompt | Press Shift+O at the installer boot and append the kickstart file location (`ks=...`) |
| Custom ISO | Edit `BOOT.CFG` (and its EFI variant) and add the `ks=` location to `kernelopt` |
| PXE / UEFI HTTP boot | Serve the ESXi files plus `boot.cfg` with `prefix=` and the `kernelopt` line |
Per-host files (one ks.cfg per MAC or hostname) avoid needing DHCP reservations for the static IP.

## 3. Gotchas
- Check Secure Boot interactions before injecting custom VIBs; prefer vendor (OEM)
  images rather than injecting drivers.
- `network --device` uses vmnic naming; if the NIC order differs by model, pin the
  device explicitly for the model.
- ESXi 7+ partition layout: OSDATA is sized from the boot disk; on small media pass
  `systemMediaSize=min` in the boot options (see the boot media skill).
- Typos in ks.cfg drop you to an interactive error screen; nothing is logged remotely.

## Verify
- Check the installer log on the newly installed host before first login.
- After first boot: check the network, NTP and syslog configuration with the
  corresponding esxcli commands.
- Join to vCenter and run a host profile compliance check to catch drift from the build.

## Checked
2026-10-31: `vmaccepteula`, `install` with `--firstdisk`/`--overwritevmfs`/`--novmfsondisk`, `rootpw --iscrypted`, the `network` command flags, `%pre`/`%post`/`%firstboot` sections, and the example `--firstdisk=ST3120814A,mptsas,local` confirmed on the Installation and Upgrade Script Commands page; the `systemMediaSize` boot option and `kernelopt` usage confirmed in KB 81166; `esxcli system syslog config set --loghost` confirmed in KB 2003322. Removed unconfirmed specifics: esxcli DNS/NTP flag lines, `vim-cmd hostsvc/enable_ssh`, `SuppressShellWarning`, exact `ks=` boot codes, `/var/log/esxi_install.log` and `/var/log/weasel.log` paths.
Method: documentation only; no commands were run.
