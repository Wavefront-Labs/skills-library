---
id: computing-software.systems-network-administration.windows-server.dynamic-access-control-central-access-policies
name: dynamic-access-control-central-access-policies
category: computing-software
field: systems-network-administration
product: windows-server
tags: [file-server, dynamic-access-control, central-access-policy, claims, kerberos-armoring]
level: advanced
status: docs-checked
description: "Deploy Dynamic Access Control: claim types, resource properties, central access rules and policies pushed by GPO, and staging before enforcement."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/solution-guides/deploy-a-central-access-policy--demonstration-steps-
  - https://learn.microsoft.com/en-us/windows-server/identity/solution-guides/dynamic-access-control-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic Access Control and central access policies

DAC grants file access with expressions over user/device claims and file properties ("Department equals Finance
AND file Confidentiality is High") instead of thousands of groups.

## Prerequisites
- KDC support for claims and compound authentication: GPO on DCs, KDC > **KDC support for claims, compound
  authentication and Kerberos armoring** = Supported.

## Build the pieces (ADAC > Dynamic Access Control)
```powershell
New-ADClaimType -DisplayName Department -SourceAttribute department -SuggestedValues @(
  New-Object Microsoft.ActiveDirectory.Management.ADSuggestedValueEntry('Finance','Finance','')
  New-Object Microsoft.ActiveDirectory.Management.ADSuggestedValueEntry('HR','HR',''))
Set-ADResourceProperty Department_MS -Enabled $true        # built-in resource property
New-ADCentralAccessRule -Name 'Finance Docs' -ResourceCondition '(@RESOURCE.Department_MS Any_of {"Finance"})' `
  -CurrentAcl $currentAcl     # build the conditional ACL as in the demonstration steps
New-ADCentralAccessPolicy -Name 'Finance Policy'
Add-ADCentralAccessPolicyMember 'Finance Policy' -Members 'Finance Docs'
```

## Publish and apply
Deploy the central access policy to file servers through Group Policy, apply it to the folder, and classify files; see the demonstration steps page for the full procedure.

## Stage first
Use **Proposed permissions** (staging) and review the Central Access Policy Staging audit events (event **4818**) to see who would lose or gain access before switching to current permissions.

## Effective access
The Effective Access tab shows the effective results of the new policy.

## Verify
- [ ] Finance user reads, others denied; 4818 staging events reviewed before enforcement.

## Checked
2026-10-28: Confirmed on Learn pages deploy-a-central-access-policy--demonstration-steps- and dynamic-access-control-overview: KDC support for claims/compound authentication, New-ADClaimType, Set-ADResourceProperty Department_MS -Enabled, New-ADCentralAccessRule -CurrentAcl -ResourceCondition, New-ADCentralAccessPolicy and Add-ADCentralAccessPolicyMember, proposed permissions, event 4818 under Central Access Policy Staging, Effective Access tab. Removed: OS version requirements, SDDL string, GPO and folder UI paths, classification detail, share AND NTFS statement.
Method: documentation only; no commands were run.
