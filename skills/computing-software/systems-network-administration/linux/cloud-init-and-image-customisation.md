---
id: computing-software.systems-network-administration.linux.cloud-init-and-image-customisation
name: cloud-init-and-image-customisation
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cloud-init, cloud-images, image-customisation, virt-customize, virt-sysprep, cloud-localds, nocloud, user-data, meta-data, network-config, cloud-config, datasource, image-builder, packer, golden-image, qcow2, machine-id, lpic-1, virtualisation, sysadmin, runcmd, write-files, cloud-init-status]
level: practitioner
status: docs-checked
description: "Boot cloud images with cloud-init and build your own: NoCloud seeds for KVM, cloud-config users/keys/packages/runcmd, network-config v2, cloud-init status/log debugging, virt-customize golden images."
sources:
  - https://github.com/canonical/cloud-init/blob/main/doc/rtd/reference/datasources/nocloud.rst
  - https://github.com/canonical/cloud-init/blob/main/doc/rtd/explanation/boot.rst
  - https://github.com/canonical/cloud-init/blob/main/doc/rtd/reference/cli.rst
  - https://github.com/canonical/cloud-init/blob/main/config/cloud.cfg.tmpl
  - https://github.com/libguestfs/guestfs-tools/blob/master/sysprep/virt-sysprep.pod
  - https://github.com/libguestfs/libguestfs-common/blob/master/mlcustomize/customize-options.pod
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# cloud-init and image customisation — a VM that configures itself on first boot

**Goal:** take a vendor cloud image (Ubuntu, Rocky, Debian, Fedora), hand it a seed, and
get a host with your users, keys, packages and network at first boot — then bake a
golden image when the seed gets too long.

## 1. How cloud-init works (so the logs make sense)
Five boot stages: Detect (`ds-identify`), Local (`cloud-init-local.service`; finds the datasource and applies
network config before networking), Network (`init` modules such as `bootcmd`, `write_files`, `growpart`,
`resizefs`, `disk_setup`, `mounts`, `set_hostname`, `ssh`), Config (config modules including `timezone` and
`runcmd`) and Final (`package_update_upgrade_install`, `write_files_deferred`, user scripts).
A **datasource** supplies `meta-data`, `user-data`, `network-config`: cloud provider
metadata services (EC2/GCE/Azure/OpenStack), or **NoCloud** — a `vfat` or `iso9660` filesystem labelled
`CIDATA` with the files in its root, or a `ds=nocloud;s=http://…/` kernel argument (also a `seedfrom` URL). Most
configuration is applied once per instance; `instance-id` is required in meta-data, and a new one makes it a new instance.

## 2. NoCloud seed for KVM/libvirt/Proxmox
```yaml
# user-data
#cloud-config
hostname: web1
fqdn: web1.corp.example
manage_etc_hosts: true
timezone: Europe/London
users:
  - name: ops
    groups: [sudo, wheel]           # whichever exists on the distro
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    lock_passwd: true
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... ops@laptop
ssh_pwauth: false
package_update: true
package_upgrade: true
packages: [qemu-guest-agent, chrony, vim]
write_files:
  - path: /etc/sysctl.d/90-web.conf
    content: |
      net.core.somaxconn = 4096
  - path: /etc/ssh/sshd_config.d/10-hardening.conf
    content: |
      PasswordAuthentication no
      PermitRootLogin no
runcmd:
  - systemctl enable --now qemu-guest-agent
  - [ sh, -c, "sysctl --system" ]
growpart: { mode: auto, devices: ['/'] }     # default anyway; root fs grows to the disk
resize_rootfs: true
final_message: "cloud-init done after $UPTIME s"
```
```yaml
# meta-data
instance-id: web1-001
local-hostname: web1
```
```yaml
# network-config (v2 / netplan syntax; v1 also accepted)
version: 2
ethernets:
  eth0:
    match: { name: "en*" }
    set-name: eth0
    addresses: [10.0.10.21/24]
    routes: [{ to: default, via: 10.0.10.1 }]
    nameservers: { addresses: [10.0.0.53], search: [corp.example] }
```
```bash
cloud-init schema --config-file user-data          # validate before wasting a boot
qemu-img create -f qcow2 -F qcow2 -b base/ubuntu-24.04.img web1.qcow2 40G
virt-install --name web1 --memory 2048 --vcpus 2 --import --os-variant ubuntu24.04 \
  --disk web1.qcow2 --network bridge=br0 --graphics none --noautoconsole \
  --cloud-init user-data=user-data,meta-data=meta-data,network-config=network-config
```
`virt-install --cloud-init` builds the seed ISO from those files. To build the seed yourself, use any tool that writes an iso9660 or vfat volume labelled `CIDATA` with the three files in its root.
- The first line **must** be `#cloud-config`; otherwise the file is treated as a script (and
  a script is fine: `#!/bin/bash` user-data runs at `final`).
