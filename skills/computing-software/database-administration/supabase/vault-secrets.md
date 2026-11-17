---
id: computing-software.database-administration.supabase.vault-secrets
name: vault-secrets
category: computing-software
field: database-administration
product: supabase
tags: [vault, secrets, decrypted-secrets, encryption, pgsodium]
level: practitioner
status: docs-checked
description: "Store encrypted secrets in Supabase Vault: create, read, update, delete SQL, access control, and root key behaviour across restores and branches."
sources:
  - https://supabase.com/docs/guides/database/vault
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep secrets encrypted in Postgres and read them only where needed.

```sql
select vault.create_secret('my_s3kre3t');
select vault.create_secret('another_s3kre3t', 'unique_name', 'This is the description');

select * from vault.decrypted_secrets order by created_at desc limit 3;

select vault.update_secret('7095d222-efe5-4cd5-b5c6-5755b451e223', 'n3w_upd@ted_s3kret',
  'updated_unique_name', 'This is the updated description');

delete from vault.secrets where id = '7095d222-efe5-4cd5-b5c6-5755b451e223' returning id, name;
```

Behaviour:
- Secrets are stored encrypted in `vault.secrets`; the `vault.decrypted_secrets` view shows them decrypted at query time.
- `vault.create_secret()` returns the new secret's UUID. Names are optional but must be unique when set.
- Deleting from `vault.secrets` also removes the row from the view.

Access: anyone who can query `vault.decrypted_secrets` can read secrets, so restrict it with SQL privileges. Consider access to `vault.secrets` carefully.

Root key: each project has its own root encryption key. Pausing and restoring, PITR and in-place restores keep it. Restore-to-new-project and Branching copy it. A manual `pg_dump`/`pg_restore` into a new project creates a fresh key, so copied secrets cannot be decrypted until the old root key is copied over, using the Management API endpoint `https://api.supabase.com/v1/projects/$REF/pgsodium` (GET from the old project, PUT to the new one, with `Authorization: Bearer $SUPABASE_ACCESS_TOKEN`). That endpoint works only for active projects.

## Checked

Confirmed against the page: vault.create_secret (optional unique name and description), vault.decrypted_secrets view, vault.update_secret, delete from vault.secrets, access-control warning, per-project root key behaviour across pause, restore, PITR, restore to new project and Branching, manual pg_dump needing the root key copied via the pgsodium Management API endpoint (active projects only). Nothing removed.

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/database/vault (apps/docs/content on GitHub master), read in full.
