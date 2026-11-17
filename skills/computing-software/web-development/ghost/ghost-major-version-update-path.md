---
id: computing-software.web-development.ghost.ghost-major-version-update-path
name: ghost-major-version-update-path
category: computing-software
field: web-development
product: ghost
tags: [ghost, upgrade, major-version, lts, reinstall, ghost-cli]
level: advanced
status: docs-checked
description: "Plan a Ghost major version upgrade: update to the latest minor first, check Node and CLI versions, back up, and know the LTS policy."
sources:
  - https://github.com/TryGhost/docs/blob/main/update-major-version.mdx
  - https://github.com/TryGhost/docs/blob/main/faq/major-versions-lts.mdx
  - https://github.com/TryGhost/docs/blob/main/faq/update-0x.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move a site to the current Ghost major without data loss.

Rules from the docs:
- Before a major update, bring the site to the latest minor of its current major and do not be more than 2 majors behind. On Ghost 3.0 run `ghost update v3` then `ghost update v4`; on 4.0 run `ghost update v4`; on 5.0 run `ghost update v5`. Run `ghost backup` first, and if Ghost is not running use `ghost start`, then log in to Ghost Admin and check the minor update worked.
- Check Node with `node -v`; if it is below 22 the guide updates it to 22. Update Ghost-CLI with `sudo npm install -g ghost-cli@latest`; for Ghost 6.0 the guide says v1.28.2 or higher is best (`ghost -v` shows the CLI version).
- Make a full backup with `ghost backup` (zip with JSON content, a member CSV export, themes, images and media, and routes.yaml and redirects files).
- MySQL 8 is the only supported database in production; `ghost config database.client` prints `sqlite3` or `mysql`.
- Review breaking changes: Ghost-CLI reports theme incompatibilities, or upload the theme to GScan. Ghost 6.0 removed `?limit=all`, so integrations may need pagination.
- Then run `ghost update`. On failure try `ghost update --force`, or revert with `ghost update --rollback`; the most common failure cause is running out of memory, so have enough RAM or swap.

Which path: updates are recommended for sites running 3.0.0 or higher with MySQL in production, and development sites on any database. Web analytics is not compatible with Ghost-CLI; the Docker preview includes a migration tool for Ghost-CLI sites. Pre-1.0 sites have no direct update path to the latest version: update to 1.0 first by creating a brand new install (`ghost install --v1`) and importing the JSON backup from the Labs area of Ghost Admin, then follow the major update guide.

Lifecycle (from the LTS page): the current major receives new features and improvements; the previous major is LTS and only receives critical security and stability fixes. End-of-life dates in the table: 3.x Jan 2022, 4.x Jan 2023, 5.x Jan 2026, 6.x (current, released 2025) TBC. A version past end of life should be considered insecure.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, no imported snippets): update-major-version.mdx (199 lines), faq/major-versions-lts.mdx (26 lines), faq/update-0x.mdx (53 lines). Removed as unconfirmed by these pages: the claim that Node 22 is required "by the node versions page" (the update guide itself says to update when below 22), the statement that sites below 3.0 or on SQLite in production "should reinstall" (the page only says updates are recommended for 3.0+ with MySQL and for dev sites), and the Verify step with `ghost -v` showing the new major. Added backup contents, MySQL check, limit=all removal and rollback details.
Method: documentation only; no commands were run.
