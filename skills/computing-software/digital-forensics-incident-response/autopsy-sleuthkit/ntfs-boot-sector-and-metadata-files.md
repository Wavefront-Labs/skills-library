---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.ntfs-boot-sector-and-metadata-files
name: ntfs-boot-sector-and-metadata-files
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [ntfs-boot-sector, ntfs, vbr, ntfs-metadata-files, sleuth-kit, dfir]
level: advanced
status: draft
description: "Analyse the NTFS $Boot volume boot record and system metadata files ($MFTMirr, $Volume, $Bitmap, $Secure, $Extend): fields, TSK commands and tampering or recovery uses."
sources: ["https://www.sleuthkit.org/sleuthkit/man/fsstat.html", "https://www.sleuthkit.org/sleuthkit/man/istat.html", "https://github.com/libyal/libfsntfs/blob/main/documentation/New%20Technologies%20File%20System%20(NTFS).asciidoc", "https://flatcap.github.io/linux-ntfs/ntfs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NTFS $Boot (VBR) and metadata files

NTFS reserves MFT entries 0 to 15 for system files. The volume boot record at sector 0 of the volume (`$Boot`, MFT entry 7) tells every tool where the MFT is. Damage or tampering here breaks parsing; understanding it lets you recover volumes and spot anomalies.

## $Boot fields (first sector)
| Offset | Field |
|---|---|
| 0x03 | OEM ID `NTFS    ` |
| 0x0B | Bytes per sector (usually 512) |
| 0x0D | Sectors per cluster |
| 0x28 | Total sectors |
| 0x30 | MFT starting cluster |
| 0x38 | $MFTMirr starting cluster |
| 0x40 | Clusters per MFT record (signed; 0xF6 = -10 means 2^10 = 1024 bytes) |
| 0x48 | Volume serial number (8 bytes; the low 4 bytes appear in LNK files and prefetch) |
| 0x1FE | Signature 0x55AA |
A backup copy of the boot sector is at the **last sector of the volume**.

## TSK
```bash
mmls image.E01                       # find partition offset
fsstat -o 2048 image.E01             # volume serial, cluster size, MFT location, version
istat -o 2048 image.E01 7            # $Boot entry
icat  -o 2048 image.E01 7 > boot.bin # extract VBR for hex review
istat -o 2048 image.E01 3            # $Volume: label, NTFS version, dirty flag
```
Key metadata entries: 0 `$MFT`, 1 `$MFTMirr` (copy of the first 4 MFT records), 2 `$LogFile`, 3 `$Volume`, 4 `$AttrDef`, 5 root dir, 6 `$Bitmap` (cluster allocation), 8 `$BadClus`, 9 `$Secure` (security descriptors `$SDS`), 10 `$UpCase`, 11 `$Extend` (`$UsnJrnl`, `$ObjId`, `$Quota`, `$Reparse`).

## Uses
- **Recovery**: corrupted primary VBR, tell TSK to use the backup (copy last sector to sector 0 of a working copy) or locate the MFT via `$MFTMirr`.
- **Attribution**: volume serial ties LNK files, prefetch and jump lists to a specific volume (e.g. a USB stick).
- **Format evidence**: `$MFT` and `$Boot` creation times reflect when the volume was formatted; a recent format on a drive claimed to be old is significant.
- **Hiding data**: `$BadClus:$Bad` marking good clusters bad, or slack in the boot area, can hide data; compare `$BadClus` size with SMART bad sector counts.
- **Bootkits**: VBR code (offset 0x54 onward) modified by bootkits; compare with a known-good VBR from the same Windows version.

## Gotchas
- Some tools trust `$MFTMirr` silently when `$MFT` is damaged; note which one was used.
- BitLocker volumes have a different OEM ID (`-FVE-FS-`) until decrypted.

## Verify
The VBR's MFT cluster x cluster size + partition offset points to a valid `FILE0` record, and the backup VBR matches or differences are explained.
