---
id: computing-software.systems-network-administration.backup-and-recovery.recovery-media-creation-and-testing
name: recovery-media-creation-and-testing
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [recovery-media, bare-metal-recovery, boot-media, winpe, dr-readiness]
level: practitioner
status: docs-checked
description: "Create and test recovery boot media for bare-metal restores: WinPE and Veeam Recovery Media basics, what the media must contain, storage and test routine."
sources:
  - https://helpcenter.veeam.com/docs/agentforwindows/userguide/image_create.html
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/winpe-intro
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovery media creation and testing

**Goal:** when a server is dead, you can boot something that reaches the backups and restores it, on the hardware you actually have.

## What the vendor pages state
- **Veeam Recovery Media** (Veeam Agent for Microsoft Windows) contains everything needed to run Microsoft Windows RE. If the computer stops working or the disk fails, boot from it instead of the hard drive, then use Veeam and Microsoft tools to fix errors and recover the system image and data. Check the prerequisites first, then create it with the Create Recovery Media wizard or the command line interface. You can predefine restore settings to automate restores, and a registry value can disable the "Press any key to boot..." prompt (see the Veeam KB article it links).
- **Windows PE (WinPE)** is a small operating system for installing, deploying and repairing Windows. It is an add-on to the Windows ADK (before Windows 10 version 1809 it was included in the ADK). It can boot from USB, CD/DVD/ISO or a virtual hard drive. It includes a generic set of drivers for networking, graphics and mass storage, supports DISM, and has optional support for BitLocker, TPM and Secure Boot. The base version needs 512 MB of memory (more if you add drivers, packages or apps). All changes are lost on reboot, so make lasting changes in the image itself (see "WinPE: Mount and Customize").

## What your media must do (design checklist)
- Boot on the target hardware and on VMs; include any drivers the generic set lacks.
- Reach the backup repository, or read local media.
- Match the version of the restore tool to the backups.

## Store and maintain
- Keep copies off the infrastructure being recovered, labelled with tool version and creation date.
- Recreate media after backup software upgrades or hardware changes, so it can read current backups.

## Test
1. Boot target hardware, or a matching VM, from the media.
2. Confirm disks and network are detected and the repository is reachable.
3. Perform a restore to a spare machine or VM.

## Verify
A dated test log per hardware family shows media version and result.

## Checked

2026-11-09. Confirmed against the Veeam "Creating Veeam Recovery Media" page and the Microsoft WinPE introduction (media types, ADK add-on, included drivers and features, memory, changes lost on reboot). Partial read: the Veeam page is an overview and the prerequisites were not read. The Relax-and-Recover documentation page is only an index of release notes and was dropped as a source. Removed: `dism /Add-Driver` instruction, `rear mkrescue`, Acronis and Commvault claims, PXE, Secure Boot signed-kernel gotcha, annual and quarterly test cadences and domain-credential advice (not on cited pages).

Method: documentation only; no commands were run.
