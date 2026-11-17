---
id: computing-software.systems-network-administration.restic.init-repository
name: init-repository
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, init, repository, repository-version, local-backend]
level: intro
status: docs-checked
description: "Create a restic repository with restic init, choose the repository format version, and avoid CIFS and SMB for repository storage."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Initialise a repository

A repository is a directory of subdirectories and files holding backups, metadata and encryption keys. One repository can hold several keys.

```
restic init --repo /path/to/restic-repo
```

`-r` is the short form of `--repo`. You will be prompted for a password twice.

## Repository format version

`init --repository-version` takes `1`, `2` or `latest`.

- Version 1 works with any restic.
- Version 2 adds compression and is the current default.

Version 2 requires restic 0.14.0 or newer. See the upgrade-repo-format skill for migrating an existing repository.

## Avoid network filesystems

On Linux, avoid keeping a repository on CIFS/SMB or backing up from CIFS. The docs advise using another backend, or setting the environment variable `GODEBUG` to `asyncpreemptoff=1`, because of compatibility issues in older Linux kernels.

## Windows terminals

Password prompts can fail in MSYS2, Cygwin, Mintty and rxvt. Run through `winpty`:

```
winpty restic -r /path/to/restic-repo init
```

Install it with `pacman -S winpty`.

`RESTIC_REPOSITORY` can hold the repository location so later commands need no `-r` flag.

## Checked

2026-11-03. Confirmed in the restic docs page Preparing a new repository (intro, Local, Password prompt on Windows, repository version table): repository contents and multiple keys, `--repository-version` with `latest`, version 2 needing 0.14.0 or newer and adding compression, the CIFS warning and `GODEBUG` workaround, `winpty` and `pacman -S winpty`. Removed: the claim that older binaries merely cannot read version 2 in unspecified builds.

Method: documentation only; no commands were run.
