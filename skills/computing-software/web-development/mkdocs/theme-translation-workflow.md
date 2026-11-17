---
id: computing-software.web-development.mkdocs.theme-translation-workflow
name: theme-translation-workflow
category: computing-software
field: web-development
product: mkdocs
tags: [theme-translation, pybabel, po-files, locales]
level: advanced
status: docs-checked
description: "Add or update a built-in theme translation with pybabel init, update and compile, then test with theme.locale; also how custom themes mark strings with trans."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/translations.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Work from a git checkout of MkDocs, with `pip install 'mkdocs[i18n]'`. Use the two-letter code unless the registry shows regional variants (for example `pt_PT`, `pt_BR`).

```bash
pybabel init --input-file mkdocs/themes/mkdocs/messages.pot --output-dir mkdocs/themes/mkdocs/locales -l es
pybabel update --ignore-obsolete --input-file mkdocs/themes/mkdocs/messages.pot --output-dir mkdocs/themes/mkdocs/locales -l fr
pybabel compile --statistics --directory mkdocs/themes/mkdocs/locales -l es
```

Repeat for `readthedocs`. Edit `locales/<lang>/LC_MESSAGES/messages.po`: fill `msgstr`, never change `msgid`.

Test: set `theme: {name: mkdocs, locale: es}` and run `mkdocs serve`. Undo the locale change before submitting; you only contribute the `messages.po` files (the rest is ignored by git).

Custom themes: wrap text in `{% trans %}...{% endtrans %}`. MkDocs reads only compiled `messages.mo` at `locales/<locale>/LC_MESSAGES/messages.mo`, so run `compile_catalog` before packaging and include the `.mo` files. Child-theme translations merge with the parent's.

## Checked

2026-11-04. Confirmed against the MkDocs Translations guide (prerequisites, `pybabel init`/`update`/`compile` commands, `msgid` warning, testing, ISO-639-1 and `pt_PT`/`pt_BR` note) and the Developing Themes page (translation workflow, `trans` tags, packaging `mo` files, parent-theme merge). Removed the Verify line, which the pages do not state.
Method: documentation only; no commands were run.
