---
id: computing-software.systems-network-administration.active-directory.offline-domain-join-djoin
name: offline-domain-join-djoin
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, domain-join, djoin, offline-domain-join, odj, provisioning-blob, unattend, requestodj, rootcacerts, directaccess]
level: practitioner
status: docs-checked
description: "Join machines with no DC line of sight using djoin: /provision on a domain member, /requestODJ on the target or via unattend, and secure handling of the blob."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/dd392267(v=ws.10)
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Offline domain join (djoin)

**Use when:** the machine cannot reach a DC at join time (staging network, image build, mass VM deployment).
Offline join removes the extra restart an online join needs when you inject the blob into an offline image.

## 1. Provision on a domain-connected machine
```cmd
djoin /provision /domain ad.example.com /machine BR02-WS15 ^
  /machineou "OU=Workstations,OU=Branch02,DC=ad,DC=example,DC=com" /savefile BR02-WS15.txt
```
Options: `/reuse` to reuse an existing account (its password is reset; `/machineou` is ignored with it), `/dcname` to
target a specific DC, `/rootcacerts`, `/certtemplate`, `/policynames` and `/policypaths` to provide DirectAccess
policies and certificates (documented as Windows Server 2012 parameters). You need the rights to join workstations to
the domain (Domain Admins have them); for a non-admin, delegate Create child on the target OU and pass `/machineou`.

The blob contains the machine account password and domain information. Treat it like a plaintext password:
transfer it securely and delete it after use.

## 2. Apply on the target (as local admin)
```cmd
djoin /requestODJ /loadfile BR02-WS15.txt /windowspath %SystemRoot% /localos
shutdown /r /t 0
```
Because `/localos` injects the blob into the running OS, restart the computer to complete the join (as for an online
join). You cannot run `/localos` on a domain controller.

For an offline image, `/windowspath` points at the image's Windows directory (no `/localos`).

## Unattend
In `unattend.xml`, the `Microsoft-Windows-UnattendedJoin` component takes the base64 blob under `Identification` >
`Provisioning` > `AccountData`. Start the computer in Windows PE or Safe Mode and run setup with the answer file, as
the reference describes.

## Gotchas
- The computer account is created at provisioning time; if the device never arrives, delete it.
- With a read-only DC as the target, the PRP must allow the machine's secrets to be cached and replicated.

## Verify
- [ ] After reboot, `(Get-CimInstance Win32_ComputerSystem).Domain` shows the domain.
- [ ] Once connected, `Test-ComputerSecureChannel` returns True.

## Checked

Date: 2026-10-27. Documentation: djoin reference and offline domain join step-by-step guide (Windows Server 2008 R2
archive page; no current-release page was readable).
Confirmed: `/provision`, `/requestODJ`, `/machineou`, `/dcname`, `/reuse`, `/rootcacerts`, `/certtemplate`,
`/policynames`, `/policypaths`, `/savefile`, `/loadfile`, `/windowspath`, `/localos` semantics, the restart requirement,
the unattend structure, rights needed, blob sensitivity, and the no-`/localos`-on-DC rule.
Removed unconfirmed claims: "GPOs apply only once the machine contacts a DC" and the blob-name versus machine-name
statement. The verify steps use `Win32_ComputerSystem.Domain` and `Test-ComputerSecureChannel`, both confirmed on
their reference pages.

Method: documentation only; no commands were run.
