---
id: computing-software.devops-ci-cd.gitea.cli-generate-and-config
name: cli-generate-and-config
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-generate-secret, gitea, gitea-cert, gitea-keys-command, gitea-dump-repo, gitea-restore-repo, internal-token, jwt-secret]
level: practitioner
status: docs-checked
description: "Gitea CLI helpers: generate secret (INTERNAL_TOKEN, JWT_SECRET, SECRET_KEY), cert self-signed TLS, keys for sshd AuthorizedKeysCommand, web flags, dump-repo."
sources: ["https://docs.gitea.com/administration/command-line/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea CLI helpers

## generate secret
`gitea generate secret INTERNAL_TOKEN|JWT_SECRET|SECRET_KEY` prints a value for `app.ini`. `JWT_SECRET` is the LFS and OAuth2 JWT secret (`LFS_JWT_SECRET` is kept as an alias). Useful in automated deployments.

## cert
`gitea cert --host git.example.com,example.com --ca` writes `cert.pem` and `key.pem` into the current directory, overwriting existing files. `--host` (required) takes hostnames and IPs, wildcards allowed. Options: `--ecdsa-curve` (P224, P256, P384, P521), `--rsa-bits` (default 3072, ignored when a curve is set), `--start-date`, `--duration` (default 8760h0m0s), `--ca`.

## keys (sshd AuthorizedKeysCommand)
```ini
AuthorizedKeysCommandUser git
AuthorizedKeysCommand /path/to/gitea keys -e git -u %u -t %t -k %k
```
The `-e` value and `AuthorizedKeysCommandUser` must match the user running Gitea. Also set `SSH_CREATE_AUTHORIZED_KEYS_FILE=false` in `[server]`. OpenSSH requires the program to be root-owned, not group/other writable, referenced by absolute path, and Gitea must be running.

## web
`gitea web [-p PORT] [--install-port N] [-P pidfile] [-q] [--verbose]` (default port 3000; `-p` overrides the config). Do not run as root; for ports below 1024 see `gitea-selinux` (setcap is lost on every upgrade).

## dump-repo / restore-repo
`gitea dump-repo --clone_addr URL --repo_dir DIR [--git_service git|github|gitea|gitlab] [--auth_username/--auth_password/--auth_token] [--owner_name] [--repo_name] [--units wiki,issues,labels,releases,release_assets,milestones,pull_requests,comments]` exports repository data; empty `--units` means all. `gitea restore-repo --repo_dir DIR --owner_name O --repo_name R [--units ...]` loads it back.

## Checked

2026-11-03: read https://docs.gitea.com/administration/command-line/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
