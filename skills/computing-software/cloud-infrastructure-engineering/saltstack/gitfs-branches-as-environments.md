---
id: computing-software.cloud-infrastructure-engineering.saltstack.gitfs-branches-as-environments
name: gitfs-branches-as-environments
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, gitfs, saltenv, branches, whitelist, blacklist, top-file]
level: advanced
status: docs-checked
description: "Map Git branches and tags to Salt environments with GitFS, filter with saltenv whitelist/blacklist, and avoid top file conflicts across branches."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/tutorials/gitfs.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitFS branches as environments

- Branches and tags map to saltenvs by name; `master` maps to `base`. To use another branch as `base`, set `gitfs_base` (also available per remote).
- Filter exposed refs with `gitfs_saltenv_whitelist` and `gitfs_saltenv_blacklist` (exact names, globs or regexes, evaluated in that order; omit `^` and `$`, the regex must match the whole name). Whitelist only: just matches are exposed. Blacklist only: matches are hidden. Both: in the whitelist and not in the blacklist.
- Top files from every branch merge during highstate, and the same SLS file in several branches gives a compile error (conflicting IDs). To avoid it: use `{{ saltenv }}` in place of the environment name in top.sls, set `top_file_merging_strategy: same` in the minion config, and set `saltenv` explicitly, either in the minion config or at runtime (`salt myminion state.apply saltenv=dev`, which overrides the config value).
- Promotion: branch qa off master and dev off qa, then merge dev into qa and qa into master.

Related: since 2018.3.0 `gitfs_update_interval` sets the refresh rate independent of `loop_interval` (60 seconds by default; `update_interval` per remote).

## Checked

2026-11-09. Read in full the Salt Git Fileserver Backend Walkthrough (doc/topics/tutorials/gitfs.rst, master branch): Branches, Environments and Top Files, Environment Whitelist/Blacklist, Update Intervals. Nothing removed.

Method: documentation only; no commands were run.
