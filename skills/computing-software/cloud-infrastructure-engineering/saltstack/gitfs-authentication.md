---
id: computing-software.cloud-infrastructure-engineering.saltstack.gitfs-authentication
name: gitfs-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, gitfs, authentication, ssh, https, gitlab, known-hosts]
level: advanced
status: docs-checked
description: "Authenticate Salt GitFS remotes per provider (pygit2, GitPython, gitcli), choose GitLab token types, and register SSH host keys in known_hosts."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/tutorials/gitfs.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitFS authentication

- **pygit2:** HTTPS with user and password; SSH with public key, private key and optional passphrase. Plain HTTP needs `insecure_auth`.
- **GitPython:** HTTPS credentials in the URL or in `/var/lib/salt/.netrc`; SSH only with passphraseless keys. The pygit2 `pubkey`/`privkey` options do not work. The key must be `~/.ssh/id_rsa` (mode 0600) of the user running the master, or chosen with an `IdentityFile` entry in `~/.ssh/config`.
- **gitcli (3008.0+):** auth goes through environment variables for `ssl_verify`, `proxy` and `privkey` only. `user`, `password`, `passphrase`, `pubkey` and `insecure_auth` are silently ignored: embed credentials in the URL or use a git credential helper. With a `privkey` it runs ssh with `StrictHostKeyChecking=no`, so use it only with trusted endpoints.
- **GitLab:** prefer deploy tokens (read-only), then project access tokens, then personal access tokens; deploy keys over SSH also work. Expired tokens or missing scopes give 401 errors.
- **Host keys:** pygit2 and GitPython SSH remotes need the host key in `~/.ssh/known_hosts` of the master's user, added with `ssh.set_known_host` (for example `salt-call --local ssh.set_known_host hostname=gitlab.example.com`) or by connecting once with `ssh` as that user. Verify the fingerprint, for example with `ssh-keyscan` plus `ssh-keygen -l`; setting `StrictHostKeyChecking no` for GitPython works but is not recommended.

## Checked

2026-11-09. Read in full the Salt Git Fileserver Backend Walkthrough (doc/topics/tutorials/gitfs.rst on the master branch): Authentication (pygit2, GitPython, gitcli, GitLab, known_hosts) sections. Added the provider-specific limits the page states; removed nothing unsupported.

Method: documentation only; no commands were run.
