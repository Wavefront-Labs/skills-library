---
id: computing-software.cloud-infrastructure-engineering.saltstack.gitfs-refresh-on-push
name: gitfs-refresh-on-push
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, gitfs, post-receive, reactor, fileserver-update, update-interval]
level: advanced
status: docs-checked
description: "Refresh Salt GitFS immediately on git push using a post-receive hook that fires a Salt event and a reactor running runner.fileserver.update."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/tutorials/gitfs.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refresh GitFS on push

By default remotes refresh every 60 seconds (`gitfs_update_interval`).

For faster updates the git server must also be a Salt minion. Three steps:
1. On the master, create `/srv/reactor/update_fileserver.sls` containing `update_fileserver:` with `runner.fileserver.update` under it.
2. In the master config map an event tag to it: `reactor:` then `- 'salt/fileserver/gitfs/update':` then `- /srv/reactor/update_fileserver.sls`.
3. On the git server add a post-receive hook: `salt-call event.fire_master update salt/fileserver/gitfs/update`.

If other git users push, run the hook with `sudo -u root salt-call ...` and add a sudoers policy (a `Cmnd_Alias` for that exact command, `Defaults!... !requiretty`, `ALL ALL=(root) NOPASSWD:`) on the git server. Use the user the minion runs as in place of `root`. The `update` data argument is ignored, and the tag can be any string if used consistently.

## Checked

2026-11-09. Read in full the Salt Git Fileserver Backend Walkthrough (doc/topics/tutorials/gitfs.rst, master branch): Refreshing gitfs Upon Push. Added the reactor files, hook and sudo details the page gives.

Method: documentation only; no commands were run.
