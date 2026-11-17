---
id: computing-software.devops-ci-cd.helm.rollback-command
name: rollback-command
category: computing-software
field: devops-ci-cd
product: helm
tags: [rollback, revision, history, release, cleanup-on-fail]
level: practitioner
status: docs-checked
description: "Roll back a release to an earlier revision with helm rollback and understand how revisions and history limits interact."
sources:
  - "https://helm.sh/docs/helm/helm_rollback/"
  - "https://helm.sh/docs/helm/helm_history/"
  - "https://helm.sh/docs/topics/charts/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helm rollback RELEASE [REVISION]` restores a release to a previous revision. If the revision is omitted or set to 0, Helm rolls back to the previous release. Find revision numbers with `helm history RELEASE`.

A rollback is itself a new revision. The history output shows a description such as `Rolled back to 2`, and `helm history --show-rollback-revision` adds a ROLLBACK column showing the revision that was rolled back to.

Flags from the rollback reference:

- `--cleanup-on-fail` allows deletion of new resources created in this rollback when it fails.
- `--description` adds a custom description (max 256 characters).
- `--history-max` limits stored revisions; default 10, 0 for no limit.
- `--no-hooks` prevents hooks from running during rollback.
- `--wait`, `--wait-for-jobs` and `--timeout` (default 5m0s) control readiness waiting.
- `--force-replace`, `--force-conflicts` and `--server-side` tune how objects are applied.

Because only the retained revisions can be targeted, a low `--history-max` (or `HELM_MAX_HISTORY`) limits how far back you can go.

Helm never installs CRDs on upgrade or rollback (it creates them only on install), so CRD changes must be reverted by hand. `helm upgrade --rollback-on-failure` rolls the upgrade back to the previous successful release when it fails.

## Checked

2026-11-03. Confirmed against helm.sh pages for helm rollback (synopsis, all flags and defaults), helm history (Rolled back to N, --show-rollback-revision, ROLLBACK column), helm upgrade (--history-max, --rollback-on-failure) and topics/charts (CRDs never installed on upgrade or rollback). Removed: the pre/post-rollback hook claim and the Helm 4 label (not on the pages).
Method: documentation only; no commands were run.

