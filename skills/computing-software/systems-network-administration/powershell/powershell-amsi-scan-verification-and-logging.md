---
id: computing-software.systems-network-administration.powershell.powershell-amsi-scan-verification-and-logging
name: powershell-amsi-scan-verification-and-logging
category: computing-software
field: systems-network-administration
product: powershell
tags: [amsi, powershell-security, script-scanning, script-block-logging, defender]
level: practitioner
status: docs-checked
description: "Understand how AMSI feeds PowerShell script content to antivirus, what integrates with it, and how to verify it is active and keep it from being bypassed."
sources: ["https://learn.microsoft.com/en-us/windows/win32/amsi/antimalware-scan-interface-portal"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMSI and PowerShell

**Goal:** make sure script content is scanned, and that you can see detections.

## What it does
The Antimalware Scan Interface (AMSI) is a vendor-agnostic interface that lets applications and services integrate
with any antimalware product present on the machine. It supports file, memory and stream scanning and URL/IP
reputation checks, and has a session notion so fragments of a payload can be correlated.

Windows components that integrate with AMSI (Windows 10): User Account Control, PowerShell (scripts, interactive use
and dynamic code evaluation), Windows Script Host (wscript.exe, cscript.exe), JavaScript and VBScript, and Office VBA
macros.

## Check it is active
1. A real-time antimalware product that registers an AMSI provider is installed and enabled; for third-party AV,
   check the vendor documentation.
2. In Windows 10 version 1903 and later, an AMSI provider DLL that is not Authenticode-signed may not be loaded,
   depending on host configuration.
3. Do not rely on AMSI alone: it is one layer. Combine it with script logging and application control.

## Verify
In a lab, a benign vendor-documented test is detected by the registered provider and the detection appears in that
product's own console or log.

## Checked
2026-11-09. Read the Learn AMSI portal page in full. Confirmed: purpose, vendor-agnostic design, scanning types,
sessions, the list of integrating components and the 1903 signing note. Removed as not on the cited page: the
Get-MpComputerStatus check, Defender event IDs and log name, event 4104 and module logging details, the console
error wording, Windows PowerShell 2.0 statements, and tamper protection advice.
Method: documentation only; no commands were run.
