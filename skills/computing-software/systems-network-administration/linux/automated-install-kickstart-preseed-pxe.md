---
id: computing-software.systems-network-administration.linux.automated-install-kickstart-preseed-pxe
name: automated-install-kickstart-preseed-pxe
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, kickstart, preseed, autoinstall, subiquity, pxe, pxe-boot, unattended-install, network-boot, tftp, dnsmasq, ipxe, grub-efi, pxelinux, syslinux, anaconda, debian-installer, cloud-init, ks-cfg, ksvalidator, inst-ks, bare-metal-provisioning, lpic-2, sysadmin, ks-post, preseed-cfg, proxy-dhcp, autoinstall-yaml]
level: advanced
status: draft
description: "Install Linux hands-free: Kickstart (RHEL-family), preseed (Debian), autoinstall (Ubuntu subiquity), and a dnsmasq PXE/iPXE boot server for BIOS and UEFI clients."
sources:
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/automatically_installing_rhel/index
  - https://pykickstart.readthedocs.io/en/latest/kickstart-docs.html
  - https://www.debian.org/releases/stable/amd64/apbs02.en.html
  - https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-reference.html
  - https://dnsmasq.org/docs/dnsmasq-man.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated installation — Kickstart, preseed, autoinstall and PXE

**Goal:** boot a bare-metal or VM host from the network (or a USB stick) and get a
fully installed, configured, reproducible OS with nobody touching a keyboard.

Three families, three answer files:
| Distro | Installer | Answer file | Boot parameter |
|---|---|---|---|
| RHEL, Rocky, Alma, Fedora, CentOS Stream | anaconda | Kickstart `ks.cfg` | `inst.ks=http://…/ks.cfg` |
| Debian | debian-installer (d-i) | preseed `preseed.cfg` | `auto=true priority=critical url=http://…/preseed.cfg` |
| Ubuntu Server ≥ 20.04 | subiquity | autoinstall `user-data` (cloud-init format) | `autoinstall ds=nocloud-net;s=http://…/` |

## 1. Kickstart (RHEL-family)
Every interactive install leaves `/root/anaconda-ks.cfg` — the best starting point.
```
# ks.cfg — RHEL 9 / Rocky 9
text
lang en_US.UTF-8
keyboard us
timezone UTC --utc
network --bootproto=dhcp --device=link --activate --hostname=node01.example.com
rootpw --iscrypted $6$...                 # openssl passwd -6  (or: rootpw --lock)
user --name=ops --groups=wheel --password=$6$... --iscrypted
sshkey --username=ops "ssh-ed25519 AAAA..."
firewall --enabled --service=ssh
selinux --enforcing
services --enabled=sshd,chronyd
bootloader --location=mbr --append="console=ttyS0,115200"
zerombr
clearpart --all --initlabel
autopart --type=lvm                       # or explicit: part /boot --size=1024 ; part pv.01 --grow ; volgroup vg0 pv.01 ; logvol / --vgname=vg0 --size=20480 --name=root
reboot --eject
url --url=https://download.rockylinux.org/pub/rocky/9/BaseOS/x86_64/os/
repo --name=AppStream --baseurl=https://download.rockylinux.org/pub/rocky/9/AppStream/x86_64/os/
%packages
@^minimal-environment
chrony
vim-enhanced
-iwl*-firmware
%end
%post --log=/root/ks-post.log
dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
systemctl enable sshd
%end
```
- Validate: `dnf install pykickstart && ksvalidator -v RHEL9 ks.cfg`.
- `%post` runs chrooted in the installed system (use `--nochroot` to see the installer
  env); network is up only if `network --activate` was used. `%pre` runs before
  partitioning (dynamic disk selection scripts).
- Serve `ks.cfg` over HTTP and boot with `inst.ks=http://host/ks.cfg inst.repo=…`
  (or `inst.ks=hd:LABEL=OEMDRV:/ks.cfg` from a USB labelled `OEMDRV`, which anaconda
  picks up automatically). Add `inst.text console=ttyS0` for headless; `inst.sshd`
  for debugging; `inst.noverifyssl` only in labs. Ctrl-Alt-F2 / `inst.vnc` get you a shell
  when it stalls; `/tmp/anaconda.log`, `/tmp/storage.log`, `/tmp/program.log` are the logs.
- Embed into an ISO for VMware/USB: `mkksiso --ks ks.cfg in.iso out.iso` (`lorax` package).
- Wrong disk wiped: pin with `ignoredisk --only-use=sda` or `--drives=` arguments.

