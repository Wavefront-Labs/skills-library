---
id: computing-software.collaboration-platform-administration.tenant-migration.cross-tenant-mailbox-migration
name: cross-tenant-mailbox-migration
category: computing-software
field: collaboration-platform-administration
product: tenant-migration
tags: [cross-tenant-mailbox-migration, mig-tenant-to-tenant]
level: advanced
status: draft
description: Move mailboxes between Microsoft 365 tenants with MRS.
sources: ['https://learn.microsoft.com/en-us/exchange/mailbox-migration/mailbox-migration', 'https://learn.microsoft.com/en-us/sharepointmigration/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cross-tenant mailbox migration
**Goal:** Move mailboxes between Microsoft 365 tenants with MRS.

- Create an Entra app and organisation relationship in both tenants; `New-MigrationEndpoint -RemoteServer outlook.office.com -RemoteTenant <tenant> -ApplicationId <id> -AppSecretKeyVaultUrl <url>`.
- Target needs a MailUser with matching ExchangeGuid and ArchiveGuid, LegacyExchangeDN as x500.
- Create batch with `New-MigrationBatch -SourceEndpoint ... -TargetDeliveryDomain <tenant>.mail.onmicrosoft.com`.
- Retain source until validation completes.

## Gotchas
- Matching GUIDs are critical; mismatches fail the move.
- Use the product documentation's current prerequisites (they change).

## Self-check
Move statistics show Completed and Outlook connects after profile update.
