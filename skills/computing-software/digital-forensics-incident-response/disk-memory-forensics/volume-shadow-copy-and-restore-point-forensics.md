---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.volume-shadow-copy-and-restore-point-forensics
name: volume-shadow-copy-and-restore-point-forensics
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [volume-shadow-copy, vss, vssadmin, vshadowmount, libvshadow, arsenal-image-mounter, restore-point, shadow-copy-deletion, ransomware-anti-forensics, prior-file-versions, deleted-file-recovery, windows-forensics, dfir, vss-symlink]
level: advanced
status: draft
description: "Enumerate, mount and mine Volume Shadow Copies (vssadmin, vshadowmount, mklink, Arsenal Image Mounter) for earlier file versions, and spot VSS deletion as anti-forensics."
sources: ["https://github.com/libyal/libvshadow", "https://arsenalrecon.com/products/arsenal-image-mounter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume Shadow Copy and restore point forensics

**Goal:** pull an earlier state of the filesystem — a file before ransomware
encrypted it, a registry key before an attacker modified it, a deleted file that still
exists in a snapshot taken before the deletion — out of VSS snapshots on a live system
or a disk image.

## 1. On a live system or mounted image
```
vssadmin list shadows                     # enumerate shadow copies, their creation time, volume
vssadmin list shadowstorage                # how much disk is allocated to VSS, diagnostic
mklink /d <MOUNT_DIR>\shadow_mount \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyN\
```
`mklink` to the shadow device gives read access to that snapshot's full filesystem via
a normal path — copy out the file(s) you need, don't modify anything under the mount.
This requires admin rights on the live box and only shows shadows still present (VSS
storage is capped and rotates out old shadows automatically, separate from any
deliberate deletion).

## 2. On a disk image (offline, preferred for evidence)
```
vshadowinfo -o <offset> image.E01          # list VSS stores (libvshadow, part of libyal/sleuthkit ecosystem)
vshadowmount -o <offset> image.E01 /mnt/vss/
```
`vshadowmount` (Linux/FUSE) exposes each store as `/mnt/vss/vss1`, `vss2`, ... — mount
each as a loopback NTFS filesystem and browse it with normal tools, entirely offline
against the image, no risk to the original evidence. On Windows, **Arsenal Image
Mounter** mounts the E01/raw image itself as a virtual disk, then Windows' own VSS
stack can enumerate and mount shadows on that virtual disk exactly as it would on a
live system — useful when you need shadows at specific points, not just the latest.

## 3. What you actually find
- Earlier versions of files modified or deleted since the shadow was taken — the
  single most useful VSS use case in ransomware cases: pre-encryption copies of
  business files sometimes survive in a shadow the attacker didn't find/delete.
- Earlier registry hive states (`HarddiskVolumeShadowCopyN\Windows\System32\config\
  SYSTEM`) — lets you diff a key's value before/after an intrusion without relying on
  the live hive's last-written time alone.
- Restore points (pre-Windows 10, or re-enabled) store a parallel structure
  (`rp.log`, `A0000123.*` renamed files) referenced from the shadow; less common on
  modern builds where VSS underlies File History/System Restore directly rather than
  the old discrete restore-point folders.

## 4. VSS deletion as anti-forensics
`vssadmin delete shadows /all` (or `/for=C:`) is a standard step in many ransomware
playbooks specifically to remove this recovery path before or during encryption.
Finding evidence of this command's **execution** (Prefetch/Amcache for `vssadmin.exe`,
command-line logging via Sysmon Event ID 1 or 4688 with full command line enabled, see
computing-software.digital-forensics-incident-response.log-analysis.windows-event-log-threat-hunting)
is itself a significant finding even when no shadows survive to mount — it establishes
intent and timeline. Also check `vssadmin list shadowstorage` sizing changes and
Windows Event ID 8224 (VSS service) / 524 (System Restore) for deletion-adjacent
service activity.

## Verify
- When mounting shadows from an image, work on a copy/read-only mount — `vshadowmount`
  is read-only by design, but double-check any Windows-side mount isn't accidentally
  against the original evidence file.
- Confirm a "recovered" pre-incident file's content differs meaningfully from the
  current state before citing it as proof of prior content — some files are
  legitimately unchanged.
- If shadows are absent, explicitly check for `vssadmin delete` execution evidence
  before concluding "no shadows existed" — absence can be anti-forensics, not absence
  of backups ever having run.

Unconfirmed: VSS retention/rotation behaviour (how many shadows survive, for how long)
depends on configured shadow storage size and system activity — don't assume a fixed
retention window without checking `vssadmin list shadowstorage` on the specific host.
