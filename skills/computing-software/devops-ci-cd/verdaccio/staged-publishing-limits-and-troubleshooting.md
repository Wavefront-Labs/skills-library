---
id: computing-software.devops-ci-cd.verdaccio.staged-publishing-limits-and-troubleshooting
name: staged-publishing-limits-and-troubleshooting
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [staged-publishing, npm-stage, four-eyes, staged-storage, stage-409, stage-404, min-release-age]
level: advanced
status: docs-checked
description: "Operate staged publishing: where staged items live, limits (no expiry, one process, memory on approve), and fixes for 404 and 409 errors and hidden approved versions."
sources:
  - https://verdaccio.org/docs/staged-publishing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Staged items are stored in the existing backend under a reserved namespace:

```
<storage>/.stage/package.json            index
<storage>/.stage/<uuid>/package.json     record
<storage>/.stage/<uuid>/<name>-<v>.tgz   tarball
```
They never appear in search, `/-/all` or the web UI home page.

Limitations:
- Nothing expires; unapproved items stay on disk, so watch `<storage>/.stage`.
- One Verdaccio process only; several instances sharing storage are unsupported.
- Approval reads the tarball fully into memory.
- npm only.

Troubleshooting:
- `404` on `POST /-/stage/package/...` or `npm stage list`: flag off, or server not restarted, or the wrong config file.
- `409` when staging: that name@version is already published or already staged (`npm stage list <package>`).
- `409` when approving: published by another route meanwhile; the staged item is kept so you can inspect it, then reject it.
- Approved but `npm install` cannot find it: check `min-release-age` in `.npmrc`; test with `npm install <pkg> --min-release-age=0`.

Notifications: `publishType` values `stage` and `unstage` fire on staging and rejection, so a webhook can alert reviewers.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Staged publishing. Confirmed: the .stage storage layout, the hidden namespace, the four limitations, the 404 and 409 troubleshooting entries, the min-release-age check and the stage and unstage publish types. Removed or corrected: nothing.

Method: documentation only; no commands were run.
