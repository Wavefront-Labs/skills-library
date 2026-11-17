---
id: computing-software.cloud-infrastructure-engineering.azure.entra-bulk-user-create-invite-and-delete
name: entra-bulk-user-create-invite-and-delete
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, bulk-operations, bulk-create-users, csv]
level: practitioner
status: docs-checked
description: "Bulk create Entra ID member accounts from the CSV template: required columns, template rules, validation, results file, verification and the one-hour batch caveat."
sources: ["https://learn.microsoft.com/en-us/entra/identity/users/users-bulk-add"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra bulk user create

**Goal:** create many internal member accounts in one operation. The cited page also says Entra supports bulk delete and downloading user lists; see the linked bulk delete, download and bulk restore pages for those, and Bulk invite B2B users for guests.

## Steps
Sign in to the Entra admin center as at least a User Administrator, then Entra ID > Users > **Bulk create**.
1. Select Download for the CSV template.
2. Fill one user per row. Keep the column headings exactly as downloaded (and the version row if present). The required columns are `Name [displayName] Required`, `User name [userPrincipalName] Required` and `Initial password [passwordProfile] Required`; all others are optional. The examples row may stay.
3. Upload the file and select Submit; validation runs. If there are errors, fix them before the job can be submitted. Once it passes, Submit starts the import and a notification shows job status.

## Template rules
- Add the .csv extension and remove any leading spaces before userPrincipalName and passwordProfile.
- Columns you add are ignored and not processed; Microsoft does not recommend adding any. Download the latest template often.
- No unintended whitespace around fields; in User principal name it causes import failure.
- Initial passwords must comply with the active password policy.

## Gotchas
- The operation creates internal members with the passwords in the CSV. No invitation emails are sent, so deliver credentials through your own process.
- Errors: download the results file from the Bulk operation results page; it gives the reason per error. The submission must match the template with exact column names.
- A bulk operation that does not finish within the hour can fail. Microsoft recommends splitting records per batch, for example by filtering an export by group type or user name.

## Verify
Entra ID > Users > All users with Show = All users, or `Get-MgUser -Filter "UserType eq 'Member'"`. Pending jobs appear on the Bulk operation results page.

## Checked
Confirmed against "Bulk create users in Microsoft Entra ID" (last updated 2026-10-01 on the page), 2026-11-08. Removed: invite and delete column details, role advice for guest invites, the New-MgUser/New-MgInvitation script, temporary access pass advice, recycle bin retention and the maximum-rows caveat, which the page does not cover.
Method: docs-only read of cited pages, 2026-11-08
