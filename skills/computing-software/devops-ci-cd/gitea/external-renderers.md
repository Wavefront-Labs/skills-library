---
id: computing-software.devops-ci-cd.gitea.external-renderers
name: external-renderers
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-external-renderer, gitea, markup-section, render-command, markup-sanitizer, asciidoctor, jupyter-nbconvert, pandoc]
level: advanced
status: docs-checked
description: "Render extra file types in Gitea with external binaries: [markup.NAME] sections, RENDER_COMMAND, IS_INPUT_FILE, bluemonday sanitizer rules, CSS hooks."
sources: ["https://docs.gitea.com/administration/external-renderers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# External renderers

Whole-file rendering (AsciiDoc, Jupyter, reStructuredText, HTML, DOCX) is delegated to binaries: install them, add `[markup.NAME]` sections to `app.ini`, restart Gitea. Markdown code-block rendering (e.g. diagrams) needs JavaScript instead (see `gitea-custom-dir`). In Docker, add the packages in your own image (the docs use `apk add asciidoctor pandoc ...` and `pipx install jupyter docutils --include-deps --global`).

```ini
[markup.asciidoc]
ENABLED = true
FILE_EXTENSIONS = .adoc,.asciidoc
RENDER_COMMAND = "asciidoctor -s -a showtitle --out-file=- -"
IS_INPUT_FILE = false

[markup.jupyter]
ENABLED = true
FILE_EXTENSIONS = .ipynb
RENDER_COMMAND = "jupyter nbconvert --stdin --stdout --to html --template basic"
IS_INPUT_FILE = false

[markup.restructuredtext]
ENABLED = true
FILE_EXTENSIONS = .rst
RENDER_COMMAND = "timeout 30s pandoc +RTS -M512M -RTS -f rst"
IS_INPUT_FILE = false
```
`IS_INPUT_FILE = false` feeds content on stdin; `true` passes a file (the HTML example uses `RENDER_COMMAND = cat` with `true`). Wrapping with `timeout` and memory flags protects the server from runaway renders.

## Sanitizer
Output goes through the bluemonday sanitizer; custom classes/attributes need rules. Each `[markup.sanitizer.X]` needs `ELEMENT` and `ALLOW_ATTR`, plus optional `REGEXP`; use unique suffixes for several rules. To scope a rule to one renderer name it `[markup.sanitizer.<renderer>.rule-1]`; a rule defined above its renderer section, or with an unknown name, applies to all renderers. Examples: pandoc math spans `ELEMENT = span`, `ALLOW_ATTR = class`, `REGEXP = ^\s*((math(\s+|$)|inline(\s+|$)|display(\s+|$)))+` with `[markup.markdown] RENDER_COMMAND = pandoc -f markdown -t html --katex`; images inline from a DOCX/Jupyter converter need `[markup.sanitizer.docx.img] ALLOW_DATA_URI_IMAGES = true` (`pandoc --from docx --to html --self-contained --template /path/to/basic.html`, template content `$body$`). Before 1.12 a single `markup.sanitiser` section was used; that format was replaced.

## Styling
Output is wrapped in `<div class="markup NAME">`. Add CSS under `custom/public/assets/css/` and load it with `custom/templates/custom/header.tmpl`: `<link rel="stylesheet" href="{{AppSubUrl}}/assets/css/my-style-NAME.css" />`.

## Checked

2026-11-03: read https://docs.gitea.com/administration/external-renderers/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
