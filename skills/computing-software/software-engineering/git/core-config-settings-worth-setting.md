---
id: computing-software.software-engineering.git.core-config-settings-worth-setting
name: core-config-settings-worth-setting
category: computing-software
field: software-engineering
product: git
tags: [git, pull-rebase, init-default-branch, core-editor, core-excludesfile, git-config, rerere-enabled]
level: practitioner
status: verified
description: "The Git settings worth configuring on a new machine: identity, editor, default branch, pull.rebase, excludes, rerere, autostash and diff defaults."
sources: ["https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration", "https://git-scm.com/docs/git-config", "https://blog.gitbutler.com/how-git-core-devs-configure-git/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Core config settings worth setting

**Goal:** a deliberate `~/.gitconfig` instead of defaults chosen for backward compatibility.

## Baseline
```bash
git config --global user.name "Jane Doe"
git config --global user.email jane@example.org
git config --global user.useConfigOnly true      # never guess identity from hostname
git config --global init.defaultBranch main
git config --global core.editor "code --wait"    # or vim, nano; must block until closed
git config --global core.excludesFile ~/.gitignore_global   # .DS_Store, .idea/, *.swp
```

## Pull, fetch, push
```bash
git config --global pull.rebase true          # or pull.ff only; silences the divergent-branches hint
git config --global rebase.autoStash true     # stash/unstash dirty tree around rebase
git config --global fetch.prune true
git config --global push.autoSetupRemote true
git config --global push.followTags true      # push annotated tags reachable from pushed commits
```
`pull.rebase true` rewrites your local unpushed commits on top of upstream instead of
creating merge bubbles. Teams wanting zero surprises pick `pull.ff only` and rebase
explicitly.

## Merge, diff, rebase quality of life
```bash
git config --global merge.conflictStyle zdiff3   # shows base in conflicts
git config --global rerere.enabled true          # remember conflict resolutions
git config --global diff.algorithm histogram
git config --global diff.colorMoved zebra
git config --global rebase.updateRefs true       # move stacked branch pointers
git config --global rebase.autoSquash true       # honour fixup! commits
git config --global branch.sort -committerdate
git config --global tag.sort version:refname
git config --global help.autocorrect prompt     # other values: show (default), never, 1, <deciseconds>
```

## Inspect and debug config
```bash
git config --list --show-origin --show-scope     # where every value comes from
git config --get-all safe.directory
git -c pull.rebase=false pull                     # one-off override
```
Precedence: command line > worktree > local (`.git/config`) > global (`~/.gitconfig` or
`$XDG_CONFIG_HOME/git/config`) > system. `GIT_CONFIG_GLOBAL=/dev/null` isolates scripts from
personal settings.

## Gotchas
- `core.editor` that returns immediately (GUI without `--wait`) yields "Aborting commit due to empty commit message".
- `core.autocrlf` belongs in `.gitattributes` per repo, not global config (see line endings skill).
- Aliases cannot override built-in commands.

## Verify
- [ ] `git config --global --list` reviewed and committed to your dotfiles repo.
- [ ] `git pull` on a diverged branch behaves as you chose, without a hint message.
