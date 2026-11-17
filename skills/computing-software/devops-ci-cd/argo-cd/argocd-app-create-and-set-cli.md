---
id: computing-software.devops-ci-cd.argo-cd.argocd-app-create-and-set-cli
name: argocd-app-create-and-set-cli
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd-app-create, argocd-cli, application]
level: practitioner
status: docs-checked
description: "Create and modify Argo CD Applications from the CLI (argocd app create/set/unset), then export them to declarative YAML so the CLI is not the source of truth."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_create/", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_set/", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_unset/", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_login/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# argocd app create / set from the CLI

```bash
argocd login argocd.example.com --sso          # or --username admin --grpc-web
argocd app create guestbook \
  --project team-a \
  --repo https://github.com/org/deploy.git --path apps/guestbook/overlays/prod --revision main \
  --dest-server https://kubernetes.default.svc --dest-namespace guestbook \
  --sync-policy automated --auto-prune --self-heal \
  --sync-option CreateNamespace=true --sync-option ServerSideApply=true \
  --label team=a --upsert
```
Helm source: `--helm-chart <chart> --repo <chart-repo-url> --revision <chart-version>
--values-literal-file values.yaml --helm-set replica.replicaCount=2`.

## Modify
```bash
argocd app set guestbook --revision v1.4.0
argocd app set guestbook --kustomize-image app=registry.example.com/app:1.4.0
argocd app set guestbook --helm-set image.tag=1.4.0
argocd app unset guestbook --kustomize-image app       # remove override
argocd app set guestbook --sync-policy none            # disable auto-sync
```

## Export to Git
```bash
argocd app get guestbook -o yaml > apps/guestbook.yaml     # -o accepts json|yaml|wide|tree
```
Remove the server-populated fields (`status`, `metadata.managedFields`, `resourceVersion`, `uid`, `creationTimestamp`) by hand, then commit it to the app-of-apps/ApplicationSet repo.

## Gotchas
- `--upsert` updates an existing app with the same name; without it, differing specs error.
- Parameter overrides (`app set --helm-set`) live in the Application spec, not in Git.
- `--grpc-web` is for Argo CD servers behind a proxy that does not support HTTP/2.
- RBAC: `applications, create` on the project is needed; `argocd account can-i create applications 'team-a/*'`.

## Verify
- [ ] `argocd app get guestbook` shows Synced/Healthy; the exported YAML (server fields removed) re-applies with no diff.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: flags of `argocd app create`/`set` (`--project`, `--repo`, `--path`, `--revision`, `--dest-server`, `--dest-namespace`, `--sync-policy` values, `--auto-prune`, `--self-heal`, `--sync-option`, `--label` (create only), `--upsert` semantics, `--helm-chart`, `--values-literal-file`, `--helm-set`, `--kustomize-image`), `app unset --kustomize-image`, `app get -o` formats, `login --sso` and `--grpc-web`, `account can-i` argument form. Removed the pinned chart example, the yq pipeline and two unconfirmed remarks.

Method: documentation only; no commands were run.
