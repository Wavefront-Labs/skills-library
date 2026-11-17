---
id: computing-software.cloud-infrastructure-engineering.saltstack.gitfs-enable-and-providers
name: gitfs-enable-and-providers
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, gitfs, fileserver-backend, gitfs-remotes, pygit2, gitpython, gitcli]
level: practitioner
status: docs-checked
description: "Enable the Salt GitFS backend: fileserver_backend and gitfs_remotes, provider choice (pygit2, GitPython, gitcli), remote search order and masterless use."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/tutorials/gitfs.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling GitFS

Master config: add `gitfs` to `fileserver_backend` and list one or more repositories in `gitfs_remotes`. Remotes may use `git://`, `https://`, `file://`, `ssh://` or scp-style syntax. Restart the master; minions need no repo access because the master caches the files.

Providers: pygit2, GitPython, and `gitcli` (added in 3008.0). If `gitfs_provider` is unset Salt tries them in that order. `gitcli` needs only git 2.3.0+, has no submodule support and clones with `--depth 1`. pygit2 is sensitive to libgit2 version mismatches, so pin it.

Lookup: remotes are searched in listed order and the first match is served. A requested state file beats a directory containing `init.sls`. Backends are searched in the order they appear in `fileserver_backend`, so with `roots` then `git`, files under `/srv/salt` win over any git remote.

Masterless (since 2014.7.0): put the GitFS settings and `fileserver_backend` in the minion config instead of the master config.

GitPython's authors advise against it for long-running processes such as a master; Salt mitigates leaks by restarting the fileserver worker every `fileserver_interval`.

## Checked

2026-11-09. Read in full the Salt Git Fileserver Backend Walkthrough (doc/topics/tutorials/gitfs.rst, master branch): Installing Dependencies, Simple Configuration, Multiple Remotes, gitfs alongside other backends, masterless mode. Corrected the backend search-order and masterless wording.

Method: documentation only; no commands were run.
