---
id: computing-software.devops-ci-cd.earthly.earthly-install-verify-uninstall
name: earthly-install-verify-uninstall
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, bootstrap, install, with-autocomplete, checksum, gpg, deb-repo, uninstall]
level: intro
status: docs-checked
description: "Install the earthly binary manually, run earthly bootstrap, verify the GPG-signed checksum, use apt/dnf/yum repos or Windows, run a hello-world check, and uninstall."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/alt-installation/alt-installation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install, verify and uninstall earthly manually

Goal: install earthly without the web installer, optionally verify the download, and remove it later.

Prerequisites: Docker or Podman, Git; on Windows also the Docker or Podman WSL 2 backend.

## Binary install
Download the binary for your platform from the GitHub releases page, rename it to `earthly`, put it in your `bin`, then:

```bash
sudo earthly bootstrap --with-autocomplete
```

Restart your shell afterwards. This also adds shell auto-completion.

## Verify the checksum (optional)
```bash
wget https://pkg.earthly.dev/earthly.pgp
md5sum earthly.pgp          # expect 8f455671610b15ee21be31e9f16b7bb6
gpg --import earthly.pgp
echo -e "5\ny\n" |  gpg --command-fd 0 --expert --edit-key 5816B2213DD1CEB61FC952BAB1185ECA33F8EB64 trust
wget https://github.com/earthly/earthly/releases/latest/download/checksum.asc
gpg --verify checksum.asc && gpg --verify --output checksum checksum.asc
sha256sum --check checksum --ignore-missing   # shows e.g. earthly-linux-amd64: OK
```

## Package repositories (beta)
- Debian/Ubuntu: install apt-transport-https, ca-certificates, curl, gnupg, lsb-release; fetch https://pkg.earthly.dev/earthly.pgp through `gpg --dearmor` into /usr/share/keyrings/earthly-archive-keyring.gpg; add a `deb [arch=amd64 signed-by=...] https://pkg.earthly.dev/deb stable main` line to /etc/apt/sources.list.d/earthly.list; then `sudo apt-get install earthly`.
- Fedora: `sudo dnf config-manager --add-repo https://pkg.earthly.dev/earthly.repo` then `sudo dnf install earthly`.
- CentOS: `sudo yum-config-manager --add-repo https://pkg.earthly.dev/earthly.repo` then `sudo yum install earthly`.

## Windows and macOS
Native Windows is experimental: download earthly-windows-amd64.exe and put it on PATH; if you mostly work in WSL2, follow the Linux instructions instead (the original WSL is unsupported). macOS binaries are earthly-darwin-arm64 and earthly-darwin-amd64; you may need a Gatekeeper exception.

## Check it works
```bash
earthly github.com/earthly/hello-world:main+hello
```
Expected output ends with "Target github.com/earthly/hello-world:main+hello built successfully" and a SUCCESS banner.

## Uninstall
macOS: `brew uninstall earthly`, `rm -rf ~/.earthly`. Linux/WSL2: remove /usr/local/bin/earthly and the bash and zsh completion files, then `rm -rf ~/.earthly`. Both: `docker rm --force earthly-buildkitd` and `docker volume rm --force earthly-cache`.

## Gotcha
Do not drop the first `gpg --verify checksum.asc`: gpg still writes the `checksum` file even when signature verification fails.

## Checked

2026-11-07. Read docs/alt-installation.md in full. Install, verify, uninstall commands, md5, fingerprint, package-manager steps and Windows/macOS notes match the page text. The pkg.earthly.dev and api.earthly.dev URLs inside commands could not be fetched by the script and were confirmed only as written on the page. Nothing removed.
Method: documentation only; no commands were run.
