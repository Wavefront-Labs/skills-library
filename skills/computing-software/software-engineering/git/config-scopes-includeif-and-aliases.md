---
id: computing-software.software-engineering.git.config-scopes-includeif-and-aliases
name: config-scopes-includeif-and-aliases
category: computing-software
field: software-engineering
product: git
tags: [git, git-config, git-config-scopes, includeif, git-aliases, dotfiles]
level: practitioner
status: verified
description: "Manage Git configuration across system, global, local and worktree scopes, switch identities with includeIf, and write useful aliases."
sources:
  - https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Git config scopes, includeIf and aliases

**Goal:** correct identity and behaviour per context (work vs personal repos), discoverable settings, and time-saving aliases.

## 1. Scopes and precedence (later wins)
| Scope | File | Flag |
|---|---|---|
| system | `$(prefix)/etc/gitconfig` | `--system` |
| global | `~/.gitconfig` or `~/.config/git/config` | `--global` |
| local | `.git/config` | `--local` (default when writing in a repo) |
| worktree | `$GIT_DIR/config.worktree` (`.git/config.worktree` in the main worktree, `.git/worktrees/<n>/config.worktree` in linked ones) | `--worktree` (needs `extensions.worktreeConfig`) |
| command | `git -c key=value`, `GIT_CONFIG_COUNT/KEY_n/VALUE_n` env | |

```bash
git config --list --show-origin --show-scope   # where every value comes from
git config --get-all remote.origin.fetch       # multi-valued keys
git config --unset-all core.hooksPath
```

## 2. includeIf for identity per directory
```ini
# ~/.gitconfig
[user]
    name = Ana Ruiz
    email = ana@personal.example
[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work
[includeIf "hasconfig:remote.*.url:git@github.com:corp/**"]
    path = ~/.gitconfig-work
```
```ini
# ~/.gitconfig-work
[user]
    email = ana.ruiz@corp.example
    signingkey = ~/.ssh/id_work.pub
[core]
    sshCommand = ssh -i ~/.ssh/id_work -o IdentitiesOnly=yes
```
- `gitdir:` needs a trailing `/` to match everything below; `gitdir/i:` is case-insensitive (use on Windows/macOS).
- `onbranch:release/**` conditions on the current branch; `hasconfig:remote.*.url:<glob>` matches on remote URL. Both `gitdir:` and `hasconfig:` forms were run and applied the included file. Use absolute paths (on Git for Windows a drive-letter path form worked where `/c/...` did not).

## 3. Aliases
```ini
[alias]
    st = status -sb
    lg = log --graph --oneline --decorate --all
    undo = reset --soft HEAD~1
    amend = commit --amend --no-edit
    fixup = "!f() { git commit --fixup=$1 && GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash $1~1; }; f"
    who = shortlog -sne
```
`!` aliases run in a shell from the repo root (`GIT_PREFIX` holds the original subdirectory).

## 4. Settings worth having globally
```ini
[init]   defaultBranch = main
[pull]   rebase = true          # or ff = only
[push]   autoSetupRemote = true
[fetch]  prune = true
[rerere] enabled = true
[diff]   algorithm = histogram
[merge]  conflictStyle = zdiff3
```

## Gotchas
- Repo-shared settings cannot be committed via `.git/config`; commit a file and ask users to `git config include.path ../.gitconfig`.
- Aliases cannot override built-in commands.
- `includeIf gitdir` uses the real path; symlinked directories may not match.

## Verify
- In a work repo, `git config user.email` and `git config --show-origin user.email` show the work address from the included file.
