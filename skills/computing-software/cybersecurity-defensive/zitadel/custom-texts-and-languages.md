---
id: computing-software.cybersecurity-defensive.zitadel.custom-texts-and-languages
name: custom-texts-and-languages
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, i18n, message-texts, login-texts, languages]
level: practitioner
status: docs-checked
description: "Customize ZITADEL message and login texts per language, and restrict which languages are offered."
sources:
  - https://zitadel.com/docs/guides/manage/customize/texts
  - https://zitadel.com/docs/guides/manage/customize/restrictions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Texts can be customized at instance or organization level.

Message texts cover emails and phone messages such as a password reset request. Open the message text policy, choose the template and language, and edit. When you click an input field, attribute chips appear under it showing parameters you can insert into that message.

Login texts work the same way: choose the screen and language, see the default in the box and overwrite it.

Reset policy removes your customization.

ZITADEL ships with many languages, including German, English, Spanish, French, Italian, Japanese, Polish, Chinese, Portuguese, Czech, Russian, Dutch, Swedish, Korean, Turkish, Ukrainian and Arabic. The language shown follows the browser's language header. If that language is unsupported or restricted, the instance default language is used. Missing languages can be contributed as translation files.

To offer only a subset, use the AllowedLanguages restriction through the restrictions API (or the Languages default settings in the console). Then the login UI and notification messages render only in allowed languages, and the OIDC discovery document lists only those in `ui_locales_supported`. Custom texts can still be created for a disallowed language that ZITADEL supports, so you can prepare texts before allowing it.

## Checked

2026-11-08. Read in full: the customized texts page and the feature restrictions page. All claims confirmed; the language list in the skill is a subset of the documented list.

Method: documentation only; no commands were run.
