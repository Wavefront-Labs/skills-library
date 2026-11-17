---
id: computing-software.web-development.bun.upgrade-and-canary
name: upgrade-and-canary
category: computing-software
field: web-development
product: bun
tags: [bun-upgrade, canary-build, pin-version, stable-channel]
level: intro
status: docs-checked
description: "Upgrade Bun in place, switch to the canary or back to stable, install a specific older version, and avoid conflicts with Homebrew or Scoop installs."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/installation.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun upgrade                 # upgrade in place
bun upgrade --canary        # canary channel
bun upgrade --stable        # back to stable
```

Canary builds are released on every commit to main, are untested, and automatically upload crash reports. Use one to try new features and fixes before they reach a stable release.

Pin an older version at install time:

```bash
curl -fsSL https://bun.com/install | bash -s "bun-v1.3.3"
```

```powershell
iex "& {$(irm https://bun.com/install.ps1)} -Version 1.3.3"
```

Gotcha: if Bun came from Homebrew or Scoop, upgrade with `brew upgrade bun` or `scoop update bun` instead of `bun upgrade`, to avoid conflicts between the package manager and the self-upgrade.

Check the result with `bun --version`; `bun --revision` prints the exact commit.

## Checked

2026-11-04. Confirmed against bun docs installation.mdx: bun upgrade, --canary and --stable, canary release cadence, untested status and crash reports, install-script version pinning for Linux/macOS and Windows, Homebrew and Scoop upgrade commands, bun --version and --revision. Replaced an unsourced stability warning and a note about reporting issues.

Method: documentation only; no commands were run.
