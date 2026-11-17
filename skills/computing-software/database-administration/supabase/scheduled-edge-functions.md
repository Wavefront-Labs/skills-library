---
id: computing-software.database-administration.supabase.scheduled-edge-functions
name: scheduled-edge-functions
category: computing-software
field: database-administration
product: supabase
tags: [edge-functions, pg-cron, pg-net, vault, schedule]
level: practitioner
status: docs-checked
description: "Schedule Supabase Edge Functions with pg_cron and pg_net, storing the project URL and secret key in Vault and avoiding the publishable key."
sources:
  - https://supabase.com/docs/guides/functions/schedule-functions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: invoke a function on a schedule from inside Postgres.

Requirements: the `pg_cron` and `pg_net` extensions, supported on the hosted platform.

Store credentials in Vault:

```sql
select vault.create_secret('https://project-ref.supabase.co', 'project_url');
select vault.create_secret('YOUR_SUPABASE_SECRET_KEY', 'secret_key');
```

Then schedule a `cron.schedule` job that calls `net.http_post(...)`. The page's example job is named `'invoke-function-every-minute'` with schedule `'* * * * *'` and a body such as `concat('{"time": "', now(), '"}')::jsonb`.

Rules:
- Call the function with the secret key, not the publishable key. The publishable key is public, so anyone holding it could call a function that accepts it.
- The function reads the key from the `apikey` header. To accept it, disable `verify_jwt` and set `auth: 'secret'`.
- Caution: any role that can log in can read the secret key while the request waits, because `pg_net` writes the decrypted key to `net.http_request_queue` until it sends.

The page gives no limits beyond its one-minute example schedule.

## Checked

Confirmed against the page and its pg_net partial: pg_cron plus pg_net, Vault storage of project URL and secret key, example job name and schedule, secret key rather than publishable key, apikey header with verify_jwt disabled and auth secret, and the net.http_request_queue warning. Nothing removed.

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/functions/schedule-functions and the _partials/pg_net_queued_key partial (apps/docs/content on GitHub master), read in full.
