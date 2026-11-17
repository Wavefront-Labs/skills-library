---
id: computing-software.systems-network-administration.backup-and-recovery.clonezilla-disk-imaging
name: clonezilla-disk-imaging
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [clonezilla, bare-metal-recovery, disk-imaging, partclone, ocs-sr, system-image]
level: practitioner
status: docs-checked
description: "Image and restore whole disks or partitions with Clonezilla Live: savedisk/restoredisk, image repositories, ocs-sr options, restoring to larger disks, and its limits."
sources:
  - https://clonezilla.org/clonezilla-live-doc.php
  - https://clonezilla.org/fine-print-live-doc.php?path=clonezilla-live/doc/98_ocs_related_command_manpages
  - https://clonezilla.org/show-live-doc-content.php?topic=clonezilla-live/doc/01_Save_disk_image
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clonezilla disk imaging

**Goal:** an offline, bootable-restore image of a machine's disks, for bare-metal recovery or before risky changes.

## How it works
Boot Clonezilla Live. Clonezilla is based on DRBL, Partclone and udpcast; with `-q2` it uses partclone to save partitions (priority partclone, then partimage, then `dd`), and `-q1` forces `dd`, which is slow but works for all file systems. Images go to an **image repository** such as a local disk or a network file system (the project mentions sshfs and Samba); check the Clonezilla Live documentation for the full list your version offers.

## Save
Menu: device-image -> repository -> Beginner/Expert -> savedisk (whole disk) or saveparts.
Command equivalent:
```sh
ocs-sr -q2 -c -j2 -z9p -i 4096 -sfsck -senc -p poweroff savedisk srv01-2026-10-17 sda
```
`-q2` partclone priority, `-j2` copy the data between the MBR and the first partition, `-z9p` multithreaded zstd, `-i 4096` split size in MB, `-sfsck` skip the source-partition fsck, `-senc` skip encrypting the image, `-p` post action. The image is checked for restorability after saving; `-scs` (`--skip-check-restorable-s`) skips that check, so omit it unless time-critical.

## Restore
```sh
ocs-sr -g auto -e1 auto -e2 -r -j2 -k1 -scr -p reboot restoredisk srv01-2026-10-17 sda
```
- `-k1` creates the partition table proportionally to the target disk size.
- `-icds` ignores the disk-size check (risky if the data does not fit).
- `-g auto` installs GRUB in the MBR (the argument can be `auto` or a device name); `-e1` changes the NTFS boot-partition geometry and `-e2` loads geometry from EDD; `-scr` skips the check that the image is restorable before restoring; `-r` resizes the partition to fit the target partition size.

## Uses and limits
- Good for: golden images, pre-upgrade images, appliances and labs; Clonezilla SE (Server Edition) clones many machines at once for massive deployment.
- Not a backup system: it images a machine that is booted into Clonezilla Live (offline), so plan regular backups separately.
- Keep BitLocker recovery keys before imaging Windows machines.
- Windows cloned to many machines needs sysprep first (unique SIDs/hostnames).

## Verify
Restore the image to a spare disk or VM and boot it; check filesystems and services.

## Checked

Checked 2026-10-27 against the Clonezilla sources in stevenshiau/clonezilla (doc/ocs-sr.8, sbin/ocs-sr and README) and the clonezilla.org Clonezilla Live page. Confirmed: the `ocs-sr` options `-q1`, `-q2`, `-j2`, `-z9p`, `-i`, `-sfsck`, `-scs`, `-scr`, `-senc`, `-p`, `-g`, `-k1`, `-e1`, `-e2`, `-r` and `-icds`, the partclone > partimage > dd priority, the `dd` fallback, and Clonezilla SE for massive deployment. Removed the unconfirmed filesystem list, the repository protocol list, the LUKS/BitLocker dd claim and the incremental and scheduling remarks that the sources do not state. The repository note reflects the sshfs and Samba mention on the Clonezilla Live page.

Method: documentation only; no commands were run.
