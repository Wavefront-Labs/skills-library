---
id: computing-software.database-administration.supabase.edge-function-secrets
name: edge-function-secrets
category: computing-software
field: database-administration
product: supabase
tags: [edge-functions, secrets, env-file, supabase-secrets, default-secrets]
level: practitioner
status: docs-checked
description: "Manage Supabase Edge Function secrets: supabase secrets set and list, default SUPABASE_ variables, local .env files and who can change production secrets."
sources:
  - https://supabase.com/docs/guides/functions/secrets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give functions configuration without leaking it.

```bash
supabase functions serve hello-world --env-file supabase/functions/.env
supabase secrets set --env-file .env
supabase secrets set STRIPE_SECRET_KEY=sk_live_...
supabase secrets list
deno run --allow-env --env-file=supabase/functions/.env script.ts
```

Default secrets in every function: `SUPABASE_URL`, `SUPABASE_DB_URL`, `SUPABASE_PUBLISHABLE_KEYS`, `SUPABASE_SECRET_KEYS`, `SUPABASE_JWKS`. Legacy: `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`. Hosted only: `SB_REGION`, `SB_EXECUTION_ID`, `DENO_DEPLOYMENT_ID`.

Rules:
- Local secrets live in `supabase/functions/.env`, loaded when the local stack starts. A root `.env` is the one `config.toml` reads (via `env()`); a variable the function needs must also be in `supabase/functions/.env`. A file you name yourself, such as `.env.local`, is read only when passed with `--env-file`.
- Add secret files to `.gitignore`; a `.env.example` is not enough because the runtime needs real values.
- Only Owners and Administrators can create or delete production secrets; Developers can view.
- Names cannot start with the reserved `SUPABASE_` prefix.
- Production functions pick up new secrets immediately; no redeploy.
- Return the result of a secret check, never the value.
- A Deno script run outside `supabase functions serve` needs `--env-file` and `--allow-env`.
- If a variable is empty, restart the stack or pass the env file to `serve`.
- Secret and service-role keys bypass RLS; keep them out of browsers. Publishable and anon keys are browser-safe only with RLS enabled.

## Checked

2026-11-04: Read the Environment variables guide in full (Markdown source on GitHub for the rendered page's truncated top). Confirmed every command, the default and legacy variable lists, hosted-only variables, local file roles, role requirements, the reserved prefix and the no-redeploy behaviour. Tightened the "root .env feeds only config.toml" wording to the page's.
Method: documentation only; no commands were run.