- The shipped `cloud.cfg` has `users: [default]`, and `default_user` (name depends on the distro variant,
  for example `ubuntu`, `debian`, `cloud-user` on RHEL) is created with a locked password; a `users:` list in
  your user-data replaces that unless you include `- default`.
- `runcmd` runs **once**; `bootcmd` runs every boot (early). For idempotent config, point
  `runcmd` at Ansible/`ansible-pull` or a script you can re-run.
- Package installs happen after network — a `write_files` that configures a repo must precede
  (`write_files` runs in `init`, before `packages`).

## 3. Debugging
```bash
cloud-init status --long --wait        # done / error / running; shows failing module
cloud-init query -a | less             # merged metadata, instance-data
tail -100 /var/log/cloud-init-output.log   # stdout of runcmd/packages
grep -iE 'warn|error|fail' /var/log/cloud-init.log
cloud-init analyze show; cloud-init analyze blame     # what took time at boot
cloud-init clean --logs --reboot                      # re-run as a fresh instance (destructive: may overwrite ssh keys or passwords; not on production)
```
- No datasource found → check that the seed volume is labelled `CIDATA` (or the `ds=nocloud;s=` URL is
  reachable) and that the files sit in its root.
- To stop cloud-init generating network config, put `network: {config: disabled}` in a file under
  `/etc/cloud/cloud.cfg.d/` (or `network-config=disabled` on the kernel command line); otherwise it
  generates config, falling back to a default one when no network information is found.
- Hostname reverting each boot: `preserve_hostname: true` in a cloud.cfg.d file (the base config default is false).
- Datasource list taking long on bare metal/VMs: set `datasource_list` (single line, e.g. `[ NoCloud, None ]`)
  in a `cloud.cfg.d` file; cloud-init skips detection when the list holds a single datasource.

## 4. Golden images with libguestfs
```bash
virt-customize -a base.qcow2 --update --install qemu-guest-agent,chrony \
  --copy-in /srv/certs/corp-ca.crt:/etc/pki/ca-trust/source/anchors --run-command 'update-ca-trust' \
  --ssh-inject ops:file:ops.pub
virt-sysprep -a base.qcow2 --operations defaults,-ssh-userdir   # strips machine-id, ssh host keys, logs, udev net rules, bash history
qemu-img convert -O qcow2 -c base.qcow2 base-compressed.qcow2    # compress for distribution
virt-filesystems -a base.qcow2 --all --long -h; virt-df -a base.qcow2; virt-cat -a base.qcow2 /etc/os-release
```
- Always `virt-sysprep` before cloning: its default operations include `machine-id`, `ssh-hostkeys`,
  `udev-persistent-net`, `bash-history`, `logfiles` and `ssh-userdir` (hence `-ssh-userdir` above, so
  the injected key stays). `cloud-init clean --machine-id` is the cloud-init-side equivalent.
- `--ssh-inject USER[:SELECTOR]` needs the user to exist already; in virt-customize `--selinux-relabel` is a
  compatibility no-op, so no manual relabel step is needed. `--copy-in` needs the destination directory to exist.
- Pipeline tools: Packer with the `qemu` builder for repeatable builds, `image-builder`/
  `osbuild` (RHEL), `mkosi`, or Kickstart/autoinstall for from-scratch images. Keep the
  seed small and move static config into the image; keep per-instance things (hostname,
  keys, IPs) in cloud-init.

## Verify
- [ ] `cloud-init status` reports `done` with no errors on first boot; `ssh ops@web1` works with the injected key and no password prompt.
- [ ] `cloud-init query local_hostname` and `hostname -f` match; packages from `packages:` are installed.
- [ ] Two VMs cloned from the sysprepped image have different `/etc/machine-id` and SSH host keys.

## Checked

Checked 2026-10-26 against canonical/cloud-init (last commit 2026-10-23: doc/rtd boot, nocloud, cli, network-config, launch_libvirt pages, config/cloud.cfg.tmpl and the cloud-config JSON schema), virt-manager's virt-install.rst, and libguestfs/guestfs-tools plus libguestfs-common (virt-sysprep.pod and operation sources, customize-options.pod). Confirmed: five boot stages and which modules run in each, NoCloud CIDATA label and ds=nocloud;s= syntax, schema keys used in the example user-data, network config disable syntax, clean/status/analyze commands, virt-install --cloud-init, virt-sysprep default operations (including ssh-userdir), virt-customize --ssh-inject, --copy-in and --run-command semantics. Corrected: four stages to five; label CIDATA (uppercase); nocloud-net kernel argument removed; the clean command line; --selinux-relabel is a no-op in virt-customize. Removed: cloud-localds and genisoimage commands, the 2-minute wait claim and the distro-path claim for datasource_list.

Method: documentation only; no commands were run.
