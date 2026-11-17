---
id: computing-software.cloud-infrastructure-engineering.terraform.drift-alerting-to-chat-and-issues
name: drift-alerting-to-chat-and-issues
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, drift-alerting, drift-detection, scheduled-drift, slack, github-actions]
level: practitioner
status: docs-checked
description: "Turn scheduled drift checks into actionable alerts: detailed-exitcode handling, summarised drift in Slack, deduplicated GitHub issues, and HCP drift notifications."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#detailed-exitcode", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings/notifications", "https://docs.github.com/en/rest/issues/issues"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Drift alerting

## Detect
```bash
set +e
terraform plan -refresh-only -detailed-exitcode -no-color -out=drift.tfplan > drift.txt
rc=$?; set -e
# 0 = no drift, 1 = error, 2 = drift
```
Also run a normal `plan -detailed-exitcode` if you want "code not applied" drift
(merged but never applied) in the same report.

## Summarise (not the whole plan)
```bash
terraform show -json drift.tfplan | jq -r '.resource_drift[]?
  | "\(.change.actions|join("/")) \(.address)"' > drift-summary.txt
```

## Slack
```bash
if [ $rc -eq 2 ]; then
  jq -n --arg s "$(head -30 drift-summary.txt)" --arg u "$RUN_URL" \
    '{text: ":warning: Drift in payments/prod\n```\($s)```\n<\($u)|run>"}' \
  | curl -s -X POST -H 'Content-type: application/json' --data @- "$SLACK_WEBHOOK"
fi
[ $rc -eq 1 ] && echo "drift check FAILED (error, not drift)" && exit 1
```
Alert on errors separately; a broken drift job that silently exits 1 looks like "no drift".

## Deduplicated GitHub issue
```bash
TITLE="Drift: payments/prod"
num=$(gh issue list --state open --search "in:title \"$TITLE\"" --json number -q '.[0].number')
if [ $rc -eq 2 ]; then
  if [ -n "$num" ]; then gh issue comment "$num" --body-file drift-summary.txt
  else gh issue create --title "$TITLE" --label drift --body-file drift-summary.txt; fi
elif [ $rc -eq 0 ] && [ -n "$num" ]; then
  gh issue close "$num" --comment "No drift as of $(date -u +%F)"
fi
```

## HCP Terraform
Health assessments detect drift (Standard and Premium editions). Enable workspace
notifications with the **Drift detected** and **Health assessment errored** triggers;
both exist only when health assessments are enabled for the workspace. Destinations:
generic webhook, Slack, Microsoft Teams or email.

## Hygiene
- Owner per stack in the alert; unowned alerts are ignored.
- Ignore known noise with `ignore_changes`, not by muting the channel.
- Never auto-apply refresh-only results.

## Verify
- [ ] A manual console change produces exactly one alert/issue; reverting closes it.
- [ ] Exit code 1 pages differently from drift.

## Checked
2026-10-28. Confirmed against the Terraform `plan` command page (`-detailed-exitcode`), the JSON output format page (`resource_drift`, `change.actions`), the HCP Terraform workspace notifications page (triggers, destinations, health assessment requirement), the GitHub CLI manual for `gh issue list|create|comment|close` (`--search`, `--json`, `-q`, `--state`, `--label`, `--title`, `--body-file`, `--comment`) and the Slack incoming webhooks page (JSON `text` payload, `Content-type: application/json`).
Corrected: the HCP notification trigger names (the docs call them Drift detected and Health assessment errored, not Drift / Check failure).
Removed: nothing else; the remaining claims are shell logic.
Method: documentation only; no commands were run.
