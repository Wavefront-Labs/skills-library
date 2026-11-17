---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.policy-assignment
name: policy-assignment
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [policy-assignment, tso-teams-policies]
level: practitioner
status: draft
description: Assign Teams policies directly, by group, or as policy packages.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Assign policies to users and groups
**Goal:** Assign Teams policies directly, by group, or as policy packages.

- Teams admin center > Users or Teams > Policy packages.
- PowerShell: `Grant-CsTeamsMeetingPolicy -Identity user@contoso.com -PolicyName Exec`; `New-CsGroupPolicyAssignment -GroupId <id> -PolicyType TeamsMeetingPolicy -PolicyName Exec -Rank 1`.
- Precedence: direct user assignment beats group assignment; group rank decides among groups.
- Policy changes can take up to 24 hours to apply (often much faster).

## Gotchas
- Group assignment supports a limited set of policy types; check the list.
- Global (Org-wide default) policy applies when nothing else does.

## Self-check
`Get-CsUserPolicyAssignment -Identity <upn>` shows effective policy and source.
