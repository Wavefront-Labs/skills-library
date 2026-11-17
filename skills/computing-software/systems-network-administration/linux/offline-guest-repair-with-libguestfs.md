---
id: computing-software.systems-network-administration.linux.offline-guest-repair-with-libguestfs
name: offline-guest-repair-with-libguestfs
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, guestfish, libguestfs, virt-rescue, virt-customize, virt-sysprep, virt-resize]
level: practitioner
status: docs-checked
description: "Repair and modify VM disk images offline with libguestfs: guestfish, virt-rescue, virt-customize, virt-cat/virt-edit, password resets, fstab fixes, and sysprep before cloning."
sources:
  - https://github.com/libguestfs/libguestfs/blob/master/fish/guestfish.pod
  - https://github.com/libguestfs/libguestfs/blob/master/rescue/virt-rescue.pod
  - https://github.com/libguestfs/guestfs-tools/blob/master/sysprep/virt-sysprep.pod
  - https://github.com/libguestfs/libguestfs-common/blob/master/mlcustomize/customize-options.pod
  - https://github.com/libguestfs/guestfs-tools/blob/master/resize/virt-resize.pod
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Offline guest repair with libguestfs

libguestfs boots a tiny appliance VM that mounts the guest's disk, so you can fix images without booting them and without loop-mounting untrusted filesystems on the host.

**Always shut the VM down first** (`virsh shutdown vm`); writing to a disk in use corrupts it. Use `--ro` for inspection of running guests.

## Inspect
```bash
virt-df -d web1 -h                     # filesystem usage inside the guest
virt-filesystems -a disk.qcow2 --all --long -h
virt-cat -d web1 /var/log/messages | tail
virt-ls -lR -d web1 /etc/ssh
virt-inspector -a disk.qcow2 | less    # OS, apps, mountpoints as XML
```

## Edit files
```bash
virt-edit -d web1 /etc/fstab                     # opens $EDITOR on the guest file
virt-edit -d web1 /etc/fstab -e 's/^UUID=dead.*//'   # non-interactive perl expression
virt-copy-out -d web1 /var/log/journal ./journal-web1
virt-copy-in -d web1 fixed.conf /etc/nginx/
```

## Interactive guestfish
```bash
guestfish -d web1 -i          # -i: inspect and mount the guest's filesystems automatically
><fs> cat /etc/default/grub
><fs> edit /etc/selinux/config
><fs> ln-sf /dev/null /etc/systemd/system/broken.service   # mask a unit that hangs boot
><fs> touch /.autorelabel     # after changes on SELinux guests
><fs> exit
```
LVM/LUKS: `guestfish --keys-from-stdin -i -a disk.qcow2` prompts for the passphrase.

## Rescue shell
`virt-rescue -d web1` gives a shell in the rescue appliance (not in the guest): you must mount the guest's filesystems yourself, on the empty `/sysroot` directory (or add `-i` to mount them automatically). Use `--ro` for live VMs. Then repair tools from the appliance can run against the guest disk:
```bash
><rescue> mount /dev/vg0/root /sysroot; mount /dev/vda1 /sysroot/boot     # device names as in the virt-rescue(1) example; check yours
><rescue> chroot /sysroot
```

## Common fixes with virt-customize
```bash
virt-customize -d web1 --root-password password:'Tmp-Pass-2026'
virt-customize -a disk.qcow2 --ssh-inject root:file:./id_ed25519.pub     # the user must already exist; --selinux-relabel is a compatibility no-op
virt-customize -a disk.qcow2 --run-command 'systemctl disable cloud-init' --install vim
```

## Before cloning: virt-sysprep
```bash
virt-sysprep -a golden.qcow2 --operations defaults,-ssh-userdir --hostname template
```
The default operations include `ssh-hostkeys`, `machine-id`, `logfiles`, `udev-persistent-net`, `dhcp-client-state` and `ssh-userdir` (excluded above with `-ssh-userdir`) so clones don't collide; `virt-sysprep --list-operations` shows which are on by default.

## Resize
`virt-resize --expand /dev/sda2 old.qcow2 new.qcow2` after creating the output disk at the larger size (`qemu-img create -f qcow2 new.qcow2 40G`; the virt-resize man page's step 4 is "create output disk").

## Verify
- [ ] Guest boots cleanly after the change; SELinux guests relabelled (no mass AVCs).
- [ ] Clones from a sysprepped image get unique machine-ids and SSH host keys.

## Checked

Checked 2026-10-26 against libguestfs/libguestfs (last commit 2026-10-16: guestfish.pod, virt-rescue.pod, virt-copy-in.pod), libguestfs/guestfs-tools (last commit 2026-10-19: virt-sysprep.pod and operation sources, virt-edit.pod, virt-resize.pod, virt-ls.pod, virt-cat.pod) and libguestfs-common customize-options.pod. Confirmed: guestfish -i, --ro and --keys-from-stdin, virt-rescue /sysroot and -i, virt-edit -e and $EDITOR, virt-customize --root-password, --ssh-inject, --run-command, --hostname, virt-sysprep default operations and --operations syntax, virt-resize output-disk step. Corrected: virt-rescue gives a shell in the appliance and the guest must be mounted under /sysroot (the example uses /dev/vda1, not /dev/sda); virt-customize --selinux-relabel is a no-op; the virt-sysprep default operation list is stated from the operation sources.

Method: documentation only; no commands were run.
