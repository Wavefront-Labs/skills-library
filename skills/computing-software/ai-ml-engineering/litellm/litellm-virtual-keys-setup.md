---
id: computing-software.ai-ml-engineering.litellm.litellm-virtual-keys-setup
name: litellm-virtual-keys-setup
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, virtual-keys, master-key, key-generate]
level: intro
status: docs-checked
description: "Set DATABASE_URL and a master key, then create virtual keys with POST /key/generate."
sources:
  - https://docs.litellm.ai/docs/proxy/virtual_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: issue virtual keys from the proxy so clients never hold provider keys.
Goal: issue per-user or per-team proxy keys.

Requirements:

- A Postgres database; set `DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname>` in the environment.
- A master key (the proxy admin key, must start with `sk-`), set either in config.yaml as `general_settings: master_key` or as env var `LITELLM_MASTER_KEY`.

Config:

```
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: "postgresql://<user>:<password>@<host>:<port>/<dbname>"
```

Start with `litellm --config /path/to/config.yaml`, then generate a key:

```
curl 'http://0.0.0.0:4000/key/generate' \
--header 'Authorization: Bearer <your-master-key>' \
--header 'Content-Type: application/json' \
--data-raw '{"models": ["gpt-6-luna", "gpt-6.1-sol"], "metadata": {"user": "ishaan@berri.ai"}}'
```

The response contains an `sk-...` key restricted to those model names. Clients send it as `Authorization: Bearer <key>`.

Keys can belong to users (`user_id`, created with POST /user/new) or teams (`team_id`, created with POST /team/new); use teams when a key should be owned by multiple people, for example a production app.

The proxy Dockerfile checks whether DATABASE_URL is set and then initialises the database connection.
Keys are managed through the /key/generate endpoint with the master key.

## Checked

2026-11-03. Confirmed on the virtual keys page (docs.litellm.ai/docs/proxy/virtual_keys): Postgres and DATABASE_URL, master key starting with sk-, general_settings master_key or LITELLM_MASTER_KEY, the /key/generate call, the Dockerfile DATABASE_URL note, user versus team keys.

Method: documentation only; no commands were run.
