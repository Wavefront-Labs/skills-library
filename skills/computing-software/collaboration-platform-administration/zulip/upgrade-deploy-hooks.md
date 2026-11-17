---
id: computing-software.collaboration-platform-administration.zulip.upgrade-deploy-hooks
name: upgrade-deploy-hooks
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [pre-deploy-hooks, post-deploy-hooks, hook-files, upgrade-automation]
level: advanced
status: docs-checked
description: "Write custom Zulip upgrade hooks in /etc/zulip/pre-deploy.d and post-deploy.d with .hook files, environment variables for old and new version and commit, and abort behaviour."
sources: ["https://zulip.readthedocs.io/en/latest/production/upgrade.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom upgrade hooks

Zulip upgrades can run arbitrary actions just before and just after the critical period when the server restarts. Place files ending in `.hook` in:

- `/etc/zulip/pre-deploy.d`
- `/etc/zulip/post-deploy.d`

They run from the working directory of the new version, in alphabetical order. If any hook exits non-zero the upgrade aborts.

Environment variables available:

- `ZULIP_OLD_VERSION`: the version upgrading from, either a release name such as `10.0` or `10.0-beta1`, or `git describe` output such as `10.0-beta1-2-abcd158b18f2`.
- `ZULIP_NEW_VERSION`: the target, in the same format.

For upgrades between Git versions these are also set:

- `ZULIP_OLD_COMMIT` and `ZULIP_NEW_COMMIT`: full commit hashes.
- `ZULIP_OLD_MERGE_BASE_COMMIT` and `ZULIP_NEW_MERGE_BASE_COMMIT`: the merge-base of each version with the public branch of the upstream repository, meaning the closest commit in standard Zulip Server.

Zulip also ships ready-made hooks, enabled through Puppet classes in `zulip.conf`, for posting an upgrade message to a channel and for creating Sentry releases; see the deployment documentation.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/upgrade.html (zulip.readthedocs.io, latest). Removed: 'executable' file requirement and the advice paragraph on guard checks.

Method: documentation only; no commands were run.
