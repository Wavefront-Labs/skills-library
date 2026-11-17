---
id: computing-software.devops-ci-cd.verdaccio.staged-publishing-flow-and-permissions
name: staged-publishing-flow-and-permissions
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [staged-publishing, npm-stage, four-eyes, npm-stage-publish, stage-approve, stage-permission, release-review]
level: advanced
status: docs-checked
description: "Review releases before they are installable with the stage flag and npm stage publish, list, download, approve, reject, plus the stage permission for four-eyes."
sources:
  - https://verdaccio.org/docs/staged-publishing/
  - https://verdaccio.org/docs/packages/
  - https://verdaccio.org/docs/setup-npm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Experimental, 7.x and later (not 6.x), needs npm 11.17+ (no Yarn/pnpm equivalent). To try it, the staged publishing page says `npx --yes verdaccio@next-7` while the npm setup page says the 9.x line `verdaccio@next-9`.

```yaml
flags:
  stage: true
packages:
  'my-company-*':
    access: $authenticated
    stage: developers
    publish: release-managers
```
Restart after enabling; with the flag off the `npm stage` commands answer 404.

Flow:
```
npm stage publish [--tag beta]   # uploaded, not installable
npm stage list [pkg] [--json]
npm stage view <id>
npm stage download <id>          # inspect the real tarball and shasum
npm stage approve <id>           # published for real
npm stage reject <id>            # deleted, never existed
```
Approval replays the normal publish path: upstream version check, dist-tag merge, filter plugins, notifications (event `publish`).

Who can do what: stage publish needs `stage`; approve needs `publish`; reject, view and download are for the person who staged it or any publisher. Unauthorized lookups return 404, not 403. `stage` falls back to `publish`; granting `stage` to a group without `publish` makes a real four-eyes control, otherwise one person can stage and approve.

Web UI: `/-/web/stage`. 2FA: `stage publish` never asks an OTP; approve and reject do in auth-and-writes mode.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Staged publishing, Package Access and Setup npm. Confirmed: the stage flag, the npm stage command flow, approval replaying the publish path, the permission table, the 404 for unauthorized lookups, the stage fallback to publish, the four-eyes setup, /-/web/stage and the two-factor interaction. Removed or corrected: 7.x only corrected to 7.x and later; the pages disagree on the try-it line, noted in the skill.

Method: documentation only; no commands were run.
