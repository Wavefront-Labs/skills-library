---
id: computing-software.devops-ci-cd.spinnaker.pipeline-permissions-managed-accounts
name: pipeline-permissions-managed-accounts
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [fiat, pipeline-permissions, managed-service-accounts, orca, front50, migration, roles]
level: advanced
status: docs-checked
description: "Enable pipeline permissions so Fiat creates managed service accounts from pipeline roles, with the Front50 migrator and its caveat."
sources:
  - https://spinnaker.io/docs/setup/other_config/security/authorization/pipeline-permissions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pipeline permissions let automatically triggered pipelines modify protected accounts and applications without an operator hand-creating a Fiat service account. A user lists roles in the pipeline specification and a service account is created and associated automatically.

**Enable (off by default):**
- Orca, in `orca-local.yml`: `tasks.useManagedServiceAccounts: true`; the page also recommends `tasks.useSharedManagedServiceAccounts: true` to create one service account per unique role set, which cuts auth sync time
- Deck, in `settings-local.js`: `window.spinnakerSettings.feature.managedServiceAccounts = true;`

**Use:** a permissions selector appears once an automated trigger is added to the pipeline in Deck. You can choose any role you currently hold. Afterwards only users with **all** the listed roles can edit or execute the pipeline, matching the service account rule.

**Migrating older pipelines.** Once enabled, the `RunAsUser` selector is hidden but existing triggers keep their old service account. To move one, remove `RunAsUser` from the trigger in the pipeline JSON (when roles are already specified), or let Front50 migrate automatically by setting in `front50-local.yml`:

```yaml
migrations:
  migrateToManagedServiceAccounts: true
```

The migrator is disabled by default and only touches pipelines with no `roles` and a non-managed `runAsUser`. It creates managed users with the same permissions as the manual ones.

**Warning:** a pipeline can have only one managed service user. If its triggers used different `runAsUser` values, the new user gets all their roles combined, which can remove some people's ability to edit or run the pipeline.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Pipeline Permissions page. Confirmed both feature flags, role semantics, the migration behaviour and the multi-trigger warning; added the shared managed accounts flag from the same page.
