---
id: computing-software.systems-network-administration.patch-management.reprepro-local-apt-repository
name: reprepro-local-apt-repository
category: computing-software
field: systems-network-administration
product: patch-management
tags: [reprepro, local-apt-repository, deb-repository, patch-acquisition, debian, ubuntu]
level: practitioner
status: docs-checked
description: "Build a signed local apt repository with reprepro: conf/distributions, includedeb, update from upstream with filters, pulling between suites to stage patches."
sources:
  - https://manpages.debian.org/stable/reprepro/reprepro.1.en.html
  - https://manpages.debian.org/stable/apt/sources.list.5.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local apt repositories with reprepro

reprepro maintains a Debian-format repository: internal packages, a filtered upstream mirror, and staged suites (`testing` -> `stable`) via `pull`.

## Layout
```text
/srv/repo/conf/distributions
/srv/repo/conf/updates
/srv/repo/conf/pulls
```
`conf/distributions`:
```text
Codename: jammy-staging
Components: main
Architectures: amd64 source
SignWith: 0xABCDEF0123456789
Update: ubuntu-security

Codename: jammy-prod
Components: main
Architectures: amd64 source
SignWith: 0xABCDEF0123456789
Pull: from-staging
```
`conf/updates`:
```text
Name: ubuntu-security
Method: http://archive.ubuntu.com/ubuntu
Suite: jammy-security
Components: main
Architectures: amd64
VerifyRelease: 871920D1991BC93C
FilterList: purge selected.list
```
`conf/pulls`:
```text
Name: from-staging
From: jammy-staging
```

## Commands
```sh
reprepro -b /srv/repo includedeb jammy-staging ./myagent_2.1_amd64.deb
reprepro -b /srv/repo update jammy-staging      # fetch filtered upstream
reprepro -b /srv/repo pull jammy-prod           # promote tested state
reprepro -b /srv/repo list jammy-prod openssl
reprepro -b /srv/repo export                    # regenerate signed indexes
```
Serve `/srv/repo/dists` and `/srv/repo/pool` with nginx.

Client:
```text
deb [signed-by=/etc/apt/keyrings/internal.gpg] https://repo.example.com jammy-prod main
```

## Gotchas
- `FilterList` takes a default action and a list file (`purge selected.list` drops every package not named in the file, in `dpkg --get-selections` style); only one entry per package is supported and dependencies are not resolved for you.
- `SignWith` accepts `yes`/`default` (gpg's default key), a key identifier passed to libgpgme, or `!script` to run a signing script; the key must be usable non-interactively on the repo host (agent with a cached passphrase or a dedicated signing key kept only there).
- `VerifyRelease` checks the upstream Release.gpg against the key given as the last 16 hex digits of the fingerprint.

## Verify
`apt-cache policy openssl` on a prod client shows the version in `jammy-prod`; `gpg --verify dists/jammy-prod/InRelease` passes.

## Checked

Checked 2026-10-27 against the Debian stable reprepro manual page.
- Commands `includedeb <codename> <file.deb>`, `update`, `checkupdate`, `pull`, `export` and the `--export` modes: confirmed.
- `conf/distributions` fields `SignWith`, `Update`, `Pull`; `conf/updates` fields `Name`, `Method`, `VerifyRelease` (16 hex digits), `FilterList`; `conf/pulls`: confirmed.
- Removed unconfirmed: the "one version per package per suite" default and the `Limit:` option with its version gate; the example key IDs are placeholders and must be replaced.
Method: documentation only; no commands were run.
