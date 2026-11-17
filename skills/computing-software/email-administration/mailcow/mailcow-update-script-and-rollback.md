---
id: computing-software.email-administration.mailcow.mailcow-update-script-and-rollback
name: mailcow-update-script-and-rollback
category: computing-software
field: email-administration
product: mailcow
tags: [update-sh, update-channels, nightly-updates, legacy-branch, rollback, update-hooks, release-cycle]
level: practitioner
status: docs-checked
description: "Update mailcow with update.sh, choose stable, legacy or nightly branches, inspect pre-update commits and roll back with git checkout."
sources: ["https://docs.mailcow.email/maintenance/update/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Updating and rolling back mailcow

Run `./update.sh` from the mailcow-dockerized directory. It reports merge errors and auto-corrects some minor conflicts in favour of the upstream code. Useful options (combinable): `--check` shows pending changes, `--skip-start` does not start mailcow afterwards, `--skip-ping-check` skips the ICMP check, `--prefetch` only pulls images, `--gc` cleans old image tags, `--force` runs unattended but unsupported, and `--ours` resolves conflicts in favour of local changes (discouraged).

Branches: `--stable` (master, default) gets at least one release a month, numbered `YYYY-MM` with revisions `a`, `b`, `c`. `--legacy` follows the 2025-02 release with security fixes only; support ends February 2026. `--nightly` is unstable and for testing only; the docs say it is not suitable for production and recommend testing it on a second machine made with the cold standby script, after a backup.

Each update makes a git commit named "Before update on <date>". Find them with `git log --pretty=oneline | grep -i "before update"` and compare with `git diff <commit>`.

Rollback: `docker compose down`, `git checkout <commit>`, `docker compose pull`, `docker compose up -d`.

The update page names `pre_commit_hook.sh` and `post_commit_hook.sh` as hook scripts in the mailcow root, while the dedicated hooks guide names `pre_update_hook.sh` (runs on every `update.sh` call) and `post_update_hook.sh` (runs only after a successful update); check which your release honours.

## Checked

2026-11-04. Confirmed on the Update page and the update-hooks page: update.sh options (--check, --skip-start, --skip-ping-check, --prefetch, --gc, --force, --ours, --stable, --legacy, --nightly), conflict handling, stable/legacy/nightly descriptions and the 2025-02 legacy base with support ending February 2026, YYYY-MM release numbering with a/b/c revisions, the "Before update" git log search, the checkout rollback sequence, and the two differing hook-name pairs. Fixed: nightly wording now matches the page (not for production; test on a second machine).

Method: documentation only; no commands were run.
