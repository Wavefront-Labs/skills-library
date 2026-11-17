---
id: computing-software.devops-ci-cd.argo-cd.debugging-cmp-timeouts-and-logs
name: debugging-cmp-timeouts-and-logs
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, cmp-timeout, argocd-exec-timeout, config-management-plugin]
level: advanced
status: docs-checked
description: "Debug slow or failing Argo CD config management plugins: sidecar logs, ARGOCD_EXEC_TIMEOUT and server.repo.server.timeout.seconds, discovery failures and caching."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/config-management-plugins/#debugging-a-cmp", "https://argo-cd.readthedocs.io/en/stable/operator-manual/high_availability/", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_manifests/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging CMP timeouts and logs

## Where to look
```bash
kubectl -n argocd logs deploy/argocd-repo-server -c <plugin-sidecar> --tail=200
```
Verify the sidecar started: `kubectl get pod -l app.kubernetes.io/component=repo-server -n argocd` should show the extra container running. Write plugin log messages to stderr and run the sidecar with `--loglevel=info` to print everything written to stderr, even on success.

## Timeouts (all must line up)
| Setting | Where | Default |
|---|---|---|
| `ARGOCD_EXEC_TIMEOUT` | env on the **plugin sidecar** (each CMP command times out independently; the repo-server enforces the same variable for helm/kustomize) | 90s |
| `server.repo.server.timeout.seconds` / `controller.repo.server.timeout.seconds` | argocd-cmd-params-cm | 60s |

A plugin needing 3 minutes (helmfile with many charts, secrets decryption) needs e.g.
`ARGOCD_EXEC_TIMEOUT=300s` on the sidecar and repo-server timeouts of 300 on server and controller.
If you raise the repo-server timeout above 90 s, also set `ARGOCD_EXEC_TIMEOUT` on the sidecar. A command that ignores the timeout signal is killed after a further `ARGOCD_EXEC_FATAL_TIMEOUT`.

## Discovery problems
- Plugin not matched: the `discover` rule (`fileName` glob, `find.glob` or `find.command`) did not match and no `plugin.name` is set. Set the name explicitly (`<name>-<version>` if the plugin has a version).
- Sidecar problems: check that `/var/run/argocd/argocd-cmp-server` is the container command, the container runs as user 999 and `plugin.yaml` is at `<ARGOCD_HOME>/cmp-server/config/plugin.yaml`.
- `plugin.yaml` from a ConfigMap changed: restart the repo-server pod. Baked into the image: force a re-pull (`imagePullPolicy: Always` for a static tag).
- CMP errors are cached by the repo-server in Redis, and a restart does not clear the cache: do a Hard Refresh while developing.

## Speed
- Pre-bake tools in the image instead of downloading in `init`.
- With `discover`, the repo-server copies the repository (or only the paths in `argocd.argoproj.io/manifest-generate-paths`) into a directory per plugin; exclude `.git/**` via plugin tar stream exclusions to cut disk load and generation time.

## Verify
- [ ] `argocd app manifests <app>` (`--source git`, the default) renders after a hard refresh (`argocd app get <app> --hard-refresh`) within the timeout.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: CMP debugging steps (restart for ConfigMap, image re-pull, Redis-cached errors and Hard Refresh, stderr logging with `--loglevel=info`, sidecar check), `ARGOCD_EXEC_TIMEOUT` default 90 s and `ARGOCD_EXEC_FATAL_TIMEOUT`, repo-server timeout keys default 60 s, `argocd app manifests --source live|git`, hard refresh flag. Removed unconfirmed error strings, the reconciliation-timeout row (the stated 180 s was stale) and caching remarks.

Method: documentation only; no commands were run.
