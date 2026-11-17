---
id: computing-software.devops-ci-cd.argo-cd.jq-normalizer-timeout
name: jq-normalizer-timeout
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, ignore-normalizer-jq-timeout, jq-timeout, diff-normalizer-performance]
level: advanced
status: docs-checked
description: "Diagnose and fix Argo CD jqPathExpressions timing out during diff normalisation by raising ignore.normalizer.jq.timeout or simplifying expressions."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/server-commands/argocd-application-controller/", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_diff/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jq normalizer timeout

`jqPathExpressions` in ignoreDifferences are evaluated for every matching resource on every
diff. Each evaluation is limited by the ignore normalizer JQ execution timeout (default 1 s in the CLI flag help).

## Raise the limit
The application controller has the flag `--ignore-normalizer-jq-execution-timeout-seconds` (a duration, for example `5s`); `argocd app diff` has `--ignore-normalizer-jq-execution-timeout` (default 1s). Set the controller flag through the container args or the matching `argocd-cmd-params-cm` key for your Argo CD version (check the controller command reference), then restart the application controller.

## Better: make expressions cheap
- Prefer `jsonPointers` when the path is fixed.
- Avoid scanning big arrays with nested `select` on large objects (CRDs with huge specs, ConfigMaps with large data).
- Scope ignore rules by `name`/`namespace` so they run on fewer resources.

## When it happens
Usually only on big objects or very busy controllers (CPU throttled). Check controller CPU limits
before raising the timeout — a throttled controller makes every jq evaluation slow.

## Verify
- [ ] The field is ignored in `argocd app diff` and the controller logs show no jq timeout errors.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: controller flag `--ignore-normalizer-jq-execution-timeout-seconds` and CLI flag `--ignore-normalizer-jq-execution-timeout` (default 1s) in the command references, `jqPathExpressions` and `jsonPointers` in ignoreDifferences. Removed the unconfirmed `argocd-cmd-params-cm` key, the failure-mode description, the argocd-server remark and the local jq timing command.

Method: documentation only; no commands were run.
