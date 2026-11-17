---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.user-create-bulk
name: user-create-bulk
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [user-create-bulk, m365-users-licensing]
level: practitioner
status: draft
description: Create Microsoft 365 users via the admin center, CSV bulk add, or Microsoft Graph PowerShell.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Create users singly and in bulk
**Goal:** Create Microsoft 365 users via the admin center, CSV bulk add, or Microsoft Graph PowerShell.

- Admin center > Users > Active users > Add a user; or Add multiple users with the CSV template.
- PowerShell: `Connect-MgGraph -Scopes User.ReadWrite.All`, then `New-MgUser -DisplayName ... -UserPrincipalName ... -MailNickname ... -AccountEnabled -PasswordProfile @{Password='...';ForceChangePasswordNextSignIn=$true}`.
- Set UsageLocation before assigning licences.
- Hybrid-synced users are managed on-premises; do not create cloud duplicates.

## Gotchas
- Missing UsageLocation causes licence assignment to fail.
- Never log or email initial passwords in clear; use a temporary access pass or secure handover.

## Self-check
`Get-MgUser -UserId <upn> | Select AccountEnabled,UsageLocation` and a test sign-in.
