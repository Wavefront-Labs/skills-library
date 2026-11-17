---
id: computing-software.devops-ci-cd.skaffold.status-check
name: status-check
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [status-check, rollout, deadline, progressdeadlineseconds]
level: practitioner
status: docs-checked
description: "Skaffold waits for deployed resources to become ready; tune or disable the check and its deadline."
sources:
  - "https://skaffold.dev/docs/status-check/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

After deploying, Skaffold checks that resources become healthy. It is enabled by default and monitors Pods, Deployments, StatefulSets and Cloud Run services.

Configure it:

```yaml
deploy:
  statusCheck: true
  statusCheckDeadlineSeconds: 300
```

- The default deadline is 10 minutes.
- If a Deployment sets `progressDeadlineSeconds`, Skaffold waits that long; if `statusCheckDeadlineSeconds` is also set, the Deployment value wins only when it is smaller.
- Disable with `--status-check=false` or `deploy.statusCheck: false`.

Behavior: container logs are suppressed until the check passes, so a failing deployment shows status messages first. If the deadline passes, the command fails, which in CI gives a failing job.

With several skaffold modules active, the `statusCheck` field disables the check only for that config, while `--status-check=false` disables it for all modules.

By default the check exits when a single deployment fails. Set `tolerateFailuresUntilDeadline` (or pass `--tolerate-failures-until-deadline`) to keep waiting until the deadline, which suits CI where services flap while they start; pair it with `statusCheckDeadlineSeconds`.

With several deployers or imported configs, one status check runs after all deployers. `--iterative-status-check=true` runs it after each deployer instead, which helps when services have startup dependencies.

Tune the deadline per environment with a profile so slow clusters do not fail spuriously.

If the check fails, rerun with `--status-check=false` to see the deployed resources' logs.

## Checked

2026-11-09: confirmed against the Skaffold docs page "Deploy Status Checking" (source file docs-v2/content/en/docs/status-check.md): monitored resource types, default on, the flag and field to disable it, 10 minute default, deadline precedence, log suppression, tolerateFailuresUntilDeadline, iterative status check. Removed a nonexistent "dedicated status check command" and unverified troubleshooting advice.

Method: docs-checked 2026-11-09 against skaffold.dev status-check page (read in full as source markdown).