## 2. preseed (Debian)
```
# preseed.cfg — Debian 12
d-i debian-installer/locale string en_US.UTF-8
d-i keyboard-configuration/xkb-keymap select us
d-i netcfg/choose_interface select auto
d-i netcfg/get_hostname string node01
d-i netcfg/get_domain string example.com
d-i mirror/country string manual
d-i mirror/http/hostname string deb.debian.org
d-i mirror/http/directory string /debian
d-i mirror/http/proxy string
d-i passwd/root-login boolean false
d-i passwd/user-fullname string Ops
d-i passwd/username string ops
d-i passwd/user-password-crypted password $6$...
d-i clock-setup/utc boolean true
d-i time/zone string UTC
d-i partman-auto/method string lvm
d-i partman-auto/disk string /dev/sda
d-i partman-auto-lvm/guided_size string max
d-i partman-auto/choose_recipe select atomic
d-i partman-partitioning/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true
d-i partman-lvm/confirm boolean true
d-i partman-lvm/confirm_nooverwrite boolean true
d-i partman-lvm/device_remove_lvm boolean true
d-i partman-md/device_remove_md boolean true
tasksel tasksel/first multiselect ssh-server, standard
d-i pkgsel/include string vim sudo
d-i pkgsel/upgrade select full-upgrade
popularity-contest popularity-contest/participate boolean false
d-i grub-installer/only_debian boolean true
d-i grub-installer/bootdev string /dev/sda
d-i finish-install/reboot_in_progress note
d-i preseed/late_command string in-target usermod -aG sudo ops; \
    in-target install -d -m 0700 -o ops -g ops ~ops/.ssh; \
    in-target sh -c "echo 'ssh-ed25519 AAAA...' > ~ops/.ssh/authorized_keys; chown ops:ops ~ops/.ssh/authorized_keys"
```
- Check syntax: `debconf-set-selections -c preseed.cfg`. Get every question the
  installer asked on a reference host: `debconf-get-selections --installer` (package
  `debconf-utils`).
- The dreaded partman confirms: each `confirm` line above suppresses one prompt; a
  missing one halts the install at a dialog. Boot with `priority=critical` so only
  unanswered critical questions stop it.
- `late_command` runs in the installer environment; `in-target` runs inside the new
  system. Use `/target/...` paths otherwise.
- Boot args: `auto=true priority=critical url=http://host/preseed.cfg interface=auto
  netcfg/get_hostname=node01` (the `auto` alias delays network questions until the
  file is fetched). For USB, put `preseed.cfg` at the ISO root and add
  `file=/cdrom/preseed.cfg`.

## 3. autoinstall (Ubuntu Server 20.04+)
`user-data` is a cloud-init file with an `autoinstall:` key; `meta-data` must exist
(may be empty). Serve both from a directory.
```yaml
#cloud-config
autoinstall:
  version: 1
  locale: en_US.UTF-8
  keyboard: {layout: us}
  refresh-installer: {update: true}
  network:
    network:
      version: 2
      ethernets:
        alleth: {match: {name: "en*"}, dhcp4: true}
  storage:
    layout: {name: lvm, sizing-policy: all}   # or a curtin 'config:' list for custom layouts
  identity:
    hostname: node01
    username: ops
    password: "$6$..."            # mkpasswd -m sha-512 (package whois)
  ssh:
    install-server: true
    allow-pw: false
    authorized-keys: ["ssh-ed25519 AAAA..."]
  packages: [vim, chrony]
  apt:
    primary: [{arches: [default], uri: http://archive.ubuntu.com/ubuntu}]
  late-commands:
    - curtin in-target --target=/target -- usermod -aG sudo ops
  user-data:                      # plain cloud-init run on first boot of the installed system
    timezone: UTC
```
- Boot: `autoinstall ds=nocloud-net\;s=http://host/dir/` (note the trailing slash; in
  GRUB the `;` must be escaped as `\;`). Without `autoinstall` on the kernel line the
  installer asks "Continue with autoinstall?" once.
- Validate: `cloud-init schema --config-file user-data` on a 22.04+ box; logs live in
  `/var/log/installer/` after install and `/var/log/installer/autoinstall-user-data`
  is the regenerated file. Shell during install: Ctrl-Alt-F2 or add `interactive-sections: [storage]`
  to stop at one screen.
- `identity` is ignored if `user-data` creates users — pick one.
- Desktop ISOs ≥ 23.04 also support autoinstall; older desktop releases need the
  legacy `ubiquity` preseed.

