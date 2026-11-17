---
id: computing-software.software-engineering.zig.zls-editor-setup
name: zls-editor-setup
category: computing-software
field: software-engineering
product: zig
tags: [zig, zls-editor-setup, zig-ecosystem, zls, language-server, vscode-zig, editor-setup, zig-fmt-on-save]
level: intro
status: docs-checked
description: "Install the Zig Language Server matching your compiler version and set up VS Code, Neovim, Helix or Zed; build-on-save is opt-in."
sources:
  - https://github.com/zigtools/zls
  - https://zigtools.org/zls/install/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ZLS and editor setup
**Goal:** completions, go-to-definition and diagnostics.

- ZLS is a non-official implementation of the Language Server Protocol for Zig, written in Zig (`zigtools/zls`). Features: completions, hover, diagnostics and opt-in build-on-save, go to definition/declaration, workspace and document symbols, find references and rename, formatting based on `zig fmt`, semantic tokens, inlay hints and code actions. Comptime and semantic analysis support is work in progress.
- Version rule (Zigtools install guide): a tagged Zig release goes with the same tagged ZLS release, and a nightly Zig with a nightly ZLS. The patch version (Y in 0.X.Y) need not match exactly; install the latest patch of each. When upgrading Zig, update ZLS to keep them in sync.
- Install: the install guide has a version-selection tool that offers a prebuilt binary (signed with minisign) or build-from-source commands. Building from source: `git clone https://github.com/zigtools/zls`, `cd zls`, `zig build -Doptimize=ReleaseSafe`; the default branch targets Zig master.
- VS Code: the official Zig Language extension (`ziglang.vscode-zig`) is all that is needed; the guide says there is no need to install Zig or ZLS manually.
- Other editor guides on the Zigtools site: Sublime Text, JetBrains IDEs, Helix, Zed, Neovim / Vim8, Emacs, Kate.
- Configuration pages exist for in-editor config, a `zls.json` file, and per-build config; the build-on-save guide covers opt-in diagnostics from the build. Read those pages for key names.

## Gotchas
- A ZLS built for another Zig version gives bogus analysis; match versions as above.

## Self-check
Open a project, hover over a std symbol, jump to its definition, and see a diagnostic appear after a typo.

## Checked

2026-11-08. Read: ZLS README in full; Zigtools ZLS install page (version compatibility section, prebuilt-binary note, VS Code banner, editor and configuration navigation) as served without JavaScript.
Removed: specific `zls.json` keys, Neovim `nvim-lspconfig` detail, "built-in" claims for Helix and Zed, `anytype` inference note, cache-clearing advice, zig.guide source (not read).
Method: documentation only; no commands were run.
