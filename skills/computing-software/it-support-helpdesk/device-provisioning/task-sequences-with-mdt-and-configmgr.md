---
id: computing-software.it-support-helpdesk.device-provisioning.task-sequences-with-mdt-and-configmgr
name: task-sequences-with-mdt-and-configmgr
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, task-sequence, configmgr, mdt, osd, smsts-log, operating-system-deployment]
level: practitioner
status: draft
description: "Build and debug OS deployment task sequences in ConfigMgr (and legacy MDT): core step order, key variables, F8 debugging, smsts.log locations and common error codes."
sources:
  - "https://learn.microsoft.com/en-us/mem/configmgr/osd/deploy-use/manage-task-sequences-to-automate-tasks"
  - "https://learn.microsoft.com/en-us/mem/configmgr/osd/understand/task-sequence-variables"
  - "https://learn.microsoft.com/en-us/mem/configmgr/core/plan-design/hierarchy/log-files#operating-system-deployment-and-image-capture"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# task-sequences-with-mdt-and-configmgr

## Core step order (bare metal)
1. Restart in Windows PE (if started from the OS) / boot media.
2. Format and Partition Disk (UEFI/GPT layout).
3. Apply Operating System (image or upgrade package).
4. Apply Windows Settings and Apply Network Settings (workgroup or domain join account).
5. Apply Driver Package (per model, with a WMI condition) or Auto Apply Drivers.
6. Setup Windows and ConfigMgr (installs the client, then reboots into the full OS).
7. Install Applications, Install Software Updates, enable BitLocker, custom scripts.

MDT task sequences follow the same shape; MDT is no longer developed, so new builds
belong in ConfigMgr or Autopilot.

## Variables you will touch
`OSDComputerName` (name, often from a prompt or collection variable), `_SMSTSMachineName`,
`OSDJoinDomainName`/`OSDDomainOUName`, `SMSTSErrorDialogTimeout`, and custom variables
for conditions. Read-only ones start with `_SMSTS`.

## Debugging
- Enable command support on the boot image; press `F8` in WinPE for a command prompt and
  open logs with CMTrace while the sequence runs.
- `smsts.log` moves during the build: in WinPE on the RAM drive under `Windows\Temp\SMSTSLog`,
  then on the OS disk under `_SMSTaskSequence\Logs`, and finally `%WINDIR%\CCM\Logs\SMSTSLog`
  (or `%WINDIR%\CCM\Logs` after completion).
- Find the last "Failed to run the action" line and read upwards.

## Common errors
| Code | Usual cause |
|---|---|
| 0x80070002 / 0x80070003 | Content or file path not found; package not distributed to the DP |
| 0x80004005 | Generic; read the lines above it |
| 0x87D00269 / no network in WinPE | NIC driver missing from the boot image |
| 0x80070057 | Disk/partition parameter issue; often missing storage driver (Intel RST/VMD) |
| App install hangs | Installer waiting for user input; needs silent switches |

## Gotchas
- Applications must allow install during a task sequence ("Allow this application to be
  installed from the Install Application task sequence action").
- Domain join account needs rights on the target OU only; credentials expire silently.

## Verify
A test device completes end to end with no error dialog, the computer is named and joined
correctly, and smsts.log ends with a successful completion.
