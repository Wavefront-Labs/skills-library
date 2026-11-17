---
id: computing-software.devops-ci-cd.deployment-strategies.booking-and-locking-shared-environments
name: booking-and-locking-shared-environments
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, environment-booking, environments-management, deploy-locks]
level: intro
status: docs-checked
description: "Coordinate shared test/staging environments: booking or locking so teams do not overwrite each other's deployments, with CI-enforced locks and expiry."
sources: ["https://docs.gitlab.com/ci/resource_groups/", "https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Booking and locking shared environments

When a few shared environments (qa1, qa2, staging) serve many teams, deployments clobber each other
and test results become meaningless.

## Lightweight booking
- A lock record per environment: holder, reason, PR/branch, expiry. Stored in a small service, a
  repo file, chat bot, or the CI system itself.
- Deploy jobs **check the lock** and refuse if held by someone else.
- Locks expire automatically (e.g. 4 hours) to avoid forgotten bookings.

## CI-enforced options
- GitLab `resource_group: qa1` serialises jobs targeting qa1; combine with a manual "release qa1" job.
- GitHub `concurrency: { group: env-qa1, cancel-in-progress: false }` serialises deploys; it does not
  express "booked for testing for 3 hours", so add a lock check step.
- Jenkins Lockable Resources plugin: builds wait for a named resource to be free, and resources can be reserved manually.

```bash
# simple lock check against a JSON in an S3 bucket
holder=$(aws s3 cp s3://env-locks/qa1.json - 2>/dev/null | jq -r 'select(.expires > now) | .holder')
[ -z "$holder" ] || [ "$holder" = "$GITHUB_ACTOR" ] || { echo "qa1 booked by $holder"; exit 1; }
```

## Better long term
Ephemeral per-PR environments remove most need for booking; keep shared staging for final integration.

## Verify
- [ ] A deploy to a booked environment by another user fails with the holder's name; expired bookings release automatically.

## Checked

2026-10-28. Confirmed: GitLab resource groups (`resource_group` keyword limits a job to one run at a time), GitHub workflow concurrency (`concurrency` groups and `cancel-in-progress`), Jenkins Lockable Resources plugin page (builds wait for a locked resource; resources can be reserved), GitHub default variable `GITHUB_ACTOR`. Removed: the `lock(resource: ...)` step syntax, which the plugin page did not show.

Method: documentation only; no commands were run.
