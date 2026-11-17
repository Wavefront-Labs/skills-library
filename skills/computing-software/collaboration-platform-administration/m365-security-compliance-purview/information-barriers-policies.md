---
id: computing-software.collaboration-platform-administration.m365-security-compliance-purview.information-barriers-policies
name: information-barriers-policies
category: computing-software
field: collaboration-platform-administration
product: m365-security-compliance-purview
tags: [information-barriers-policies, pv-information-barriers]
level: advanced
status: draft
description: Segment users to block communication where regulations require.
sources: ['https://learn.microsoft.com/en-us/purview/', 'https://learn.microsoft.com/en-us/defender-office-365/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Information barriers
**Goal:** Segment users to block communication where regulations require.

- Define segments with user attributes (Department, etc.) in PowerShell: `New-OrganizationSegment -Name HR -UserGroupFilter "Department -eq 'HR'"`.
- Create IB policies `New-InformationBarrierPolicy -Name ... -AssignedSegment HR -SegmentsBlocked Sales -State Inactive`.
- Apply with `Start-InformationBarrierPoliciesApplication`.
- Covers Teams, SharePoint, OneDrive (confirm current scope).

## Gotchas
- Policies need an order of operations and propagate over hours.
- Segments cannot overlap in one user's attributes in a conflicting way.

## Self-check
Policy application status shows Completed and a blocked chat is denied.
