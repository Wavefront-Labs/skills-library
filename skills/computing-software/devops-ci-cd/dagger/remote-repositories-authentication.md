---
id: computing-software.devops-ci-cd.dagger.remote-repositories-authentication
name: remote-repositories-authentication
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, remote-repositories, git, ssh, https, authentication, ssh-agent, private-repos]
level: practitioner
status: docs-checked
description: "Reference remote Git directories, files and modules in Dagger over HTTPS or SSH, forward the SSH agent socket, and work around known SSH limitations."
sources: [https://docs.dagger.io/0.21/extending/remote-repositories]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote Git repositories and authentication in Dagger

Goal: pull private or public repositories into directory, file and module arguments. Works with GitHub, GitLab, BitBucket, Azure DevOps, Codeberg and Sourcehut. Dagger 0.21 docs.

## Reference schemes (directory and file arguments)
| Protocol | Scheme | Auth | Example |
|---|---|---|---|
| HTTP(S) | Git HTTP | Git credential manager | `https://github.com/username/repo.git[#version[:subpath]]` |
| SSH | explicit | SSH keys | `ssh://git@github.com/username/repo.git[#version[:subpath]]` |
| SSH | SCP-like | SSH keys | `git@github.com:username/repo.git[#version[:subpath]]` |

- `#version` is a tag, branch or full commit hash; default branch if omitted.
- `:subpath` selects a subdirectory; a version is mandatory when a subpath is used.
- For modules use `@version` and `/subpath` instead. The directory scheme is under discussion upstream and may change.

## Two SSH cloning patterns
1. Pre-resolve to a `Directory` at the top-level call: `dagger call clone --dir git@github.com:private/secret-repo#main`. The module never touches your SSH agent.
2. Pass the agent socket so the function clones itself: `dagger call clone-with-ssh --repository git@github.com:private/secret-repo.git --ref main --sock "$SSH_AUTH_SOCK"`. The caller explicitly approves credential use. The linked cookbook snippet (not this page) does this in Go with a `*dagger.Socket` argument: `dag.Git(repository, dagger.GitOpts{SSHAuthSocket: sock}).Ref(ref).Tree()`.

## HTTPS
Dagger uses your configured Git credential manager (Git Credential Manager, macOS Keychain, Windows Credential Manager, or helpers in `.gitconfig`). Check with `git clone https://github.com/USER/PRIVATE_REPOSITORY.git`; if it works, Dagger can too. Provider setup: GitHub `gh auth login`; GitLab `glab auth login`; Azure DevOps via Git Credential Manager; BitBucket via the git credential system.

## SSH
Dagger mounts the socket in `SSH_AUTH_SOCK` into the engine. It is needed for SSH refs even for public repositories, because most servers use your key for authentication and tracking. Make sure the variable is set and keys are loaded in the agent.

## Known limitations
- SSH refs are supported on Linux and macOS; Windows is not supported yet.
- Multiple keys in the agent may break SSH forwarding. Workaround: `ssh-add -D`, then `ssh-add /path/to/key` for only the needed key.

Related: module-dependencies-install-update, cookbook-filesystems-directories-files.

## Checked

2026-11-07

Read extending/modules/remote-repositories.mdx in full (live slug /extending/remote-repositories matches the cited URL; the page has no snippet includes). Also read the cookbook snippet clone-git-repository-ssh/go/main.go that the page links, to confirm the Go SSHAuthSocket example; the cookbook filesystems page itself and the other language snippets were not opened. Confirmed the reference scheme table, the note that the scheme may change, #version and :subpath rules, both SSH cloning patterns and their commands, the supported credential helpers and git clone check, the provider setup commands, SSH_AUTH_SOCK behaviour, and both known limitations with the ssh-add workaround. Only the attribution of the Go example was changed.

Method: documentation only; no commands were run.
