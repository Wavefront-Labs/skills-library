---
id: computing-software.devops-ci-cd.earthly.earthly-git-auth-ssh-https
name: earthly-git-auth-ssh-https
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, git-auth, ssh-auth-sock, ssh-agent, https, netrc, git-clone, strict-host-key-checking]
level: practitioner
status: docs-checked
description: "Configure Git authentication for earthly remote targets and GIT CLONE using the SSH agent socket, https user and password in config, auto mode and the netrc fallback."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/auth.md
  - https://github.com/earthly/earthly/blob/main/docs/earthly-config/earthly-config.md
  - https://github.com/earthly/earthly/blob/main/docs/earthly-command/earthly-command.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Git authentication for earthly

Goal: let remote target references and `GIT CLONE` reach private repositories. This is not for secrets inside your own commands; use `RUN --secret` for those.

## Auto mode (default)
`auth` defaults to `auto`: ssh is used when ssh-agent is running with at least one key loaded, otherwise earthly falls back to https. If a private repo fails over ssh, make sure `SSH_AUTH_SOCK` is set (start an agent with `eval $(ssh-agent)`) and add the key with `ssh-add <path to key>`.

## SSH agent socket
Earthly mounts the socket from `SSH_AUTH_SOCK` into the BuildKit container (on Mac, Docker's compatibility socket `/run/host-services/ssh-auth.sock` is the default). Override with `EARTHLY_SSH_AUTH_SOCK` or `--ssh-auth-sock <path-to-sock>`. Force ssh for one site:
```yaml
git:
    git.example.com:
        auth: ssh
        user: git
```

## Username and password
```yaml
git:
    github.com:
        auth: https
        user: <username>
        password: <password>
```
If no `user` or `password` is found, earthly checks `~/.netrc`. The `GIT_USERNAME` and `GIT_PASSWORD` env vars override all host entries but are deprecated in favour of the config file.

## Other site options
`strict_host_key_checking` (on by default; ssh only; rather than disabling it, record the key with `ssh-keyscan <hostname> >> ~/.ssh/known_hosts`), `ssh_command`, `port`, `prefix`, `pattern`, `substitute`.

## Debugging
Run `earthly --verbose` to see how a remote reference is turned into a git URL. For low-level BuildKit git debugging add to the config:
```yaml
global:
  buildkit_additional_args: [ '-e', 'BUILDKIT_DEBUG_GIT=1' ]
```
BuildKit logs: `docker logs earthly-buildkitd`.

## Gotcha
If a host is reachable only over HTTP, earthly refuses to send credentials.

## Checked

2026-11-07. Read docs/guides/auth.md in full. Read only the git section (around lines 230-302 and the global section) of earthly-config.md and the --ssh-auth-sock entry of earthly-command.md rather than those pages in full. Auth modes, SSH agent socket, netrc, strict_host_key_checking default and ssh-keyscan, ssh_command, port, prefix, pattern and substitute all match. Nothing removed.
Method: documentation only; no commands were run.
