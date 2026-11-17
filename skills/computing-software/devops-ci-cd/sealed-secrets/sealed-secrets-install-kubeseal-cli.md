---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-install-kubeseal-cli
name: sealed-secrets-install-kubeseal-cli
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, kubeseal, install, homebrew, macports, nixpkgs, go-install, linux]
level: intro
status: docs-checked
description: "Install the kubeseal client via Homebrew, MacPorts, Nixpkgs, a Linux release tarball or go install, including a script that resolves the latest version."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets install kubeseal cli

Package managers:
- Homebrew: `brew install kubeseal`
- MacPorts: `port install kubeseal`
- Nixpkgs: `nix-env -iA nixpkgs.kubeseal` (not maintained by the project)

Linux, from a release tarball (set `KUBESEAL_VERSION` without the leading v, for example `0.23.0`):

```bash
curl -OL "https://github.com/bitnami/sealed-secrets/releases/download/v${KUBESEAL_VERSION:?}/kubeseal-${KUBESEAL_VERSION:?}-linux-amd64.tar.gz"
tar -xvzf kubeseal-${KUBESEAL_VERSION:?}-linux-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
```

For automation the README resolves the newest tag with the GitHub API and `jq`:

```bash
KUBESEAL_VERSION=$(curl -s https://api.github.com/repos/bitnami/sealed-secrets/tags | jq -r '.[0].name' | cut -c 2-)
```

and aborts if the variable is empty before downloading.

From source, the latest client lands in `$GOPATH/bin`:

```bash
go install github.com/bitnami/sealed-secrets/cmd/kubeseal@main
```

You can replace `main` with a release tag or commit SHA. Check the release notes when upgrading client or controller, since breaking changes are listed there. Run `kubeseal --help` for the full flag list.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections Kubeseal, Upgrade.
Confirmed: Homebrew, MacPorts, Nixpkgs (not maintained by the project), Linux tarball commands, GitHub API tag lookup, `go install ...@main` and `$GOPATH/bin`, release notes pointer.
Removed: nothing.
Method: documentation only; no commands were run.
