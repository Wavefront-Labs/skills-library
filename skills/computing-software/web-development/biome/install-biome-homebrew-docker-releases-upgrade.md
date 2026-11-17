---
id: computing-software.web-development.biome.install-biome-homebrew-docker-releases-upgrade
name: install-biome-homebrew-docker-releases-upgrade
category: computing-software
field: web-development
product: biome
tags: [biome, homebrew, winget, arch-linux, docker, ghcr, github-release, biome-upgrade, biome-distribution, biome-migrate]
level: practitioner
status: docs-checked
description: "Install Biome via Homebrew, Winget, pacman, Docker images or GitHub release binaries and upgrade it correctly, then run biome migrate."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/installation/install-biome.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Other install routes**

- Homebrew (macOS, Linux): `brew install biome`.
- Winget (community maintained): `winget install biomejs.biome`.
- Arch Linux (community maintained, `extra` repository): `pacman -S biome`. If `extra` is disabled, uncomment `[extra]` and `Include = /etc/pacman.d/mirrorlist` in `/etc/pacman.conf`.
- **Docker**: official images for `amd64` and `arm64` at `ghcr.io/biomejs/biome:{major}`, `:{major}.{minor}` and `:{major}.{minor}.{patch}`. The working directory is `/code`, so mount the project there:

```sh
docker run -v $(pwd):/code ghcr.io/biomejs/biome check
docker run -v $(pwd):/code ghcr.io/biomejs/biome check --write
```

- **GitHub release**: download the platform binary from the latest release (for example `biome-darwin-arm64`, `biome-linux-x64`, `biome-win32-x64.exe`), `chmod +x biome` on Unix, then run `./biome` or put it on your PATH.

**Upgrading.** Use the same method you installed with. Package managers: reinstall with `@biomejs/biome@latest` (keep `-E`). Standalone: `biome upgrade`, which detects whether Biome came from Homebrew or as a plain binary. If detection is wrong, set the `BIOME_DISTRIBUTION` environment variable. If you installed via Winget or pacman, update with that tool instead.

**After a major upgrade** run `biome migrate` to see the configuration changes the new version requires, then `biome migrate --write` to apply them.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
