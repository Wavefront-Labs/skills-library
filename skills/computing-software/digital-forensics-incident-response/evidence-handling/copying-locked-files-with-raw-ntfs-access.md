---
id: computing-software.digital-forensics-incident-response.evidence-handling.copying-locked-files-with-raw-ntfs-access
name: copying-locked-files-with-raw-ntfs-access
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [locked-file-copy, live-response, triage-collection, ntfs, dfir]
level: practitioner
status: docs-checked
description: "Copy in-use Windows files (registry hives, $MFT, pagefile) on a live system with RawCopy's low-level NTFS reads, and why reg save is only a logical export."
sources: ["https://github.com/jschicht/RawCopy", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/reg-save"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copying locked files with raw NTFS access

**Goal:** many key artefacts are locked by the OS on a live system, so a normal copy fails. A raw-read tool gets the file from the volume without going through the locking file APIs.

## RawCopy
RawCopy is a console application that copies files off NTFS volumes using a low-level disk reading method. Its README says it can copy files the system has locked: registry hives like SYSTEM and SAM, files inside System Volume Information, pagefile.sys, or any file on the filesystem.
```text
RawCopy.exe /FileNamePath:<SYSTEM_DRIVE>\WINDOWS\system32\config\SYSTEM /OutputPath:<EVIDENCE_DRIVE>\output
RawCopy.exe /FileNamePath:<SYSTEM_DRIVE>\hiberfil.sys /OutputPath:<EVIDENCE_DRIVE>\output /OutputName:hiberfil_c.sys
RawCopy.exe /FileNamePath:C:0 /OutputName:MFT_C.bin
```
- `/FileNamePath:` is mandatory: a full path, or `Volume:MftRef` ($MFT record number). `C:0` is the $MFT in the README example.
- `/OutputPath:` and `/OutputName:` are optional; with no output path the file goes to the program directory.
- `/AllAttr:1` extracts all attributes. `/RawDirMode:1|2` prints a detailed or basic raw directory listing, which helps find a file's MFT reference.
- `/ImageFile:` with `/ImageVolume:` reads from a disk image instead of the live volume.
- Device paths such as HarddiskVolumeShadowCopy1 or PhysicalDrive1 can be given in `/FileNamePath:`.
- `/TcpSend:1` sends output over the network with `/OutputPath:` set to IP:PORT; the README says the data is sent as is, unencrypted, and something such as netcat must be listening.
- Write output to external or network storage, not the evidence volume (this is practitioner advice, not stated by the README).
- The README says this version is incompatible with Windows 2000 / NTFS 3.0.

## reg save
`reg save <keyname> <filename> [/y]` saves a copy of the specified registry subkeys, entries and values to a file; valid local root keys are HKLM, HKCU, HKCR, HKU and HKCC. It exports through the registry, so treat it as a logical copy: it is not a raw read of the hive file from the volume, and the page does not say it preserves transaction logs or slack.

## Verify
Hash every copied file and record the tool, version and exact command in the collection log.

## Checked
Confirmed against the RawCopy README (purpose, parameters, locked-file examples, TcpSend note, Windows 2000 note) and the Microsoft `reg save` page (syntax, root keys, `/y`). Removed claims neither page gives: KAPE and Velociraptor methods, FTK Imager and vssadmin steps, the "what to grab together" artefact list and log files, alternate data stream and AV/EDR remarks, and claims about reg save losing slack and transaction logs (reworded as "not documented").

Method: docs-only read of cited pages, 2026-11-09
