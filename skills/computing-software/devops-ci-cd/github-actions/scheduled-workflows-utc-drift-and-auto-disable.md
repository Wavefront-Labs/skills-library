---
id: computing-software.devops-ci-cd.github-actions.scheduled-workflows-utc-drift-and-auto-disable
name: scheduled-workflows-utc-drift-and-auto-disable
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, schedule-cron, cron-utc, schedule-drift, scheduled-workflow-disabled, cron-delay, high-load-times, default-branch-only, keepalive, workflow-inactivity, nightly-build, schedule-timezone, posix-cron, schedule-filters, workflow-triggers]
level: practitioner
status: verified
description: "Run cron workflows reliably: UTC-only syntax, why :00 runs start 5-30 minutes late, default-branch-only evaluation, the 60-day inactivity auto-disable and how to keep schedules alive."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule", "https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/disabling-and-enabling-a-workflow"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled workflows: UTC, drift and auto-disable

**Goal:** a nightly job that actually runs every night, at a predictable time, and does not
silently stop after two months.

## 1. Syntax and rules
```yaml
on:
  schedule:
    - cron: '17 3 * * 1-5'     # 03:17 UTC Mon-Fri — POSIX 5-field only, quoted
    - cron: '0 */6 * * *'      # several entries allowed; each fires separately
```
- **UTC by default**, so DST shifts your local time twice a year. GitHub's docs now also describe an
  optional `timezone: America/New_York` key (IANA name) next to `cron:`, which actionlint 1.7.12
  accepts; without it keep a comment with the intended local time.
- The shortest interval is once every 5 minutes. The documented operators are `*`, `,`, `-` and `/`;
  `@yearly`, `@monthly`, `@weekly`, `@daily`, `@hourly` and `@reboot` are not supported (actionlint:
  `parser does not accept descriptors`).
- Evaluated from the workflow file on the **default branch only**. A schedule added on a
  feature branch does nothing until merged; the run checks out the default branch head.
- `github.event` is nearly empty: `github.event.schedule` holds the matching cron string, so
  one workflow can branch on which entry fired.

## 2. Drift
The `schedule` event can be delayed during periods of high load, which include the start of every hour,
and if load is high enough some queued jobs may be **dropped** (GitHub docs). Pick an odd minute
(`17 3`) and avoid the top of the hour. Do not build logic that
assumes exact timing (e.g. "the 03:00 run creates the file the 03:30 run reads") — chain
with `workflow_run` or one workflow instead.

## 3. Auto-disable after 60 days
In a public repository scheduled workflows are automatically disabled when no repository activity has
occurred in **60 days**. The workflow's `actor` is the user who last changed the cron line (or who
changed the default branch): scheduled runs need that user *account* to be active, but removing the user
from the organization does not stop them (GitHub docs). Re-enable options:
- `gh workflow enable nightly.yml` or the UI;
- a commit by a user with write access that changes the `cron` line reactivates it.

## 4. Testing a schedule
Add `workflow_dispatch:` alongside `schedule:` so you can trigger it by hand; branch on
`github.event_name` where behaviour must differ. Verify timing after the first cron fire with
`gh run list --workflow nightly.yml --event schedule --json createdAt,startedAt`.

## 5. Gotchas
- `paths` filters belong to `push` and `pull_request`, not `schedule`; the run always uses the default
  branch.
- A job that uses an environment with required reviewers waits for approval, so a nightly deploy to a
  protected environment will not run unattended.
- Concurrency: two overlapping slow nightlies run in parallel unless you set
  `concurrency: { group: nightly, cancel-in-progress: false }`.

## Verify
- [ ] Cron is quoted, 5 fields, minute not `0`.
- [ ] Workflow is on the default branch and shows the next scheduled time in the Actions tab.
- [ ] A `workflow_dispatch` trigger exists for manual testing.
