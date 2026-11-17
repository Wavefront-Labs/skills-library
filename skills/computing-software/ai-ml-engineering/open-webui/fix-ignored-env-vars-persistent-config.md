---
id: computing-software.ai-ml-engineering.open-webui.fix-ignored-env-vars-persistent-config
name: fix-ignored-env-vars-persistent-config
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [persistent-config, env-configuration, configvar, enable-persistent-config, sqlite]
level: practitioner
status: docs-checked
description: "Work out why an Open WebUI environment variable change is ignored after restart (ConfigVar persistence) and apply it via the admin UI, the flag, or the database."
sources:
  - https://docs.openwebui.com/reference/env-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make a changed environment variable take effect when Open WebUI keeps showing the old value.

## Why it happens
On the first launch every variable configures the app. Variables marked `ConfigVar` in the reference are then persisted in the database. On later restarts they use the stored value, not the environment. Regular variables are re-read on every start. Example: you set `ENABLE_SIGNUP=True` but the Sign Up button is still missing because a value is already stored in the `open-webui` volume.

## Fix options
1. Recommended: change the setting in the Admin Panel. UI changes override the environment and are saved to the database.
2. Temporary: set `ENABLE_PERSISTENT_CONFIG=False` so Open WebUI always uses your environment variables and ignores the database. Critical: with this off you may still edit settings in the Admin UI, but those changes are NOT saved. OAuth settings are shown read-only in the Admin Panel whenever `ENABLE_OAUTH_PERSISTENT_CONFIG` is `False` (its default), so there is nothing to edit.
3. Lock-out recovery: edit SQLite directly.
```bash
docker exec -it open-webui sqlite3 /app/backend/data/webui.db "UPDATE config SET value = json('true') WHERE key = 'ui.enable_signup';"
```
Each setting is its own row under an internal key that differs from the variable name. List keys with `SELECT key FROM config;`, then substitute the key and value.
4. Fresh install only: stop the container, `docker volume rm open-webui`, restart. This deletes all chats and accounts.

## Gotchas
- `WEBUI_URL` is a ConfigVar and must be set before first OAuth/SSO use or login fails. Change it afterwards only in Admin Panel > Settings ("WebUI URL") or with persistent config disabled.
- Variables not marked ConfigVar (for example `PASSWORD_HASH_ALGORITHM`, `ENABLE_API_OUTLET_FILTERS`, `ENABLE_INITIAL_ADMIN_SIGNUP`) apply at startup and need no workaround.
- Keys like `models.default_metadata`, `ui.default_interface_settings` and `ui.visibility` show how names differ from variable names.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page reference/env-configuration (read the ConfigVar note, the troubleshooting section, and the WEBUI_URL, ENABLE_API_OUTLET_FILTERS, ENABLE_INITIAL_ADMIN_SIGNUP, PASSWORD_HASH_ALGORITHM, ENABLE_PERSISTENT_CONFIG and ENABLE_OAUTH_PERSISTENT_CONFIG sections): first-launch persistence, the four fix options and the sqlite3 command, the critical warning and the OAuth read-only exception, the WEBUI_URL restriction and the non-ConfigVar examples. Removed the Verify section, which the page does not contain.
Method: documentation only; no commands were run.
