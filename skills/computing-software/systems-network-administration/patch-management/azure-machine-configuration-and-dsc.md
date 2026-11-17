---
id: computing-software.systems-network-administration.patch-management.azure-machine-configuration-and-dsc
name: azure-machine-configuration-and-dsc
category: computing-software
field: systems-network-administration
product: patch-management
tags: [machine-configuration, dsc, azure-policy, guest-configuration, config-baselines, patch-management]
level: practitioner
status: docs-checked
description: "Enforce OS configuration baselines with Azure Machine Configuration and PowerShell DSC: built-in policies, custom packages, audit vs apply-and-autocorrect modes, Arc servers."
sources:
  - https://learn.microsoft.com/en-us/azure/governance/machine-configuration/overview
  - https://learn.microsoft.com/en-us/azure/governance/machine-configuration/how-to/develop-custom-package/overview
  - https://learn.microsoft.com/en-us/powershell/dsc/overview
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Azure Machine Configuration and DSC

Azure Policy's machine configuration feature audits or configures operating system settings as code on machines in Azure and on Azure Arc-enabled hybrid machines. It uses PowerShell Desired State Configuration (PSDSC) for both Windows and Linux, and can be used per machine or orchestrated at scale through Azure Policy.

## Enforcement modes (custom policies)
- **Audit**: only report the state of the machine.
- **Apply and Monitor**: apply the configuration, then monitor for changes (drift is reported).
- **Apply and Autocorrect**: apply, and bring the machine back into conformance when drift occurs.

## Built-in policies
Microsoft publishes built-in policy definitions and initiatives in the "Guest Configuration" category of Azure Policy. Assign them at management group or subscription scope and read results in Policy compliance. Check the overview page for the current list of supported operating systems before assigning.

## Custom packages
1. Write a DSC configuration that defines the condition the machine should be in.
2. Compile it to a MOF and build a package with the `GuestConfiguration` PowerShell module (it runs only on Ubuntu 18 or later on Linux, but the packages and policies it produces work on any Linux version supported in Azure or Arc).
3. Test the package locally, upload it to storage the machines can read, and create the policy definition from it. Follow the "develop custom package" how-to pages for the exact cmdlets and parameters; they change between module versions.
4. Packages that apply configuration (not just audit) need Azure VM guest configuration extension 1.26.24 or later, or Arc agent 1.10.0 or later.

## Gotchas
- Auto-correct fights other tools (GPO, Intune) that manage the same setting; pick one owner per setting.
- Package changes need a new package version and an updated policy; do not overwrite content under an existing assignment.

## Verify
Policy compliance shows Compliant for the assignment, and a drift introduced on a test VM is reported (Apply and Monitor) or corrected (Apply and Autocorrect).

## Checked
2026-11-01. Confirmed against the machine configuration overview and custom-package overview pages: the three enforcement modes, Azure and Arc scope, PSDSC for Windows and Linux, the module platform note, and the extension and Arc agent minimum versions. Removed because not found in the cited pages: the "formerly Guest Configuration" claim, specific built-in initiative names, managed-identity prerequisites, cmdlet examples and parameter values, the 5-minute check interval, and the classic DSC pull-server and Automation notes.
Method: documentation only; no commands were run.
