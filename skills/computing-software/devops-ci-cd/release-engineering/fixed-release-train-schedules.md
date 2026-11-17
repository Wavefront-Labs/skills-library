---
id: computing-software.devops-ci-cd.release-engineering.fixed-release-train-schedules
name: fixed-release-train-schedules
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, train-schedule, release-train, code-freeze, release-calendar, time-based-releases, branch-cut]
level: practitioner
status: docs-checked
description: "Run time-based release trains: picking cadence, the calendar of branch cut, stabilisation and ship dates, what may board late, missed-train rules and automating the schedule."
sources:
  - https://docs.gitlab.com/ee/policy/maintenance.html
  - https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/release_cycle.md
  - https://wiki.mozilla.org/Release_Management/Calendar
  - https://kubernetes.io/releases/release/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fixed release train schedules

A release train leaves on a fixed date whether or not every feature is ready. Features that miss take the next train. It trades scope for predictability.

## Pick the cadence
| Cadence | Typical for |
|---|---|
| weekly / biweekly | teams with fast, low-risk release mechanics |
| two weeks | Chrome (a new milestone ships to stable every two weeks, per Chromium's release cycle doc) |
| monthly | GitLab (third Thursday) |
| about three per year | Kubernetes minor releases |
Short trains make missing one cheap, which is what makes the model work.

## The calendar (example 4-week train)
| Day | Event |
|---|---|
| T-14 | feature complete: branch cut `release/2026.11` from main |
| T-14..T-3 | stabilisation: only bug fixes, cherry-picked via PR with release-manager approval |
| T-7 | release candidate to beta/canary users |
| T-3 | code freeze: only blocker fixes |
| T-0 | ship; staged rollout begins |
Publish the calendar a year ahead (shared calendar + `RELEASES.md`), including holiday adjustments.

## Boarding rules
- Unfinished work ships dark behind feature flags; main is always releasable.
- After branch cut, a change boards only if it's a regression fix, security fix, or release-blocker; a named release manager decides.
- "Missed the train" is normal; no slipping the date for a feature. Slip only for quality blockers, and then announce the new date.

## Automation
```yaml
# GitHub Actions: cut the branch on schedule
on:
  schedule: [{ cron: "0 9 * * 4" }]   # Thursdays; script checks if today is a cut day from releases.yml
jobs:
  cut:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
        with: { fetch-depth: 0 }
      - run: ./scripts/cut-release-if-due.sh releases.yml   # creates release/<version>, bumps version on main, opens tracking issue
```
- Tracking issue per train with checklist (RC built, release notes drafted, go/no-go).
- Bots label PRs merged after the cut as "next train" and manage backport labels.

## Health metrics
- Trains shipped on time (%), cherry-picks per train (rising = main quality problem), time from merge to production.

## Verify
- [ ] Calendar published and followed for three consecutive trains; branch cut automated.
- [ ] Late features were flagged off rather than delaying the train.

## Checked

2026-10-28. Confirmed: GitLab maintenance policy (monthly release on the third Thursday), Chromium release cycle doc (a new milestone to stable every two weeks), Kubernetes release docs (releases happen about three times per year, with a code freeze before release). Corrected: the browser row (Chrome was listed at 4 weeks; Firefox was removed because its calendar page gave no cadence) and Kubernetes (about 15 weeks replaced by about three per year). Removed: the mobile-app cadence claim and the `actions/checkout@v4` pin.

Method: documentation only; no commands were run.
