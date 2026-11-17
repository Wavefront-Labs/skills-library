---
id: computing-software.software-engineering.git.ssh-keys-and-multiple-git-accounts
name: ssh-keys-and-multiple-git-accounts
category: computing-software
field: software-engineering
product: git
tags: [git, ssh-config-git, multiple-git-accounts, ssh-keys, core-sshcommand, ssh-agent, deploy-keys]
level: practitioner
status: docs-checked
description: "Set up SSH keys for Git hosts and use several accounts on one host via ~/.ssh/config host aliases, core.sshCommand or includeIf, and debug 'Permission denied (publickey)'."
sources:
  - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
  - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection
  - https://docs.github.com/en/authentication/troubleshooting-ssh/using-ssh-over-the-https-port
  - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys
  - https://git-scm.com/docs/git-config
  - https://github.com/openssh/openssh-portable/blob/master/ssh_config.5
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH keys and multiple Git accounts

**Goal:** push to work and personal accounts on the same host without the wrong key
being offered first.

## Create and load a key
```bash
ssh-keygen -t ed25519 -C "jane@work.example" -f ~/.ssh/id_ed25519_work
ssh-add ~/.ssh/id_ed25519_work            # macOS: ssh-add --apple-use-keychain
ssh -T git@github.com                     # "Hi <user>! You've successfully authenticated"
```
Upload the `.pub` file to the host. `core.sshCommand` (or the `GIT_SSH_COMMAND` environment variable, which overrides it) sets the command Git runs instead of `ssh`.

## Multiple accounts: host aliases
The host identifies your account by the key, so the first key the agent offers wins.
```
# ~/.ssh/config
Host github.com-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
    IdentitiesOnly yes
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
    IdentitiesOnly yes
```
Clone with the alias: `git clone git@github.com-work:acme/api.git`. Fix an existing
repo: `git remote set-url origin git@github.com-work:acme/api.git`.
`IdentitiesOnly yes` makes `ssh` use only the identity files configured for the host (per ssh_config(5)) rather than also offering every key held by the agent.

## Alternative: per-directory config
```ini
# ~/.gitconfig
[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work
# ~/.gitconfig-work
[user]
    email = jane@work.example
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519_work -o IdentitiesOnly=yes
```
This also fixes the commit email per directory, which aliases alone do not.
One-off: `GIT_SSH_COMMAND="ssh -i ~/.ssh/key -o IdentitiesOnly=yes" git clone ...`.

## Debugging
```bash
ssh -vT git@github.com-work
```
The verbose output shows which identity files `ssh` tries for that alias.
- `Permission denied (publickey)`: key not uploaded, wrong alias, or agent not running.
- Authenticated as the wrong user: another key offered first; add `IdentitiesOnly`.
- Port 22 blocked: GitHub serves SSH on host `ssh.github.com` port 443 (`ssh -T -p 443 git@ssh.github.com`).
- `~/.ssh/config` must be read/write for you and not writable by others (`chmod 600 ~/.ssh/config`).

## Deploy keys and CI
A GitHub deploy key cannot be reused across repositories; for many repositories on one server GitHub's docs describe SSH agent forwarding, machine users or a GitHub App instead.

## Verify
- [ ] `ssh -T` for each alias greets the expected account.
- [ ] `git config user.email` inside each workspace shows the matching identity.

## Checked

Checked 2026-10-25 against the github/docs repository (main), the Git config manual (git/git master, latest commit 2026-10-22) and the OpenSSH `ssh_config.5` source. Confirmed: `ssh-keygen -t ed25519 -C`, `ssh-add --apple-use-keychain` (GitHub docs), the `ssh -T git@github.com` success message, SSH over port 443 on `ssh.github.com`, deploy keys not reusable across repositories (machine user, GitHub App alternatives), `core.sshCommand` and `GIT_SSH_COMMAND` precedence, `includeIf "gitdir:..."`, `IdentitiesOnly` semantics, strict permissions required for `~/.ssh/config`. Removed as unconfirmed: the Windows agent service and `ssh.exe` advice, the exact `Too many authentication failures` and `Bad owner or permissions` messages and the `grep` filter on verbose output.

Method: documentation only; no commands were run.
