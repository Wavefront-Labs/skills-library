---
id: computing-software.web-development.strapi.i18n-setup
name: i18n-setup
category: computing-software
field: web-development
product: strapi
tags: [strapi, i18n, internationalization, locales, localization, content-type-builder]
level: practitioner
status: docs-checked
description: "Enable Strapi Internationalization: tick it per content-type and field in the Content-type Builder, then manage locales in Settings."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/internationalization.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/environment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Internationalization setup

Two places to configure before it works in the Content Manager.

## 1. Content-type Builder
Per content-type or per field:
1. Edit or create the content-type or field.
2. Open the **Advanced settings** tab.
3. Tick "Internationalization" at content-type level and "Enable localization for this field" at field level.

## 2. Locales
Settings > Global Settings > Internationalization lists all locales. By default only English is configured and set as default. Add locales there; a locale must exist before the REST `locale` parameter can use it.

## API
- REST: `?locale=fr` (see `computing-software.web-development.strapi.rest-locale-parameter`).
- The `locale` and `localizations` attribute types only work when i18n is enabled on the content-type.

## Environment
`STRAPI_PLUGIN_I18N_INIT_LOCALE_CODE` (optional) sets the initialization locale of the application when i18n is installed and enabled.

## Checked

2026-11-04: checked against the Strapi docs pages Internationalization (features/internationalization) and Environment variables configuration. Confirmed: Content-type Builder Advanced settings steps, Settings > Global Settings > Internationalization, English as the only default locale, the REST locale prerequisite, `STRAPI_PLUGIN_I18N_INIT_LOCALE_CODE`, `locale` and `localizations` attributes. Removed: the Document Service relations sentence and the `i18n: true` config shorthand, neither confirmed by the cited pages.

Method: documentation only; no commands were run.
