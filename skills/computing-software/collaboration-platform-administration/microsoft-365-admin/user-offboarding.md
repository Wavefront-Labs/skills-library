---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.user-offboarding
name: user-offboarding
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [user-offboarding]
level: practitioner
status: draft
description: Remove a departed user safely while retaining mail and files.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Offboard a leaver
**Goal:** Remove a departed user safely while retaining mail and files.

- Block sign-in and revoke sessions (`Revoke-MgUserSignInSession`).
- Convert the mailbox to shared if it must be retained (`Set-Mailbox -Identity <upn> -Type Shared`, under 50 GB without a licence).
- Transfer OneDrive access to the manager (OneDrive retention for deleted users defaults to 30 days, configurable).
- Remove licences after conversion and holds are in place; reassign ownership of groups and Teams.
- Delete the user; recover within 30 days from Deleted users.

## Gotchas
- Removing the licence before conversion or hold can start deletion of the mailbox.
- Shared mailboxes over 50 GB or with archive need a licence.

## Self-check
The mailbox is accessible by the manager and the user shows in Deleted users after deletion.