## 4. PXE boot server (BIOS + UEFI) with dnsmasq
One box runs DHCP (or proxy-DHCP next to an existing DHCP server), TFTP and HTTP.
```bash
apt install dnsmasq nginx syslinux-common pxelinux shim-signed grub-efi-amd64-signed
# or: dnf install dnsmasq nginx syslinux shim-x64 grub2-efi-x64
mkdir -p /srv/tftp/{bios,efi,images} /srv/http
```
`/etc/dnsmasq.d/pxe.conf`:
```
interface=eth1
bind-interfaces
dhcp-range=10.10.0.100,10.10.0.200,12h         # omit and use dhcp-range=10.10.0.0,proxy for proxy-DHCP
enable-tftp
tftp-root=/srv/tftp
# client architecture (RFC 4578 option 93): 0 = BIOS, 7/9 = x64 UEFI
dhcp-match=set:efi-x86_64,option:client-arch,7
dhcp-match=set:efi-x86_64,option:client-arch,9
dhcp-match=set:bios,option:client-arch,0
dhcp-boot=tag:bios,bios/pxelinux.0
dhcp-boot=tag:efi-x86_64,efi/shimx64.efi       # shim → grubx64.efi → grub.cfg (Secure Boot friendly)
log-dhcp
```
BIOS: copy `pxelinux.0`, `ldlinux.c32`, `menu.c32`, `libutil.c32` into `/srv/tftp/bios`
and write `bios/pxelinux.cfg/default`:
```
DEFAULT menu.c32
TIMEOUT 50
LABEL rocky9
  KERNEL ../images/rocky9/vmlinuz
  APPEND initrd=../images/rocky9/initrd.img inst.repo=http://10.10.0.1/rocky9 inst.ks=http://10.10.0.1/ks.cfg ip=dhcp
LABEL ubuntu2404
  KERNEL ../images/ubuntu2404/vmlinuz
  APPEND initrd=../images/ubuntu2404/initrd ip=dhcp url=http://10.10.0.1/ubuntu-24.04-live-server-amd64.iso autoinstall ds=nocloud-net;s=http://10.10.0.1/ubuntu/
LABEL debian12
  KERNEL ../images/debian12/linux
  APPEND initrd=../images/debian12/initrd.gz auto=true priority=critical url=http://10.10.0.1/preseed.cfg
```
UEFI: copy `shimx64.efi` and `grubx64.efi` (from `shim-signed`/`grub-efi-amd64-signed`
on Debian: `/usr/lib/shim/shimx64.efi.signed`, `/usr/lib/grub/x86_64-efi-signed/grubnetx64.efi.signed`
→ rename to `grubx64.efi`) into `/srv/tftp/efi` and write `efi/grub.cfg` with
`menuentry` blocks whose `linux`/`initrd` lines carry the same arguments (paths
relative to the TFTP root, e.g. `linux /images/rocky9/vmlinuz inst.ks=...`).
Kernel/initrd sources: RHEL-family `images/pxeboot/{vmlinuz,initrd.img}` from the ISO;
Debian `netboot/debian-installer/amd64/{linux,initrd.gz}` from the mirror; Ubuntu
`casper/{vmlinuz,initrd}` from the live-server ISO, with the whole ISO served over
HTTP (`url=`). Mount ISOs under `/srv/http` with `mount -o loop,ro` and an fstab entry.

iPXE (`ipxe.efi`/`undionly.kpxe` from the `ipxe` package) replaces both bootloaders with
one HTTP-capable loader and a scripted menu (`chain http://10.10.0.1/boot.ipxe`);
chainload it from dnsmasq with `dhcp-match=set:ipxe,175` + `dhcp-boot=tag:ipxe,http://…/boot.ipxe`
so iPXE does not loop fetching itself. Worth it once you have more than three images.

Debugging: `journalctl -fu dnsmasq` shows the DHCP offer and TFTP requests (file names
reveal BIOS vs UEFI and the arch option); `tcpdump -i eth1 port 67 or port 69`;
`tftp 10.10.0.1 -c get bios/pxelinux.0` from a client proves TFTP; firewall must allow
udp/67-69 and tcp/80. A client that gets DHCP but shows `PXE-E53: No boot filename
received` means the `dhcp-boot` tag did not match its arch. UEFI clients with Secure
Boot refuse unsigned `grubx64.efi` — use the shim chain or disable Secure Boot in the lab.
Large initrds over TFTP are slow: raise `tftp-mtu`/use blocksize or move to iPXE+HTTP.

## 5. Reproducibility and secrets
- Answer files contain hashed passwords and SSH keys only; never cleartext passwords
  (`rootpw --plaintext` is for labs). Serve them from a network only installers reach,
  or generate per-host files from a template (Jinja via a tiny web app, or Foreman/Cobbler/
  MAAS if the fleet justifies it).
- First-boot configuration belongs in cloud-init/Ansible, not `%post` — keep the install
  file to "get me to SSH with the right key".
- Version-control the answer files; the `/var/log/installer` or `/root/anaconda-ks.cfg`
  on a finished host is the audit trail.

**Unconfirmed:** exact signed-bootloader file names vary by distro version; `dpkg -L
shim-signed grub-efi-amd64-signed` / `rpm -ql shim-x64 grub2-efi-x64` lists them.

## Verify
- [ ] `ksvalidator` / `debconf-set-selections -c` / `cloud-init schema` passes.
- [ ] A VM booted with the kernel line (no PXE) installs to a login prompt with zero
      prompts and SSH works with the injected key.
- [ ] A BIOS VM and a UEFI VM both reach the PXE menu from the dnsmasq server
      (`journalctl -u dnsmasq` shows both `pxelinux.0` and `shimx64.efi` served).
- [ ] The install log (`/root/anaconda-ks.cfg`, `/var/log/installer/`) matches the
      answer file in version control.
