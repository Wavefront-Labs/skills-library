---
id: computing-software.data-engineering.kestra.git-sync-and-push
name: git-sync-and-push
category: computing-software
field: data-engineering
product: kestra
tags: [git, syncflows, pushflows, syncnamespacefiles, pushnamespacefiles, gitops]
level: advanced
status: docs-checked
description: "Keep Kestra flows and namespace files in Git with SyncFlows, PushFlows, SyncNamespaceFiles and PushNamespaceFiles, and the overwrite and filename traps."
sources:
  - https://kestra.io/docs/version-control-cicd/git
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Four tasks (the page marks only the blueprint, app and unit-test tasks as Enterprise):

- `io.kestra.plugin.git.SyncFlows`: Git is the source of truth; a scheduled flow applies it. Props `url`, `branch`, `username`, `password` (use a secret), `targetNamespace`, `includeChildNamespaces` (default `false`), `gitDirectory`.
- `PushFlows`: commit UI edits to Git. Props `sourceNamespace`, `targetNamespace`, `flows` (e.g. `"*"`), `commitMessage`.
- `SyncNamespaceFiles`: `namespace`, `gitDirectory` (default `_files`), `namespaceDirectory`, `delete`.
- `PushNamespaceFiles`: `files`, `gitDirectory`, `branch`, `commitMessage`.

```yaml
tasks:
  - id: git
    type: io.kestra.plugin.git.SyncFlows
    url: https://github.com/kestra/scripts
    branch: main
    username: git_username
    password: "{{ secret('GITHUB_ACCESS_TOKEN') }}"
    targetNamespace: git
    gitDirectory: your_git_dir
triggers:
  - id: schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "*/1 * * * *"
```

A sync flow can also be started by a webhook trigger from the repository's webhook settings. Push to a feature branch and open a pull request.

Caveats:

- Sync overwrites conflicting UI edits with the Git version. Keep the sync flow itself in Git or the editor; reconciliation does not overwrite it.
- The filename stem is the flow ID during sync and must match the YAML `id`, else "Flow already exists" can occur. `onInvalidSyntax` on TenantSync and NamespaceSync: `FAIL` (default), `WARN`, `SKIP`.
- With `delete: true`, only files under the `namespaceDirectory` prefix can be deleted.
- Enterprise only: SyncNamespaceFiles creates a missing namespace, which needs credentials.

## Checked

2026-11-04. Confirmed against the Kestra Git page: SyncFlows, PushFlows, SyncNamespaceFiles and PushNamespaceFiles examples and properties, includeChildNamespaces default false, gitDirectory default _files, delete limited to the namespaceDirectory prefix, UI edits overwritten by sync, filename stem as flow ID with the Flow already exists error, EE namespace creation needing credentials, webhook trigger. Removed the claim that all four tasks exist in both editions (the page does not state it) and scoped onInvalidSyntax to TenantSync and NamespaceSync where the page documents it.

Method: documentation only; no commands were run.
