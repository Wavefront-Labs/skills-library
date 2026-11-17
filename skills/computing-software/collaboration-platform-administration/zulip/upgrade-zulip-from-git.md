---
id: computing-software.collaboration-platform-administration.zulip.upgrade-zulip-from-git
name: upgrade-zulip-from-git
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [upgrade-from-git, upgrade-zulip-from-git, git-repo-url, maintenance-branch]
level: advanced
status: docs-checked
description: "Upgrade a Zulip production server to a Git branch or tag with upgrade-zulip-from-git, including main, maintenance and cloud branches and a custom git_repo_url."
sources: ["https://zulip.readthedocs.io/en/latest/production/upgrade.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrading Zulip from Git

Zulip can upgrade a production install to any commit of a Git repository. That gets unreleased fixes and features, or supports maintaining a fork. Docker deployments have separate instructions.

Run from the current deployment:

```
~zulip/deployments/current/scripts/upgrade-zulip-from-git 11.5      # an official release
~zulip/deployments/current/scripts/upgrade-zulip-from-git 11.x      # a maintenance branch
~zulip/deployments/current/scripts/upgrade-zulip-from-git zulip-cloud-current
~zulip/deployments/current/scripts/upgrade-zulip-from-git main
```

Zulip fetches the relevant commit itself. On top of the normal release-upgrade steps, it also builds the frontend assets with `webpack`.

Which branch to choose is described in the release lifecycle notes on Git versions. For `main`, read the project's guidance on upgrading to `main`; for a single fix, you can apply a small change from `main` instead of moving the whole server.

To use a repository other than upstream, add to `/etc/zulip/zulip.conf`:

```
[deployment]
git_repo_url = https://github.com/zulip/zulip.git
```

Replace the URL with your fork's.

Memory warning: on hosts with minimal RAM the `tools/webpack` step can run out of memory during `upgrade-zulip-from-git`. Free RAM by stopping the server with `./scripts/stop-server` before upgrading.

Deployment hooks receive extra commit variables for Git upgrades.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/upgrade.html (zulip.readthedocs.io, latest). Removed: the unsupported 'run as root' wording for upgrade-zulip-from-git.

Method: documentation only; no commands were run.
