---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.group-types
name: group-types
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [group-types]
level: practitioner
status: draft
description: Choose between Microsoft 365 groups, security groups, distribution lists and mail-enabled security groups.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Group types and when to use each
**Goal:** Choose between Microsoft 365 groups, security groups, distribution lists and mail-enabled security groups.

- Microsoft 365 group: shared mailbox, calendar, SharePoint site, optional Team.
- Security group: access control to resources and licence assignment; not mail-enabled.
- Distribution list: email only, managed in Exchange.
- Mail-enabled security group: both mail and permissions, created in Exchange.
- Dynamic membership is available for Microsoft 365 and security groups through rules.

## Gotchas
- Converting types is limited; distribution lists can be upgraded to Microsoft 365 groups, but not the reverse.
- Guests added to Microsoft 365 groups gain access to the group's resources.

## Self-check
Create each type in a test tenant and verify which workloads each provisions.
