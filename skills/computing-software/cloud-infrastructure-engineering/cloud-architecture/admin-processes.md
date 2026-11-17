---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.admin-processes
name: admin-processes
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, 12-factor-app, twelve-factor, admin-processes, one-off-processes, database-migrations, kubernetes-jobs, cloud-run-jobs, repl-access, database-migrations-at-deploy]
level: practitioner
status: docs-checked
description: "Apply factor XII: run migrations, data fixes and consoles as one-off processes from the same release and config as the app, repeatable and audited."
sources: ["https://12factor.net/admin-processes", "https://kubernetes.io/docs/concepts/workloads/controllers/job/", "https://cloud.google.com/run/docs/create-jobs"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Factor XII — Run admin tasks as one-off processes

Migrations, REPL sessions and one-time scripts run against a release, with the same codebase, config and dependency
isolation as the long-running processes (12factor.net). Admin code ships with the application code to avoid
synchronisation issues.

## Steps
1. Ship admin code in the app's codebase (for example `manage.py migrate` in Django or `rake db:migrate` in Rails).
2. Run them as one-off executions of the current release:
   - Kubernetes `Job`, with `backoffLimit` and `activeDeadlineSeconds` set deliberately.
   - Cloud Run jobs.
3. Use the same dependency mechanism for admin commands as for the app (for example `bundle exec rake db:migrate` if
   the web process uses `bundle exec`).
4. Data fixes: scripted, reviewed, idempotent, with a dry-run mode and logged row counts.
5. Interactive consoles: through access you can audit and time-limit; 12factor.net notes production consoles are
   typically reached by ssh or the environment's remote command mechanism.

## Gotchas
- Laptop-run scripts against prod with personal credentials: no audit, wrong versions.
- Long backfills: batch with checkpoints and throttle to protect the database.

## Verify
- [ ] Every migration/backfill has a pipeline run id.
- [ ] No human has standing write credentials to prod databases.

## Checked
2026-11-01. Confirmed in 12factor.net Admin processes (same release, config and dependency isolation, examples of
migrations and consoles, admin code ships with app, ssh in production), and the Kubernetes Job and Cloud Run create-jobs
pages for the Job fields and Cloud Run jobs. Removed: Helm/Argo hooks, ECS run-task, WebJobs, Container Apps jobs,
migration-locking and expand/contract claims, kubectl exec/SSM specifics, "never via SSH" wording.
Method: documentation only; no commands were run.
