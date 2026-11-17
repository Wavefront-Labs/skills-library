---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.refs-forensics
name: refs-forensics
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [refs-forensics, filesystem-forensics, windows-server, storage-spaces, dfir]
level: advanced
status: draft
description: "Approach ReFS volumes on Windows Server and Storage Spaces: version differences, limited tool support, metadata structures, integrity streams and acquisition advice."
sources: ["https://learn.microsoft.com/en-us/windows-server/storage/refs/refs-overview", "https://github.com/libyal/libfsrefs", "https://www.sciencedirect.com/journal/forensic-science-international-digital-investigation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ReFS forensics

**Goal:** Resilient File System is used on Windows Server for Hyper-V storage, backup repositories
(Veeam block cloning) and Storage Spaces Direct. Forensic tooling is far less mature than for NTFS.

## Know the version
- ReFS 1.x (Server 2012/2012 R2), 3.x (Server 2016+, Windows 10/11 Pro for Workstations). Major
  on-disk changes between versions: check with `fsutil fsinfo refsinfo X:` live, or the boot sector of the image.

## What differs from NTFS
- No `$MFT`; metadata in B+ tables (object table, directory tables) with copy-on-write: old
  metadata pages may survive after updates, which can help recovery.
- No USN-like journal by default in early versions; ReFS 3.x supports USN journal (`fsutil usn` works).
- No EFS, no short names, no hard links (on older versions), no disk quotas.
- **Integrity streams**: per-file checksums (optional; enabled on Storage Spaces mirrors).
- **Block cloning**: files sharing clusters (backup synthetic fulls) - deleting one does not free shared blocks.

## Tools
- Live analysis on Windows (the most reliable): collect file listings with timestamps (PowerShell
  `Get-ChildItem -Recurse | Select FullName,CreationTimeUtc,LastWriteTimeUtc,Length`), event logs.
- Images: mount on a Windows analysis host of the same or newer ReFS version (Arsenal Image Mounter read-only).
  Commercial tools (X-Ways, some versions of EnCase/AXIOM) and research tools (libfsrefs, Paragon ReFS) have partial support; TSK lacks ReFS.
- Validate any recovery tool on a test ReFS volume of the same version first.

## Gotchas
- Mounting a ReFS image on an older Windows can fail; newer Windows may upgrade the volume version on read-write mount - mount read-only only.
- Storage Spaces: the ReFS volume sits on a virtual disk spread across physical disks; acquire all member disks and reconstruct the pool (or image the virtual disk live).

## Verify
Record ReFS version and the method used, and validate recovered artefacts against a test volume.
