---
id: computing-software.it-support-helpdesk.intune-mdm.proactive-remediations-and-scripting
name: proactive-remediations-and-scripting
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, proactive-remediations, remediations, powershell, run-as-user, detection-script, remediation-script, exit-codes, intune-management-extension, script-signing, logged-on-user]
level: practitioner
status: docs-checked
description: "Deploy and debug Intune Remediations (formerly Proactive Remediations): detection exit 1 contract, script requirements, schedules, on-demand runs and reporting cadence."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/fundamentals/remediations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# proactive-remediations-and-scripting

Proactive Remediations was renamed **Remediations**; find it at Devices > Manage devices > Scripts and remediations. A script package is a detection script, an optional remediation script, and metadata. The IME fetches and runs the scripts.

## Prerequisites
- Devices Entra joined or hybrid joined, and either MDM enrolled in Intune running Windows Enterprise, Professional or Education, or co-managed Windows.
- Users licensed with Windows Enterprise E3/E5 (Microsoft 365 F3, E3, E5), Windows Education A3/A5, or Windows VDA per user. An Intune Service Administrator confirms licensing before first use.
- Permissions come from the Device configurations category of the user's role.

## Detection and remediation contract
- The remediation runs only if the detection script exits with **exit 1** (issue detected). Any other exit code, including empty output, means no issue found, so the remediation does not run. (Not "any non-zero.")
- A package can hold a detection script only. Detection and its remediation must be in the same package.
- Up to 200 script packages. Maximum output 2,048 characters. Scripts must be UTF-8; with Enforce script signature check on, UTF-8 without BOM.
- With signature check on, scripts follow the device PowerShell execution policy (default Restricted on Windows client, RemoteSigned on Server) and non-Microsoft signing certificates must be in Trusted Publishers. Without it, scripts run with the Bypass execution policy.
- No reboot commands, no sensitive or personal data in scripts.
- Microsoft's recommended settings for the package: Run this script using the logged-on credentials depends on the script; Enforce script signature check No; Run script in 64-bit PowerShell No.
- Do not mix user and device groups across include and exclude assignments.

## Schedule
Once (date and time), Hourly (every n hours, n under 24) or Daily. Runs use device local time unless Use UTC is selected. A missed run executes as soon as the device is online. Use less frequent schedules (for example every seven days) for heavy scripts, avoid values that change every run such as timestamps. Scripts rerun every 24 hours per the custom package guidance.

## On-demand run (preview)
Devices > By platform > Windows > the device > ... > Run remediation (preview). Needs Run remediation permission (Remote tasks) and Organization: Read during preview, an online device that can reach Intune and WNS, and the IME installed. Only one run at a time per device or they can overwrite each other.

## Policy retrieval and reporting
The client retrieves Remediation policy after a restart of the device or IME service, after a user signs in, and every 8 hours (fixed from when the IME starts). Run-once scripts report after running. Recurring scripts report on change within the first six days (the first run counts), and every seven days regardless.

## Monitor
Scripts and remediations > the package > Device status; per device: the device > Monitor > Remediations. Export gives a CSV, but only for script packages loaded in the list so far.

## Checked
Date: 2026-11-08. Read in full: Microsoft Learn "Remediations" (updated 2026-04-16). Corrections: detection must exit 1 (previously "any non-zero"); 64-bit PowerShell is not the default per the recommended settings; schedule options are Once, Hourly and Daily. Removed as unconfirmed: platform scripts behaviour and menu path, the SYSTEM context and HKCU explanation, Write-Host surfacing in reports, "Run script immediately" wording, the IME log GUID tip, PowerShell 5.1 statements, PsExec testing, and the Gotchas and Verify sections.
Method: documentation only; no commands were run.
