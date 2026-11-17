---
id: computing-software.devops-ci-cd.release-engineering.release-calendar-and-freeze-windows
name: release-calendar-and-freeze-windows
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, release-calendar, release-plan, deploy-freeze]
level: intro
status: docs-checked
description: "Maintain a release calendar with freeze windows (peak trading, holidays, major events), enforce freezes in pipelines and define the exception process."
sources: ["https://docs.gitlab.com/user/project/releases/#prevent-unintentional-releases-by-setting-a-deploy-freeze", "https://sre.google/workbook/canarying-releases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Release calendar and freeze windows

## Calendar contents
- Scheduled releases/trains (dates, branch-cut times) for products that batch.
- Freeze windows: peak business periods (Black Friday, tax deadlines, end of quarter), holidays with
  thin on-call, major marketing launches, dependent vendor freezes.
- Planned maintenance and large migrations, to avoid stacking risk.
Publish as a shared calendar (ICS) and in the deploy tooling, not just a wiki page.

## Enforce in pipelines
- GitLab: deploy freeze periods (crontab start/end, set in the UI or the Freeze Periods API); jobs check
  `$CI_DEPLOY_FREEZE`:
  ```yaml
  deploy:
    rules:
      - if: $CI_DEPLOY_FREEZE
        when: manual        # or never
      - when: on_success
  ```
- Other platforms: a first pipeline step that checks a freeze calendar file or API and fails.

## Exceptions
Defined process: security fixes and incident remediation allowed with named approver (e.g. on-call
lead + product owner), recorded in the change log. Exceptions should be rare; track their count.

## Gotchas
- Long freezes create giant post-freeze releases: keep deploying to non-prod and use flags so the
  first post-freeze deploy is small batches, not one big bang.
- Timezones: define windows in one zone with explicit offsets.

## Verify
- [ ] Attempted production deploy during a freeze is blocked unless the exception path is used.

## Checked

2026-10-28. Confirmed in the GitLab deploy freeze docs: $CI_DEPLOY_FREEZE, freeze periods as crontab entries, set in the UI or the Freeze Periods API. Removed: the exact GitLab menu path, the GitHub custom protection rule claim, the Argo CD sync window claim.

Method: documentation only; no commands were run.
