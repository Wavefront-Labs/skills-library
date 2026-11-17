---
id: computing-software.software-engineering.haskell.hls-editor-setup
name: hls-editor-setup
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, hls, haskell-language-server, hie-yaml, lsp, vscode-haskell, hie-bios, code-actions, plugins, hls-editor-setup]
level: practitioner
status: docs-checked
description: "Install Haskell Language Server with ghcup, write a hie.yaml cradle (cabal, stack, direct, multi), set the formatting provider and plugin switches, and probe tools."
sources: ["https://haskell-language-server.readthedocs.io/en/stable/installation.html", "https://haskell-language-server.readthedocs.io/en/stable/configuration.html", "https://haskell-language-server.readthedocs.io/en/stable/features.html", "https://haskell-language-server.readthedocs.io/en/stable/troubleshooting.html", "https://github.com/haskell/hie-bios"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HLS setup

**Goal:** working type info, completion, diagnostics and code actions in the editor.

## Install
1. Install via GHCup: `ghcup install hls`. For Cabal projects both `ghc` and `cabal-install` must be on the `PATH`; standalone files need `ghc` on the `PATH`.
2. Editor: HLS is an LSP server, so use your editor's LSP client support (for example `nvim-lspconfig` for Neovim, `lsp-haskell` for Emacs).
3. Open the project root.

## Cradles
HLS finds a build context through `hie-bios`. To state it explicitly, put a `hie.yaml` in the workspace root. The supported cradle types are stack, cabal, bios, direct and none, plus multi-cradles that map paths to components:
```yaml
cradle:
  cabal:
    - path: "./src"
      component: "lib:myapp"
```
`lib:myapp` means the library of the package `myapp`. A cabal cradle can also set `cabalProject: "./cabal.project.dev"` to use another project file. Without `hie.yaml`, hie-bios applies implicit configuration.

## Features
Diagnostics (GHC errors, HLint hints), hover, jump to definition, completions, formatting, code actions (apply HLint fixes, make import lists explicit, expand record wildcard), code lenses (add type signature, evaluate code snippets in comments), rename and semantic tokens.

## Settings (VS Code `settings.json`)
```json
{ "haskell.formattingProvider": "fourmolu",
  "haskell.plugin.hlint.globalOn": true }
```
`haskell.formattingProvider` defaults to `ormolu` and accepts `ormolu`, `fourmolu` or `stylish-haskell`. `haskell.plugin.${pluginName}.globalOn` (usually default true) enables or disables a plugin at runtime, for example `haskell.plugin.importLens.globalOn: false`.

## Gotchas
- An HLS build supports only certain GHC versions; see the GHC version support page before pairing them.
- `haskell-language-server --probe-tools` prints useful information such as the HLS version; include it in issue reports.
- Cradle errors: run the build tool (`cabal build`) from the shell to see the real failure.

## Self-check
- [ ] Hover shows types in every component (lib, exe, test).
- [ ] Format-on-save matches CI's formatter.

## Checked
2026-11-03. Confirmed against the HLS installation, configuration, features and troubleshooting pages and the hie-bios README: `ghcup install hls`, PATH requirements, hie.yaml cradle types and the `path`/`component`/`cabalProject` keys, `haskell.formattingProvider` values and default, `haskell.plugin.<name>.globalOn`, `--probe-tools`, feature list. Removed: `haskell.manageHLS`, retrie, `direct` argument example, `exe:`/`test:` component examples, cabal-store reuse claim, memory and `.hie` cache advice, and the "No HLS for GHC" message.
Method: documentation only; no commands were run.
