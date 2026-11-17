---
id: computing-software.database-administration.supabase.branching
name: branching
category: computing-software
field: database-administration
product: supabase
tags: [branching, preview-branches, persistent-branches, github-integration, deployment]
level: practitioner
status: docs-checked
description: "Supabase Branching: preview vs persistent branches, what is cloned, data-less defaults, placeholder secrets and the seven-step merge deployment."
sources:
  - https://supabase.com/docs/guides/deployment/branching/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give each change an isolated Supabase environment.

Types:
- Preview branches are ephemeral and auto-deleted when the PR is merged or closed.
- Persistent branches are long-lived (staging, QA, development) and are not auto-paused or deleted for inactivity or PR closure.

Each branch is a separate Supabase instance with its own API credentials, cloned from the base project with Edge Functions deployed and configuration applied. Dashboard branching is in beta.

Data: branches are data-less by default (no rows or storage objects). Seed files (GitHub integration) or the Dashboard "Include data" option add data. The schema is not cloned: GitHub-connected branches build it from repository migrations, Dashboard branches from the base project's migration history.

Copied settings: Postgres, pooler, Auth, Data API, Realtime and Storage settings, SSL enforcement, network restrictions (if the base has them) and deployed Edge Functions. Auth secrets such as OAuth and SMTP passwords get placeholder values, so set real ones as branch secrets. Database Webhooks are enabled on every branch.

Merging into the base project runs a deployment workflow expressed as a directed acyclic graph of these steps (listed in the page's order):
1. Clone the repository at the git branch (optional for Dashboard branching).
2. Pull migrations from the base project.
3. Health: wait up to 2 minutes for Auth, API, Database, Storage and Realtime.
4. Configure from `config.toml` (GitHub integration only).
5. Migrate: apply pending migrations and vault secrets.
6. Seed (persistent branches need seeding enabled in `config.toml`).
7. Deploy changed Edge Functions and update function secrets.

If a step fails, dependent steps are skipped; a migration failure prevents seeding. With GitHub integration the workflow runs on every commit pushed to the git branch.

## Checked

2026-11-04: Read the Branching overview in full. Confirmed branch types, data-less default, copied settings, placeholder secrets, Database Webhooks, the seven deployment steps, the 2-minute health wait and failure skipping. Reworded "in order" to match the page's DAG description.
Method: documentation only; no commands were run.
