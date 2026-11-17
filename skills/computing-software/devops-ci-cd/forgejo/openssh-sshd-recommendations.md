---
id: computing-software.devops-ci-cd.forgejo.openssh-sshd-recommendations
name: openssh-sshd-recommendations
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [sshd-config, git-protocol-v2, per-source-penalties, openssh]
level: advanced
status: docs-checked
description: "Configure OpenSSH for the git user: pass GIT_PROTOCOL and disable per-source penalties behind a proxy."
sources:
  - https://forgejo.org/docs/latest/admin/setup/recommendations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
These apply when SSH is enabled (the default) and the host sshd from OpenSSH is used, which is Forgejo's recommended practice; they do not apply to the built-in SSH server (`[ssh].START_SSH_SERVER = true`). Scope each setting to the git user, or to whatever `[ssh].SSH_USER` is set to, with a `Match User git` block in sshd_config.

Git wire protocol v2: Git announces support for the newer protocol over SSH, but OpenSSH does not pass the environment by default. Add `AcceptEnv GIT_PROTOCOL` inside the Match block.

Per source penalties: since OpenSSH 9.8, sshd penalizes source IPs that misbehave. If SSH connections go through a reverse proxy, sshd only sees the proxy address, so enough bad behavior from one attacker can block all incoming SSH connections, including legitimate users. The recommendation is `PerSourcePenalties no`. To keep the feature, the client IP must reach sshd; sshd does not support the PROXY protocol, so you would need mmproxy (go-mmproxy and mmproxy-rs are preferred over Cloudflare's) or transparent proxying, both of which need firewall changes, and the latter kernel parameter changes.

## Checked

2026-11-04. Confirmed against the Forgejo Recommended Settings and Tips page (OpenSSH recommendations): applicability, Match User git scoping, AcceptEnv GIT_PROTOCOL, OpenSSH 9.8 per source penalties, PerSourcePenalties no, and the mmproxy and transparent proxy options. Removed: the restart-sshd sentence, not on the page.

Method: documentation only; no commands were run.
