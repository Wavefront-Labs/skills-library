---
id: computing-software.systems-network-administration.patch-management.microsoft-security-baselines
name: microsoft-security-baselines
category: computing-software
field: systems-network-administration
product: patch-management
tags: [security-baseline, policy-analyzer, security-compliance-toolkit, lgpo, intune-security-baselines, group-policy, config-baselines]
level: practitioner
status: docs-checked
description: "Apply Microsoft security baselines from the Security Compliance Toolkit: import GPO backups, compare with Policy Analyzer, LGPO for standalone hosts, and Intune baselines."
sources:
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/security-compliance-toolkit-10
  - https://learn.microsoft.com/en-us/mem/intune/protect/security-baselines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft security baselines

**Goal:** start from Microsoft's recommended security settings for each Windows, Windows Server, Edge and Microsoft 365 Apps release.

## Get the baseline
Download from the Security Compliance Toolkit: the toolkit provides the baselines plus the tools Policy Analyzer, LGPO, Set Object Security and GPO to Policy Rules (GPO2PolicyRules converts GPO backups to Policy Analyzer `.PolicyRules` files). Baseline packages carry GPO backups and documentation; check each download for its contents.

## Compare before applying
Policy Analyzer compares the baseline with your existing GPOs and the local effective policy:
1. Load the baseline rules and your current GPOs (or local policy) into Policy Analyzer.
2. Compare to find duplicated or conflicting settings; export the result to Excel for review.
Use it again when a new baseline ships to see exactly what changed.

## Apply in a domain
```powershell
Import-GPO -BackupGpoName 'MSFT Windows Server 2022 - Member Server' -Path .\GPOs -TargetName 'SEC-Baseline-WS2022-Member' -CreateIfNeeded
New-GPLink -Name 'SEC-Baseline-WS2022-Member' -Target 'OU=Servers,DC=corp,DC=example' -LinkEnabled No
```
Link to a pilot OU first; keep your own deviations in a separate higher-precedence GPO, never edit the imported baseline GPO (so updates can be swapped cleanly).

## Standalone or workgroup hosts
`LGPO.exe` is a command-line tool for managing local group policy on non-domain-joined systems: it imports settings from Registry.pol files, security templates, advanced audit backup files and LGPO text files, and exports local policy. See its documentation for the switches; back up local policy before applying.

## Intune
Endpoint security > Security baselines in the Intune admin center lists baselines including Windows, Microsoft Defender for Endpoint, Microsoft Edge and Microsoft 365 Apps for Enterprise. Create a profile, customise, assign to pilot then broad groups; new baseline versions are handled as described on the Intune security baselines page.

## Gotchas
- Baselines can break legacy protocols (NTLMv1, SMB signing requirements, old TLS); test line-of-business apps.
- Don't layer CIS and Microsoft baselines blindly; resolve conflicts deliberately.

## Verify
Policy Analyzer against the local policy of a pilot machine shows no differences from baseline plus documented deviations.

## Checked
Date: 2026-10-27. Documentation: Microsoft Learn Security Compliance Toolkit page (Policy Analyzer, LGPO, Set Object Security, GPO to Policy Rules), Import-GPO and New-GPLink cmdlet references (parameters -BackupGpoName, -Path, -TargetName, -CreateIfNeeded, -Target, -LinkEnabled), Intune security baselines page (Endpoint security > Security baselines; Windows, Defender for Endpoint, Edge, Microsoft 365 Apps baselines). Removed the unconfirmed LGPO /g and /b switches and Policy Analyzer menu names.
Method: documentation only; no commands were run.
