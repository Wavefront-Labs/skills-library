---
id: computing-software.software-engineering.git.safe-directory-and-dubious-ownership
name: safe-directory-and-dubious-ownership
category: computing-software
field: software-engineering
product: git
tags: [git, safe-directory, dubious-ownership, cve-2022-24765, ci-containers, file-ownership]
level: practitioner
status: docs-checked
description: "Fix 'detected dubious ownership in repository' correctly: why Git checks owners, safe.directory scoping, container/CI volume mounts, and Windows network or external drives."
sources:
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/docs/git-init
  - https://github.com/git/git/blob/master/Documentation/RelNotes/2.35.2.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# safe.directory and dubious ownership

**Goal:** make Git work in repos owned by another user without disabling a real
security check everywhere.

## Why the error exists
Since Git 2.35.2 (CVE-2022-24765), Git refuses to use a repository whose directory is
owned by a different user than the one running Git: by default it will not even parse the
config of a repository owned by someone else, let alone run its hooks, because that config
could otherwise make Git run attacker-chosen commands as you. Message:
```
fatal: detected dubious ownership in repository at '/work/app'
To add an exception for this directory, call:
    git config --global --add safe.directory /work/app
```

## Fix in order of preference
1. **Fix ownership** so the repo belongs to the user running Git:
   `sudo chown -R "$(id -u):$(id -g)" /work/app`, or run the container as the host UID
   (`docker run --user "$(id -u):$(id -g)" ...`).
2. **Trust that one path:**
   `git config --global --add safe.directory /work/app`
   Only protected configuration (the system, global and command scopes) is honoured for
   this key; a repo-local setting is ignored by design. It is multi-valued, accepts
   `~/<path>` and `%(prefix)/<path>`, and a path with `/*` appended trusts every
   repository under that directory. An empty value resets the list.
3. **Ephemeral CI/container only:** `git config --global --add safe.directory '*'`
   (completely opts out of the check). Acceptable inside a throwaway build container;
   never on a multi-user host.

## Common situations
- **Docker bind mounts:** files owned by host UID 1000, container runs as root. Mount
  and run as the same UID, or add the specific path.
- **CI steps running as a different user than the checkout:** add the specific workspace
  path with `git config --global --add safe.directory <path>` rather than `'*'`.
- **sudo git ...**: running as root in a user's repo. Don't; if unavoidable, on non-Windows
  platforms with sudo, Git also trusts the uid recorded in `SUDO_UID` in addition to
  root's (remove `SUDO_UID` from root's environment to trust only root-owned repos).

## Verify
- [ ] `git config --show-origin --get-all safe.directory` lists only intended paths.
- [ ] `stat -c '%U' .git` matches `whoami` where possible.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22). Confirmed in config/safe: default refusal to parse another owner's repository config or run its hooks; `safe.directory` is multi-valued, an empty value resets it, `*` opts out, `/*` suffix trusts all repositories below a directory, `~/` and `%(prefix)/` interpolation, honoured only in protected configuration (system, global, command scopes, per git-config); `SUDO_UID` handling when running as root under sudo; Git 2.35.2 release notes reference CVE-2022-24765. Removed as unconfirmed: the `core.fsmonitor` / `core.pager` examples, the GitHub Actions `actions/checkout` behaviour, the Windows network-share and FAT/exFAT remarks with the UNC `%(prefix)` recipe, and the Git version for `SUDO_UID` handling.

Method: documentation only; no commands were run.
