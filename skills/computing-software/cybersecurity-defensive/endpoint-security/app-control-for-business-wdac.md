---
id: computing-software.cybersecurity-defensive.endpoint-security.app-control-for-business-wdac
name: app-control-for-business-wdac
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [application-control, wdac, app-control-for-business, code-integrity-policy, managed-installer, isg, wdac-wizard, audit-mode, supplemental-policies]
level: advanced
status: docs-checked
description: "Deploy App Control for Business (WDAC): base policy from a template, managed installer and ISG, audit then enforce, supplemental policies and event-driven tuning."
sources: ["https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/select-types-of-rules-to-create", "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/operations/event-id-explanations", "https://learn.microsoft.com/en-us/powershell/module/configci/convertfrom-cipolicy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Control for Business (WDAC)

**Goal:** only trusted code runs on Windows endpoints and servers, enforced in the kernel,
stopping most malware and unauthorised tools.

## Plan the policy
- Start from a Microsoft template (`DefaultWindows_Audit.xml` or `AllowMicrosoft.xml`) in the **App Control Policy Wizard**.
- Trust sources:
  - **Managed installer**: anything installed by Intune Management Extension / Configuration Manager is trusted automatically.
  - **Intelligent Security Graph (ISG)**: trust files with good Microsoft reputation (convenient; less strict).
  - Publisher/signer rules for line-of-business vendors; hash rules as last resort.
- Rule options: enable `Audit Mode` first, `Enabled:Update Policy No Reboot`, `Enabled:Unsigned System Integrity Policy` only for testing; consider `Required:Enforce Store Applications`, script enforcement, and the Microsoft recommended block rules (LOLBins and vulnerable drivers).

## Deploy
1. Convert XML to binary: `ConvertFrom-CIPolicy -XmlFilePath policy.xml -BinaryFilePath {PolicyId}.cip`.
2. Deploy via Intune (App Control for Business profile or custom OMA-URI), Configuration Manager, or GPO for single-policy format.
3. **Audit mode** on a pilot ring for a full business cycle; collect `Microsoft-Windows-CodeIntegrity/Operational` events **3076** (would block) and `AppLocker/MSI and Script` **8028**.
4. Build supplemental policies from audit events (`New-CIPolicy -Audit` or Defender for Endpoint advanced hunting).
5. Switch to enforce (events **3077** for blocks), ring by ring.

## Operations
- Multiple-policy format (Windows 10 1903+): base plus supplemental policies per department.
- Exceptions process with fast turnaround; developers and IT admin machines in separate policies.
- Sign policies for tamper resistance once mature (signed policies cannot be removed without the signed removal policy).

## Gotchas
- Kernel drivers blocked by policy can make machines unbootable: test driver rules on representative hardware.
- ISG trust changes over time; a file trusted today may not be tomorrow.
- Scripts: PowerShell runs in Constrained Language Mode for untrusted scripts under enforcement, which breaks some admin scripts - sign them.

## Checked
2026-10-28. Confirmed in the App Control rule options, event ID and ConvertFrom-CIPolicy pages: `DefaultWindows_*` and `AllowMicrosoft.xml` templates, rule options `Enabled:Update Policy No Reboot` and `Required:Enforce Store Applications`, events 3076/3077, event 8028 in the AppLocker MSI and Script log, `New-CIPolicy -Audit`. Removed: the advanced hunting query and the 2-4 week figure.
Method: documentation only; no commands were run.

## Verify
- [ ] Audit events reviewed until block-would-be events are only unwanted software.
- [ ] Enforced ring: an unsigned test executable from Downloads is blocked (event 3077).
