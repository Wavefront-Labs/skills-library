---
id: computing-software.cloud-infrastructure-engineering.zot.extensions-enable-model
name: extensions-enable-model
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, extensions, full-image, mgmt-extension, userprefs, extension-discovery]
level: practitioner
status: docs-checked
description: "How Zot extensions are enabled in config, which exist, which need the full image, and which are API-only (mgmt, user preferences)."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/admin-guide/admin-configuration.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/general/extensions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Extensions add features beyond the Distribution Spec and live under `extensions` in the config:

```json
"extensions": { "metrics": {}, "sync": {}, "search": {}, "scrub": {}, "lint": {}, "trust": {}, "ui": {} }
```

- They exist only in the full image. A minimal image ignores the `extensions` section.
- Presence of the attribute usually enables the feature. Omitting it, or `"enable": false`, disables it.
- Search: basic search is always on; if the `enable` attribute is missing under `search`, enhanced search is enabled by default.
- Full list from the docs: search, sync, lint, scrub, trust, metrics, GUI, user preferences.

API-only extensions with no config keys:
- Mgmt is enabled when `search` is enabled.
- User Preferences is enabled when both `search` and `ui` are enabled.

Only search, trust and userprefs are operable by end users, reachable over HTTP and discoverable through the OCI extensions mechanism (`GET /v2/_oci/ext/discover`).

Extensions can also be selected at build time, for example `make EXTENSIONS=search binary`.

## Checked

Both pages read. Reworded the search default to match the config page.

Method: docs-checked 2026-11-09 against zot docs admin-guide/admin-configuration.md (extensions, search sections) and general/extensions.md.
