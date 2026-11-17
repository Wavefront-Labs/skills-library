---
id: computing-software.devops-ci-cd.verdaccio.publish-offline-owners-readmes
name: publish-offline-owners-readmes
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [allow-offline, check-owners, keep-readmes, publish-block, package-owners, offline-publish]
level: practitioner
status: docs-checked
description: "The publish block: allow_offline, check_owners (7.x) to restrict changes to package owners, and keep_readmes (7.x) to retain tagged or all readmes."
sources:
  - https://verdaccio.org/docs/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
publish:
  allow_offline: false
  check_owners: false
  keep_readmes: 'tagged'
```
- `allow_offline: true` lets clients publish while offline (not allowed by default).
- `check_owners` (7.x): when true, only package owners can change a package. The first owner is whoever published the first version. Manage owners with `npm owner` and list them with `npm owner list` (or read `maintainers` in the package manifest).
- `keep_readmes` (7.x): by default only the latest version's readme markdown is stored. `'tagged'` keeps readmes of versions that carry dist-tags (latest, next, ...); `'all'` keeps the full history and can use much more storage.

6.x does not receive these features.

Verify: `npm owner list <pkg>` shows the owners; with `check_owners` on, only those owners may change the package.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Configuration (Advanced Settings: Offline Publish, Checking Package Ownership, Keep Readmes). Confirmed: allow_offline, check_owners and keep_readmes with the 7.x availability, the first-owner rule and the tagged and all readme behaviour. Removed or corrected: the npm owner add|rm detail and the claim about access applying first.

Method: documentation only; no commands were run.
