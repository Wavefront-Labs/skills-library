---
id: computing-software.software-engineering.haskell.ghcup-install-and-manage
name: ghcup-install-and-manage
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, ghcup, ghcup-install, ghcup-tui, set-ghc, recommended, toolchain, msys2, ghcup-install-and-manage, haskell-toolchain]
level: intro
status: docs-checked
description: "Install and switch GHC and cabal with GHCup: the install script, ghcup tui, list, install and set commands, version tags (recommended, latest) and ghcup upgrade."
sources: ["https://www.haskell.org/ghcup/install/", "https://www.haskell.org/ghcup/guide/", "https://www.haskell.org/ghcup/steps/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GHCup

**Goal:** a single installer for the Haskell toolchain (GHC, cabal-install, Stack, HLS).

```bash
# Linux, macOS, FreeBSD or WSL2: run as a non-root user (see https://www.haskell.org/ghcup/install/)
curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
# Windows: the install page gives a PowerShell command
ghcup tui                           # interactive text UI
ghcup list                          # list available ghc/cabal versions
ghcup install ghc                   # install the recommended GHC
ghcup install ghc 9.6.7             # a specific version (example)
ghcup set ghc 9.6.7                 # set the currently "active" GHC
ghcup install cabal
ghcup upgrade                       # update ghcup itself
```
The script downloads the ghcup binary into `~/.ghcup/bin` (a `ghcup\bin` folder on Windows) and then runs it to install the toolchain interactively. On Windows it also installs MSYS2.

## Facts
- Tags and shortcuts accepted by `install` and `set`: `latest`, `recommended`, `base-4.15.1.0`, and `9.0.2`, `9.0` or `9`. With the argument omitted the default is `recommended`. Other tags: `prerelease`, `latest-prerelease`.
- Revisions (for example `9.6.7-r1`) are new bindists or metadata for the same upstream version; only one revision can be installed at a time, and revisions are hidden from the TUI and `list` by default.
- Downloaded tarballs are not cached unless you pass `ghcup --cache` or run `ghcup config set cache true`.
- Metadata is cached for 5 minutes by default, so repeated `ghcup list` calls reuse it.
- `ghcup --help` documents every command and option.

## Gotchas
- Check `which ghc` if you also have a distro or Homebrew GHC on `PATH`.
- VS Code launched outside a terminal may report "cannot find ghc version" because HLS cannot see GHCup on `PATH`; the install page describes the fix.
- Prefer the `recommended` tag for projects; the newest GHC may lag in library or HLS support.

## Self-check
- [ ] `ghc --version` runs.
- [ ] `ghcup list` shows the GHC marked as set that you expect.

## Checked
2026-11-03. Confirmed against the GHCup install page, user guide (basic usage, tags and shortcuts, revisions, caching) and the install script page: install command, install locations, MSYS2 on Windows, `tui`, `list`, `install`, `set`, `upgrade`, tags, revisions, `config set cache true`. Removed: `ghcup rm`, `ghcup compile`, `ghcup list -t hls`, proxy and `--url-source` advice, HLS version matching, Stack `install-ghc` settings and the side-by-side binary naming (not in the pages read).
Method: documentation only; no commands were run.
