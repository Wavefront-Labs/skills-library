---
id: computing-software.devops-ci-cd.argo-cd.troubleshooting-argocd-image-updater
name: troubleshooting-argocd-image-updater
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd-image-updater-test, argocd-image-updater, image-updater]
level: practitioner
status: gated
description: "Troubleshoot Argo CD Image Updater: dry-run test command, debug logs, registry auth failures, write-back git errors and apps it silently skips."
sources: ["https://argocd-image-updater.readthedocs.io/en/stable/install/testing/", "https://argocd-image-updater.readthedocs.io/en/stable/basics/update-methods/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Image Updater

**Version note:** the current Image Updater docs (v1.x) describe CRD-based configuration (`ImageUpdater` custom resources); the annotation-based configuration used below belongs to v0.x. Check which major version you run before applying the table below.

## Test resolution offline
```bash
kubectl -n argocd exec -it deploy/argocd-image-updater -- \
  argocd-image-updater test registry.example.com/team/app \
    --update-strategy semver --semver-constraint '1.x' \
    --credentials pullsecret:argocd/regcred --loglevel debug
```
The docs show `argocd-image-updater test <image_name>` with `--update-strategy`, `--semver-constraint`, `--platforms` and `--loglevel`; it needs no changes to Argo CD or the applications and can be run from a workstation. The `--credentials` form above was not checked (gated: unconfirmed, source is paywalled or blocked).

## Logs
```bash
kubectl -n argocd logs deploy/argocd-image-updater --tail=300
```
The IMAGE_UPDATER_LOGLEVEL variable and the exact summary log line were not confirmed (gated: unconfirmed, source is paywalled or blocked); use the `--loglevel` option documented for the CLI.

## Common problems
The table rows below are unconfirmed field experience for the v0.x annotation model (gated: unconfirmed, source is paywalled or blocked).
| Symptom | Cause | Fix |
|---|---|---|
| App never processed | missing `image-list` annotation or app not Helm/Kustomize (directory apps unsupported) | annotate; use Kustomize/Helm |
| `unauthorized` / `denied` from registry | no credentials for that registry | `registries.conf` credentials or `pull-secret` annotation |
| Picks wrong tag | strategy/filter mismatch | test command with filters |
| `could not update application spec: ... permission denied` | Updater's Argo API account lacks `applications, update` | RBAC `role:image-updater` |
| Git write-back `authentication required` / `non-fast-forward` | creds or branch protection | `write-back-method: git:secret:argocd/git-creds`, write-back-target branch, allow bot push |
| Updated but rolled back | parent app-of-apps reverts parameter override | use git write-back |
| ECR auth expires | static token | `ext:/scripts/ecr-login.sh` credential with `credsexpire: 10h` |

## Verify
- [ ] Log shows `Successfully updated image ... to ...`; for git write-back, a commit `.argocd-source-<app>.yaml` appears.

## Checked

2026-11-02. Confirmed against the Image Updater docs (stable): the project has moved to CRD-based configuration in v1.0.0, with annotations documented for v0.x only; the argocd-image-updater test command and its --update-strategy, --semver-constraint, --platforms and --loglevel options; image pull secrets must be in the cluster where the updater runs. Added a version note. Gated: log variable and line, --credentials form and every row of the problems table.

Method: documentation only; no commands were run.
