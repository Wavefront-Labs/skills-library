---
id: computing-software.devops-ci-cd.jenkins.embeddable-build-status-badges
name: embeddable-build-status-badges
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, embeddable-build-status, notifications, build-status]
level: intro
status: docs-checked
description: "Add Jenkins build status badges to READMEs with the Embeddable Build Status plugin: badge URLs for jobs and branches, unprotected access and custom subjects."
sources: ["https://github.com/jenkinsci/embeddable-build-status-plugin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embeddable build status badges

Plugin: `embeddable-build-status`. Each job shows "Embeddable Build Status" in its sidebar with
ready-made Markdown.

## URLs
```
https://jenkins.example.com/buildStatus/icon?job=team%2Fapp%2Fmain
https://jenkins.example.com/buildStatus/icon?job=team%2Fapp%2Fmain&subject=build&style=flat-square
https://jenkins.example.com/job/team/job/app/job/main/badge/icon      # protected form
https://jenkins.example.com/buildStatus/icon?job=team%2Fapp%2Fmain&build=lastStable    # selector (lastStable, last, -1, ...)
```
The `job` parameter must be URL-escaped (`%2F` for slashes) and works only on the unprotected URL. For multibranch jobs the branch name inside the selector must be URL-encoded twice (a branch `feature/x` becomes `feature%252Fx`).

Markdown:
```markdown
[![Build](https://jenkins.example.com/buildStatus/icon?job=team%2Fapp%2Fmain)](https://jenkins.example.com/job/team/job/app/job/main/)
```

## Permissions
- `/buildStatus/icon` is the **unprotected** endpoint: it exposes the badge to users with at
  least `ViewStatus` permission on the job (grant it to Anonymous for public badges).
- `/badge/icon` is the **protected** endpoint: it needs at least `Read` permission on the job.
- For public READMEs on a private Jenkins, grant only `ViewStatus` and review what the badge reveals (job name and status).

## Customising
Query parameters: `style` (plastic is the default; flat, flat-square and ball-<size> also exist),
`subject`, `status`, `color`, `animatedOverlayColor`, `link`, `build`, `config`. Define named badges in a
Pipeline with `addEmbeddableBadgeConfiguration(id: 'coverage', subject: 'coverage')` and update the
returned object with `setStatus('87%')`; reference it with `config=coverage`.

## Verify
- [ ] Badge renders in a private browser window (anonymous) and links to the job.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in the Embeddable Build Status README: protected `/badge/icon` (Read) versus unprotected `/buildStatus/icon` (ViewStatus), the `job` parameter (URL escaped, double-encoded branch for multibranch), `build` selectors including `lastStable`, `style` values, `subject`/`status`/`color`/`animatedOverlayColor`/`link`/`config`, and `addEmbeddableBadgeConfiguration` with `setStatus`. Corrected the multibranch encoding note and the `.status =` assignment.
Method: documentation only; no commands were run.
