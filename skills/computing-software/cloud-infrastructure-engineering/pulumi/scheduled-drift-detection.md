---
id: computing-software.cloud-infrastructure-engineering.pulumi.scheduled-drift-detection
name: scheduled-drift-detection
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, drift-detection, scheduled-refresh, deployments-schedule, drift-schedule]
level: practitioner
status: docs-checked
description: "Run Pulumi refresh on a schedule: Pulumi Cloud Deployments cron schedules, or a CI job using pulumi refresh --expect-no-changes or --preview-only."
sources:
  - https://www.pulumi.com/docs/deployments/concepts/schedules/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_refresh/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled drift detection

**Option 1: Pulumi Cloud Deployments schedules** (Pro and Enterprise). Configure Deployments settings on the stack, then Stack > Settings > Schedules and set a cron expression. Schedules run in UTC unless the expression starts with `CRON_TZ=<IANA zone>` (for example `CRON_TZ=America/New_York 0 9 * * *`); the same rule applies to drift detection and ESC secret rotation schedules. Deployments concurrency limits apply, and pausing deployments on a stack queues scheduled ones. The org-wide schedule list includes Drift and Time-to-Live schedules. Raw schedules can also be created by REST:

```bash
curl -H "Accept: application/vnd.pulumi+8" -H "Content-Type: application/json" \
  -H "Authorization: token $PULUMI_ACCESS_TOKEN" --request POST \
  --data '{ "scheduleCron":"0 0 * * *", "request": { "operation": "update" } }' \
  https://api.pulumi.com/api/stacks/{organization}/{project}/{stack}/deployments/schedules
```
or with the `pulumiservice.DeploymentSchedule` resource (`organization`, `project`, `stack`, `scheduleCron`, `pulumiOperation`).

**Option 2: cron job in CI** using the `pulumi refresh` flags:
- `--expect-no-changes`: return an error if any changes occur; the check happens after the refresh is applied, so state is updated.
- `--preview-only`: only show a preview, do not perform the refresh (report-only).
- `--diff` rich diff, `--yes` auto-approve, `--skip-preview` / `-f`, `--stack` / `-s`, `--non-interactive`.

```bash
pulumi refresh --expect-no-changes --non-interactive --yes --stack <org>/<project>/<stack>
pulumi refresh --preview-only --diff --stack <org>/<project>/<stack>
```

## Gotchas
- A non-zero exit from `--expect-no-changes` is the drift signal for CI; use `--preview-only` when the job must not touch state.
- The scheduled run needs the same credentials as a normal update.
- The schedules page does not document drift-specific CLI subcommands or auto-remediation fields; check the Pulumi Cloud drift detection docs before relying on them.

## Checked
2026-11-03. Confirmed on the Deployments Schedules page (Pro/Enterprise, UI path, `CRON_TZ`, REST body, concurrency, drift listing) and the `pulumi refresh` CLI page (flags). Removed: invented `pulumi deployment schedule drift create` command, drift REST path, `autoRemediate` and `--auto-remediate`, GitHub Actions cron snippet, `ignoreChanges` advice, `pulumi preview --refresh --diff`, Verify paragraph.
Method: documentation only; no commands were run.
