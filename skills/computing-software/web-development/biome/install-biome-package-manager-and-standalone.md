---
id: computing-software.web-development.biome.install-biome-package-manager-and-standalone
name: install-biome-package-manager-and-standalone
category: computing-software
field: web-development
product: biome
tags: [biome, install, npm, pnpm, yarn, bun, deno, standalone-binary, version-pinning, install-script, platforms]
level: intro
status: docs-checked
description: "Install @biomejs/biome with exact pinning via npm, pnpm, Yarn, Bun or Deno, or use the standalone installer, with platform and installer options."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/installation/install-biome.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Biome ships as an npm package and as a standalone executable. Use a package manager when the project already has one; use the standalone binary when you have no Node.js or when Biome would be the only reason for a `package.json`.

**Package managers** (the `-E` flag pins the exact version so contributors and CI run the same Biome, which matters because rule behaviour changes between versions):

```sh
npm i -D -E @biomejs/biome
pnpm add -D -E @biomejs/biome
yarn add -D -E @biomejs/biome
bun add -D -E @biomejs/biome
deno add -D npm:@biomejs/biome
```

**Standalone installer** (no Node.js; afterwards run `biome` directly, restarting the shell may be needed):

```sh
curl -fsSL https://biomejs.dev/install | bash        # macOS, Linux
irm https://biomejs.dev/install.ps1 | iex            # Windows PowerShell
```

It installs to `${XDG_BIN_HOME:-$HOME/.local/bin}` on macOS and Linux and `%LOCALAPPDATA%\Biome\bin` on Windows. Specific version: `bash -s -- --version 2.5.9`, or on PowerShell set `$env:BIOME_VERSION` first. Options: `BIOME_INSTALL_DIR` env var changes the directory; `--no-modify-path` (`-NoModifyPath`) leaves PATH alone; `--force` (`-Force`) reinstalls an installed version.

**Binary names by platform:** `win32-arm64`/`win32-x64`, `darwin-arm64` (Apple silicon)/`darwin-x64`, `linux-arm64`/`linux-x64`, `linux-arm64-musl`/`linux-x64-musl`, `android-arm64`/`android-x64` (Termux). Use the Linux variant inside WSL.

Once installed, `biome check` runs the formatter, linter and assist actions.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
