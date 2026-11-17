---
id: computing-software.devops-ci-cd.tilt.tilt-editor
name: tilt-editor
category: computing-software
field: devops-ci-cd
product: tilt
tags: [editor, tilt, tiltfile, language-server]
level: intro
status: docs-checked
description: "Set up Tiltfile editor support: the VS Code extension, TextMate bundle, Emacs lsp-mode config and the built-in tilt lsp start server."
sources:
  - "https://docs.tilt.dev/editor.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tiltfile editor support

Goal: get syntax highlighting, autocomplete and signature help for Tiltfiles without leaving the editor.

## VS Code

Install the official `Tiltfile` extension (publisher `tilt-dev`) from the VS Code marketplace. It provides syntax highlighting, autocomplete and signature support for Tiltfile functions.

## TextMate bundles

`tiltfile.tmbundle` (github.com/tilt-dev/tiltfile.tmbundle) gives syntax highlighting in IDEs that support TextMate bundles, such as IntelliJ GoLand, PyCharm or WebStorm.

## Emacs

Tilt works with `lsp-mode`. Install `lsp-mode` and add this to `.emacs`:

```
(require 'python-mode)

(define-derived-mode tiltfile-mode
  python-mode "tiltfile"
  "Major mode for Tilt Dev."
  (setq-local case-fold-search nil))

(add-to-list 'auto-mode-alist '("Tiltfile$" . tiltfile-mode))

(with-eval-after-load 'lsp-mode
  (add-to-list 'lsp-language-id-configuration
    '(tiltfile-mode . "tiltfile"))

  (lsp-register-client
    (make-lsp-client :new-connection (lsp-stdio-connection `("tilt" "lsp" "start"))
                     :activation-fn (lsp-activate-on "tiltfile")
                     :server-id 'tilt-lsp)))
```

## Other editors

Tilt embeds its own language server, based on Tree Sitter (github.com/tilt-dev/starlark-lsp). Run it with:

```
tilt lsp start
```

Adding Tiltfile support to a new editor usually takes a few lines of config to start the language server and connect to it.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/editor.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
