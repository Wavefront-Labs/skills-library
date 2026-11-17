---
id: computing-software.ai-ml-engineering.litellm.litellm-config-vs-database-settings
name: litellm-config-vs-database-settings
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, config-yaml, store-model-in-db, config-update]
level: sme
status: docs-checked
description: "Since v1.103.0 a setting declared in config.yaml is owned by the file, and UI or API writes to it are refused."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Applies to general_settings, router_settings, litellm_settings and environment_variables, owned key by key.

Rules:

- A key declared in config.yaml is owned by the file; the proxy always runs with the file's value.
- A key the file does not declare is owned by the database, so the Admin UI, /config/update and /config/field/update can change it.
- A write to a file-owned key is refused with HTTP 400 naming the key and section, for example `general_settings key 'store_model_in_db' is set in the config file and cannot be changed here.` The response lists `keys`, `section`, `stored_database_values_ignored` and a `resolution`: edit the config file, or remove the key from the file to let the database own it.
- /config/update returns the same fields inside error.message.
- Resending the value the file already holds is accepted, since it changes nothing.
- If the database already holds a value for a key the file now declares (for example saved from the UI before you added it to the YAML), that stored value is ignored and never applied.

model_list is not merged this way: models added through the UI or API are stored in LiteLLM_ProxyModelTable and served alongside the YAML models, so a database model never replaces a YAML one.

Before v1.103.0 precedence was the reverse: the database was deep-merged over config.yaml, so the database value won, and editing the YAML and restarting did not change the running value.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/configs (config.yaml vs database settings section)
