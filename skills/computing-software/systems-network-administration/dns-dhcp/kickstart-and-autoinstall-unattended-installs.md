---
id: computing-software.systems-network-administration.dns-dhcp.kickstart-and-autoinstall-unattended-installs
name: kickstart-and-autoinstall-unattended-installs
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [pxe, kickstart, autoinstall, unattended-install, cloud-init, network-boot]
level: practitioner
status: draft
description: "Automate network installs with RHEL Kickstart and Ubuntu autoinstall (cloud-init) from PXE/iPXE: kernel arguments, config serving, validation and per-host data."
sources:
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/automatically_installing_rhel/index
  - https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-reference.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kickstart and autoinstall

## RHEL/Rocky/Alma: Kickstart
Boot entry (GRUB/iPXE):
```
linuxefi images/rhel9/vmlinuz inst.repo=http://10.0.0.20/rhel9 inst.ks=http://10.0.0.20/ks/base.ks ip=dhcp
initrdefi images/rhel9/initrd.img
```
Minimal `base.ks`:
```
text
lang en_GB.UTF-8
keyboard gb
timezone Europe/London --utc
rootpw --lock
user --name=ops --groups=wheel --iscrypted --password=$6$...
network --bootproto=dhcp --hostname=host.example.com
zerombr
clearpart --all --initlabel
autopart --type=lvm
%packages
@^minimal-environment
%end
reboot
```
Validate: `ksvalidator base.ks`. Logs during install: `/tmp/anaconda.log`, Ctrl+Alt+F2 shell.

## Ubuntu Server 20.04+: autoinstall
Boot entry:
```
linux /ubuntu/casper/vmlinuz ip=dhcp url=http://10.0.0.20/ubuntu-24.04-live-server-amd64.iso autoinstall ds=nocloud-net;s=http://10.0.0.20/autoinstall/
initrd /ubuntu/casper/initrd
```
Serve `user-data` and an empty `meta-data` at that URL:
```yaml
#cloud-config
autoinstall:
  version: 1
  identity: { hostname: host1, username: ops, password: "$6$..." }
  ssh: { install-server: true, authorized-keys: ["ssh-ed25519 AAAA..."] }
  storage: { layout: { name: lvm } }
  late-commands: [ "curtin in-target -- systemctl enable ssh" ]
```
In GRUB escape `;` as `\;` or quote the `ds=` argument. Validate with `cloud-init schema -c user-data`.

## Per-host data
iPXE scripts with `${mac}` or `${serial}` select host-specific config URLs; generate configs from
inventory (NetBox) rather than editing by hand.

## Verify
- [ ] A test VM boots via PXE and installs without prompts, reboots into the OS with the expected hostname, user and SSH key.
