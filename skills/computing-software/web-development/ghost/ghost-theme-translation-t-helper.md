---
id: computing-software.web-development.ghost.ghost-theme-translation-t-helper
name: ghost-theme-translation-t-helper
category: computing-software
field: web-development
product: ghost
tags: [ghost, theme, translation, i18n, locales, t-helper]
level: practitioner
status: docs-checked
description: "Make a Ghost theme translatable with locales JSON files and the t helper, then enable the publication language."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/helpers/utility/translate.mdx
  - https://github.com/TryGhost/docs/blob/main/faq/translation.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve a theme in the site's language.

Steps:
1. Create a `locales` folder in the theme with one JSON file per language, such as `locales/en.json` and `locales/es.json`. Use a valid language code.
2. Put each sentence key and its translation in the file. Keys can be any text, but readable English is advised so the fallback works when a translation is missing.
3. Wrap strings in templates: `{{t "Subscribe"}}`. With the site language set to `es` this outputs the Spanish value.
4. Set the publication language in General settings of Ghost Admin (the JSON file for the active theme must exist).

Details: month names in dates are translated automatically. Use HTML entities instead of characters like `<` inside translation files.

Best practices from the FAQ: keep hardcoded text to a minimum (for example avoid a word like "by" in the byline and just show the author name) and use custom theme settings so site owners can supply translated text.

Further steps from the page: make sure `pagination.hbs` and `navigation.hbs` exist in the theme's `partials` folder; wrap all plain text in `.hbs` templates in `{{t}}`; set `<html lang="{{@site.locale}}">` in `default.hbs`; run `ghost restart` to make the changes effective.

Optional features: placeholders use single braces, e.g. `{{t "Subscribe to {blogtitle}" blogtitle=@site.title}}`; `(t "...")` subexpressions can translate the prefix or suffix of `{{tags}}`, `{{authors}}` or `{{tiers}}`; `{{plural ../pagination.total empty=(t "No posts") singular=(t "1 post") plural=(t "% posts")}}`; `{{reading_time minute=(t "1 min read") minutes=(t "% min read")}}`; `<title>{{meta_title page=(t "Page %")}}</title>`.

Limits from the FAQ: Ghost has native translated system text for transactional emails, Portal, search and comments, but Ghost Admin does not support internationalization yet. The translate helper does not work for multi-language content sites; the FAQ recommends one Ghost install per language for different content per language, or a service such as WeGlot or Transifex for the same content.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 219 and 44 lines, code samples inline, no imported snippets): themes/helpers/utility/translate.mdx and faq/translation.mdx. Steps, key advice, date translation and best practices match. Removed the invented Verify step and rephrased the fallback wording. The page's fallback claim is only that readable English keys help the fallback when no translation exists. Added remaining steps, optional features and FAQ limits.
Method: documentation only; no commands were run.
