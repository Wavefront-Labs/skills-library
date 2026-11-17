---
id: computing-software.it-support-helpdesk.device-provisioning.build-qa-checklist-and-sign-off
name: build-qa-checklist-and-sign-off
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, standard-build, build-qa, provisioning-checklist, handover-checklist, compliance-check, autopilot-verification, pester]
level: practitioner
status: draft
description: "Quality-check a newly built device before handover: an automated build check script, compliance and encryption status, apps and updates, user-facing tests, and sign-off records."
sources:
  - "https://learn.microsoft.com/en-us/intune/intune-service/protect/device-compliance-get-started"
  - "https://learn.microsoft.com/en-us/windows/deployment/windows-autopilot/"
  - "https://pester.dev/docs/quick-start"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# build-qa-checklist-and-sign-off

Goal: no device reaches a user with a missing app, unencrypted disk or
failed policy — caught at the bench, not on the user's first morning.

## Automate the checks
A script run at the end of provisioning (or by the tech) beats a paper
checklist. Example checks:
```powershell
$r = [ordered]@{}
$r.BitLocker   = (Get-BitLockerVolume -MountPoint $env:SystemDrive).ProtectionStatus -eq 'On'
$r.EntraJoined = (dsregcmd /status | Select-String 'AzureAdJoined : YES') -ne $null
$r.DefenderOn  = (Get-MpComputerStatus).RealTimeProtectionEnabled
$r.TPMReady    = (Get-Tpm).TpmReady
$r.FreeGB      = [math]::Round((Get-PSDrive C).Free/1GB) -gt 30
$r.PendingReboot = -not (Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending')
foreach ($app in 'Microsoft Teams','Company Portal','Zscaler') {
  $r["App: $app"] = [bool](Get-CimInstance Win32_InstalledWin32Program | Where Name -like "*$app*") -or
                    [bool](Get-AppxPackage -AllUsers | Where Name -like "*$($app -replace ' ','')*")
}
$r.GetEnumerator() | Format-Table -AutoSize
```
Pester tests are a tidy way to keep this as a maintained test suite.

## Portal-side checks
- Intune device: **Compliant**, primary user correct, all required apps
  "Installed", configuration profiles "Succeeded" (no Error/Conflict).
- Correct device group / Autopilot group tag, naming convention, asset tag
  recorded against serial in CMDB.
- Latest quality update installed (`winver` build vs current).

## Hands-on checks (5 minutes)
Sign in as a test or the target user (if pre-provisioned): Wi-Fi joins
corporate SSID, VPN connects, printer reachable, OneDrive KFM active,
Teams camera/mic, docking station and displays, keyboard layout and
language, battery report sane.

## Sign-off
Record in the ticket/RITM: device serial, build version, script output
(attach), tech name, date. Failed check → fix and rerun, don't hand over
"mostly done".

## Gotchas
- Pre-provisioned (white glove) devices: user-targeted apps/policies aren't
  there until the user signs in — check those at handover.
- Compliance can show "Not evaluated" for up to hours after enrolment —
  trigger a sync and wait, don't skip.

## Verify
Every device handed over has an attached QA output with all checks true,
and first-week tickets per new device trend down.
