---
id: computing-software.systems-network-administration.bash.managing-dotfiles-across-machines
name: managing-dotfiles-across-machines
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, dotfiles, chezmoi, gnu-stow, yadm, bare-git-repo, bashrc, config-management]
level: practitioner
status: draft
description: "Keep shell and tool dotfiles in git and deploy them to many hosts: bare repo, GNU stow symlink farms, chezmoi templates and secrets, and host-specific overrides."
sources:
  - https://www.chezmoi.io/user-guide/command-overview/
  - https://www.gnu.org/software/stow/manual/stow.html
  - https://www.atlassian.com/git/tutorials/dotfiles
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Managing dotfiles

## Option 1 — bare git repo (no tools)
```bash
git init --bare ~/.dotfiles
alias dot='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
dot config status.showUntrackedFiles no
dot add ~/.bashrc ~/.vimrc ~/.tmux.conf && dot commit -m init && dot push
# new machine:
git clone --bare <url> ~/.dotfiles && dot checkout   # move conflicting files away first
```
## Option 2 — GNU stow (symlink farm per package)
```
~/dotfiles/bash/.bashrc
~/dotfiles/vim/.vimrc
~/dotfiles/tmux/.tmux.conf
```
```bash
cd ~/dotfiles && stow -v bash vim tmux      # symlinks into $HOME (target = parent dir by default)
stow -n -v bash                             # dry run; conflicts with real files abort
stow -D vim                                 # remove links
```
## Option 3 — chezmoi (templates, secrets, many hosts)
```bash
chezmoi init <git-url> ; chezmoi add ~/.bashrc ; chezmoi edit ~/.bashrc
chezmoi diff ; chezmoi apply -v
```
Templates (`dot_gitconfig.tmpl`) with `{{ if eq .chezmoi.hostname "work01" }}`, password-manager lookups
(`{{ (bitwarden "item" "x").login.password }}`), `.chezmoiignore` per OS.

## Host-specific overrides (any method)
End `.bashrc` with `[ -r ~/.bashrc.local ] && . ~/.bashrc.local`; keep `.local` files out of git.

## Gotchas
- Never commit private keys/tokens; scan with `git secrets`/`gitleaks`.
- Servers you share with others: dotfiles are personal — don't stow into service accounts.
- Symlinked `.ssh/config` must still be mode 600 on the target file.

## Verify
- [ ] Fresh VM: one clone + apply command yields a working shell with no errors on login.
