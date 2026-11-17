---
id: computing-software.web-development.eleventy.eleventy-supplied-data
name: eleventy-supplied-data
category: computing-software
field: web-development
product: eleventy
tags: [page-variable, eleventy-variable, fileslug, filepathstem, frozen-data]
level: practitioner
status: docs-checked
description: "Use the data Eleventy supplies to templates: pkg, collections, the page and eleventy variables, fileSlug rules, and frozen reserved data."
sources:
  - https://www.11ty.dev/docs/data-eleventy-supplied/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Supplied keys: `pkg` (package.json values), `pagination`, `collections`, `page`, `eleventy` (1.0.0+).

`page` holds `url`, `fileSlug`, `filePathStem`, `date`, `inputPath` (includes the input dir), `outputPath`, `outputFileExtension`, `templateSyntax`, `rawInput` (3.0+) and `lang` (only with the i18n plugin). `url` and `outputPath` are `false` when `permalink` is `false`. It is also `this.page` in shortcodes, filters, transforms and linters.

`fileSlug` comes from `inputPath`: `2018-01-01-myFile.md` gives `myFile`; `myDir/myFile.md` gives `myFile`. For index templates it is the parent directory: `index.md` gives empty, `myDir/index.md` gives `myDir`.

`filePathStem` is the path minus extension, e.g. `myDir/myFile`. For a file extension in the URL:

```yaml
permalink: "{{ page.filePathStem }}.html"
```

`eleventy` has `version`, `generator`, `env` (`root`, `config`, `source` of `cli` or `script`, `runMode` of `serve`, `watch` or `build`) and `directories` (3.0.0+).

```html
<meta name="generator" content="{{ eleventy.generator }}">
```

From 3.0, `pkg`, `eleventy`, `page`, `content` and `collections` are frozen. Opt out temporarily with `eleventyConfig.setFreezeReservedData(false)`.

## Checked

2026-11-04. Confirmed against the Eleventy Supplied Data page: pkg, pagination, collections, page and eleventy (v1.0.0) keys, the page fields with their notes (false url and outputPath, rawInput 3.0+, lang with the i18n plugin, this.page availability), fileSlug and filePathStem rules, eleventy.version, generator, env (root, config, source, runMode) and directories (v3.0.0), the generator meta tag, and frozen reserved data in Eleventy 3.0. Corrected the directories version gate from 3.0.0-alpha.6 to 3.0.0.

Method: documentation only; no commands were run.
