---
id: computing-software.database-administration.supabase.edge-function-deploy
name: edge-function-deploy
category: computing-software
field: database-administration
product: supabase
tags: [edge-functions, deploy, ci, verify-jwt, project-ref]
level: intro
status: docs-checked
description: "Deploy Supabase Edge Functions with the CLI and from GitHub Actions, GitLab CI or Bitbucket, including required variables and verify_jwt config."
sources:
  - https://supabase.com/docs/guides/functions/deploy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get functions from the repo to production.

Local steps:

```bash
supabase login
supabase projects list
supabase link --project-ref your-project-id
supabase functions deploy
supabase functions deploy hello-world
```

The bare `deploy` ships every function in the `functions` folder; naming one deploys just that. The CLI must be installed, you must be signed in, and the local project linked first. Deployed functions are distributed to edge locations worldwide. The publishable key differs between development and production (see API settings in the dashboard).

CI:
- GitHub Actions: the official `supabase/setup-cli` action, then a deploy step. The page's two samples disagree: the rendered example ends with `supabase functions deploy --project-ref $SUPABASE_PROJECT_ID` (secrets `SUPABASE_ACCESS_TOKEN` and `SUPABASE_PROJECT_ID`), while the page's Markdown source in the GitHub Actions section uses `supabase functions deploy --remote=$PROJECT_ID --yes` (env `PROJECT_ID`). Prefer `--project-ref`, which is also the flag used in `supabase link`; check `supabase functions deploy --help` for `--remote`. The sample workflow deploys on pushes to `main` and can be run manually (`workflow_dispatch`).
- GitLab CI and Bitbucket: `npm i supabase`, then `npx supabase functions deploy --debug --yes`, with `SUPABASE_ACCESS_TOKEN` and `SUPABASE_PROJECT_ID` as CI/CD (GitLab) or repository (Bitbucket) variables. The GitLab sample uses a `docker:dind` service.

Per-function settings such as JWT verification and import map location go in `config.toml`; to disable JWT verification for a function:

```toml
[functions.hello-world]
verify_jwt = false
```

## Checked

2026-11-04: Read the Deploy to Production guide (rendered text was truncated at the top, so the Markdown source on GitHub was read too). Confirmed the local steps, CI variables, GitLab/Bitbucket commands and the `verify_jwt` config. Found the page's two GitHub Actions samples disagree (`--project-ref $SUPABASE_PROJECT_ID` versus `--remote=$PROJECT_ID --yes`); the skill now says so and drops the flag glossary, which the page does not give.
Method: documentation only; no commands were run.
