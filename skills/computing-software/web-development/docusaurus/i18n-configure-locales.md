---
id: computing-software.web-development.docusaurus.i18n-configure-locales
name: i18n-configure-locales
category: computing-software
field: web-development
product: docusaurus
tags: [i18n, locales, localeconfigs, localedropdown, rtl]
level: practitioner
status: docs-checked
description: "Configure Docusaurus i18n: declare locales and localeConfigs, add the localeDropdown navbar item, start the dev server per locale, and find the i18n translation folders."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/i18n/i18n-tutorial.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Declare locales in the site config:

```js title="docusaurus.config.js"
export default {
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'fr', 'fa'],
    localeConfigs: {
      en: {htmlLang: 'en-GB'},
      fa: {direction: 'rtl'},
    },
  },
};
```

Locale names set the translation file locations and the translated base URLs; only the default locale omits its name from the URL when building all locales. Docusaurus derives defaults from the name (the `<html lang>`, label, calendar format); `localeConfigs` overrides them, and a locale can be omitted there if defaults suffice.

Add a locale switcher to the navbar:

```js
navbar: {items: [{type: 'localeDropdown', position: 'left'}]},
```

`queryString: '?persistLocale=true'` on that item appends a query parameter on switch, useful for server-side locale detection (for example storing the preference in a cookie).

Start the dev server for one locale:

```bash
npm run start -- --locale fr
```

Each locale is a distinct standalone single-page application, so you cannot run all locales in dev at once. Restart after copying files; hot reload works better on edits of existing files. Default translations for generic theme labels (such as pagination) ship with the theme.

All translation data for a locale lives in `i18n/<locale>`. Each plugin has its own subfolder, and `code.json` holds the React-code labels.

## Checked

2026-11-04: read the Docusaurus i18n tutorial in full. Confirmed the i18n config example, locale name and base URL rule, defaults derived from the name, localeDropdown with queryString, start --locale, the standalone SPA warning, restart note, default theme translations and the i18n folder layout. Nothing removed.

Method: documentation only; no commands were run.
