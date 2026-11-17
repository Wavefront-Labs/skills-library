---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.enumerating-volume-shadow-copies
name: enumerating-volume-shadow-copies
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [vshadowmount, volume-shadow-copy, vss, vssadmin, dfir]
level: practitioner
status: docs-checked
description: "Enumerate shadow copies on live systems with vssadmin and expose them from disk images with vshadowmount, then plan which stores to process."
sources: ["https://github.com/libyal/libvshadow", "https://github.com/libyal/libvshadow/wiki/Mounting", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/vssadmin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enumerating volume shadow copies

**Goal:** know how many shadow copies exist before deciding which to process.

## On a disk image (Linux, libvshadow)
libvshadow accesses the Volume Shadow Snapshot (VSS) format used by Windows since Vista.
vshadowmount takes a byte offset with `-o`; if you take the offset from mmls multiply by the sector size.
```bash
mmls image.dd                                          # find NTFS partition offset (sectors)
vshadowmount -o $(( 206848 * 512 )) image.dd /mnt/vss  # exposes /mnt/vss/vshadow1 ... as raw volumes
mount -o loop,ro /mnt/vss/vshadow1 /mnt/file_system    # loop mount, Linux
```
The libvshadow wiki says to use fuse; "No sub system to mount VSHADOW" means fuse was not detected when
building. By default fuse blocks root access to the mount point: set `user_allow_other` in
`/etc/fuse.conf` and pass `-X allow_root`.

## On a live system
```cmd
vssadmin list shadows
vssadmin list shadowstorage
vssadmin list volumes
```
`list shadows` lists existing shadow copies; `list shadowstorage` lists shadow copy storage
associations; `list volumes` lists volumes eligible for shadow copies.

## Interpreting
- Each store is a point-in-time copy. Copies live on the local volume in "System Volume Information"
  using the GUID 3808876b-c176-4e48-b7ae-04046e6cc752 to identify the VSS metadata files (the catalog
  and the store files). The format notes record a creation time (a FILETIME) per catalog entry.
- `vssadmin resize shadowstorage` changes the storage limit; `vssadmin delete shadows` removes copies.

## Plan processing
- Process the latest pre-incident store and any created during the incident window.
- For deleted-file questions, process all stores and compare them.

## Gotchas
- Absence of stores on a system where you expect them may indicate deletion; confirm from other
  evidence (process creation logs, prefetch) rather than assuming.

## Verify
List of stores with creation times and the processing decision is recorded in case notes.

## Checked
Method: docs-checked 2026-11-09 against the libvshadow README, Mounting wiki and format documentation (GUID, catalog creation time) and the Microsoft Learn vssadmin page (list/delete/resize subcommands). Dropped unconfirmed items: vshadowinfo output, ewfmount step, wmic/WMI commands, restore point triggers and schedules, MaxSpace behaviour, and VSS event IDs.
