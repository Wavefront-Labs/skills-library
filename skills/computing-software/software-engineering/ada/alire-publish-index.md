---
id: computing-software.software-engineering.ada.alire-publish-index
name: alire-publish-index
category: computing-software
field: software-engineering
product: ada
tags: [ada, alire-publish-index]
level: advanced
status: docs-checked
description: "Publish a crate to the Alire community index: alr publish, required manifest fields, SPDX licences and release sources."
sources:
  - https://alire.ada.dev/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alire publishing and index
```
alr publish          # runs checks, writes alire/releases/<crate>-<version>.toml, offers to open the index PR
```
- Required for the community index: `description`, `licenses` (a valid SPDX expression, or `custom-...`), `maintainers` (name optional, email mandatory) and `maintainers-logins` (GitHub logins). `website` is optional.
- The commit to publish must exist locally and at the remote; by default the last commit is used and the revision is resolved to a commit, so a moving branch or tag cannot change a release.
- `alr publish --tar` builds a source archive you upload yourself, then give its URL to `alr publish`.
- The community index is the alire-index repository; releases arrive as a pull request and become usable after `alr index --update-all`.
## Gotchas
- Only the listed maintainers can submit later releases or metadata changes; the first submission is approved manually.
## Self-check
Run `alr publish --skip-submit` and read the warnings; it skips opening the pull request.

## Checked
2026-11-03. Confirmed in the Alire documentation (publishing section and manifest reference): `alr publish` steps, `--skip-submit`, `--tar`, manifest properties and their requirement level, maintainers rule, `alr index --update-all`. Removed the CI version/tag claim and `website or origin` as required.
Method: documentation only; no commands were run.
