---
id: computing-software.web-development.docusaurus.cli-write-translations
name: cli-write-translations
category: computing-software
field: web-development
product: docusaurus
tags: [write-translations, i18n-json, message-prefix, locale-flag, override]
level: practitioner
status: docs-checked
description: "Generate the JSON translation files for a Docusaurus site with docusaurus write-translations, including --locale, --override and --messagePrefix."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`docusaurus write-translations [siteDir]` writes the JSON translation files you need to translate. By default they go to `website/i18n/<defaultLocale>/...`.

| Option | Default | Use |
| --- | --- | --- |
| `--locale` | `<defaultLocale>` | which locale folder to write the JSON files in |
| `--override` | `false` | override existing translation messages |
| `--config` | | path to the config file |
| `--messagePrefix` | `''` | prefix every message, to highlight untranslated strings |

```sh
npm run write-translations -- --locale fr --messagePrefix "(fr) "
```

The prefix makes untranslated strings easy to spot when previewing the locale.

Related CLI behaviour: `docusaurus start --locale <locale>` previews one locale, and `docusaurus build --locale <locale>` builds only that locale (default: all known locales).

## Checked

2026-11-04: read the Docusaurus CLI page in full. Confirmed write-translations options, defaults and output location, and the --locale behaviour of start and build. Nothing removed.

Method: documentation only; no commands were run.
