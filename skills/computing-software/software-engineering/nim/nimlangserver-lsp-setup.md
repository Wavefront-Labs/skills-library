---
id: computing-software.software-engineering.nim.nimlangserver-lsp-setup
name: nimlangserver-lsp-setup
category: computing-software
field: software-engineering
product: nim
tags: [nimlangserver-lsp-setup, editor-tooling, nimlangserver, lsp, vscode, neovim, nim-extension, editor-setup, language-server, project-mapping, nim]
level: practitioner
status: docs-checked
description: "Set up the Nim language server with VS Code, Neovim and Helix, and configure project mapping, nimsuggest and formatting."
sources:
  - https://nim-lang.github.io/langserver/
  - https://nim-lang.github.io/langserver/lsp.html
  - https://github.com/nim-lang/langserver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nimlangserver and editor setup (VS Code, Neovim, Helix)

Goal: get completion, diagnostics and navigation working.

- Requirements: Nim >= 1.6.8 and nimble >= 0.16.1. Install the latest release into `$HOME/.nimble/bin` with `nimble install -g nimlangserver`.
- `nimlangserver` runs as an LSP server by default (`nimlangserver` equals `nimlangserver --lsp`); it can also run as an MCP server for AI coding agents.
- VS Code: install the vscode-nim extension and follow its setup; it bundles the LSP and MCP servers. Sublime Text: LSP-nimlangserver from Package Control. Zed: the Nim extension. Helix: install with Nimble and keep it on `PATH`, no extra configuration. Emacs: lsp-mode and nim-mode from MELPA, then `(add-hook 'nim-mode-hook #'lsp)`.
- Neovim (lspconfig): `require'lspconfig'.nim_langserver.setup{ settings = { nim = { nimsuggestPath = "~/.nimble/bin/nimsuggest" } } }`. The docs say defaults work for most users, so you likely need not set `nimsuggestPath`. coc.nvim uses a `languageserver` block in `coc-settings.json` with `"command": "nimlangserver"`.
- Settings come from the client under `nim.*`: `nim.projectMapping`, `nim.nimsuggestPath` (default `"nimsuggest"`), `nim.checkOnSave` (default true, needs `nim.autoCheckProject`), `nim.autoCheckFile` (default false), `nim.formatOnSave` (needs `nph` on `PATH`), `nim.useNimCheck`, `nim.maxNimsuggestProcesses`, `nim.nimsuggestIdleTimeout`, `nim.inlayHints`.
- Project mapping example: `{"nim.projectMapping": [{"projectFile": "tests/all.nim", "fileRegex": "tests/.*\\.nim"}, {"projectFile": "main.nim", "fileRegex": ".*\\.nim"}]}`. Mappings are checked in order, so put specific patterns first; paths are relative to the workspace root and the mapped file must be a compilable entry point.
- Inside a Nimble project, nimble drives the nimsuggest entry points automatically. Document formatting requires `nph` on `PATH`.

Gotchas:
- Without a mapping the opened file becomes its own project root, so independent entry points that use the file are not seen; generic code may then resolve badly.
- Exception inlay hints are off by default because they can multiply nimsuggest's initial compile time; type hints are on by default.
- On Windows the docs recommend WSL for better performance and stability.

Verify: hover shows types and go-to-definition works on a symbol from another module.

## Checked

2026-11-08. Read in full: the Quickstart and LSP Server pages of the Nim Language Server book (setup per editor, supported features, nim.* settings table, project-mapping examples, inlay hints) and the repository README. Removed: the extension id, `nim.lintOnSave` and `nim.timeout` as VS Code keys (the settings table lists different names), `nimble setup` advice, and the claims about Helix/Zed "using the same server" detail beyond the setup lines; manual, tutorial and lib.html dropped from sources.
Method: documentation only; no commands were run.
