---
id: computing-software.cybersecurity-defensive.keycloak.theme-migration-on-upgrade
name: theme-migration-on-upgrade
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, themes, upgrade, templates, freemarker]
level: practitioner
status: docs-checked
description: "Migrate custom Keycloak themes after an upgrade by diffing templates, message keys and styles against the new base theme."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/upgrading/topics/migrate_themes.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# theme migration on upgrade
Custom themes must be migrated to the new server, and changes to the built-in themes may need to be reflected in them, depending on what you customised.

Procedure from the upgrade guide:
1. Copy your custom themes from the old server's themes directory to the new server's themes directory.
2. Migrate templates, messages and styles:
   - **Templates**: if you customised any of the updated templates listed in Migration Changes, compare your template with the new base theme version using a diff tool. The guide's example shows one difference that is your customisation (a greeting) and one that is an upstream change (an `if pageRedirectUri` condition in `info.ftl`); copy the upstream change into your template. The harder alternative is to diff the old installation's template against the new one and apply those changes by hand.
   - **Messages**: if you customised messages you might need to change the key or value or add messages. Added values: review the base theme value; renamed keys: rename the key in your theme; changed values: check the base value.
   - **Styles**: if you extend the Keycloak themes, review style changes (for example diff the old and new `themes/keycloak/login/resources/css/login.css`); if you extend the `base` theme you can skip this step.

## Checked
2026-11-03. Confirmed against upgrading/topics/migrate_themes.adoc. Removed (not on the page): the "keep themes small" good practice, the `keycloak.v2` name, the caching and FreeMarker gotchas and the Verify step.
Method: documentation only; no commands were run.
