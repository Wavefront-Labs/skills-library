---
id: computing-software.ai-ml-engineering.litellm.litellm-prod-security-settings
name: litellm-prod-security-settings
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, master-key, litellm-salt-key, trusted-proxy-ranges]
level: practitioner
status: docs-checked
description: "Production security settings for the LiteLLM proxy: master key, trusted proxy ranges, salt key and LITELLM_MODE."
sources:
  - https://docs.litellm.ai/docs/proxy/prod
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Master key: the proxy admin credential. It authenticates admin API calls and is the Admin UI login password. It must start with `sk-`; keep it in a secret manager.

```
export LITELLM_MASTER_KEY="sk-<long-random-value>"
```

Trusted proxy ranges: failed Admin UI sign-ins are limited per source address, and that limit only runs when the proxy knows which address is the client. Set the CIDR ranges of the proxies in front of it:

```
general_settings:
  trusted_proxy_ranges: ["10.0.0.0/8"]   # or [] when clients connect directly
```

Salt key: if you use the database, set a salt key used to encrypt and decrypt stored variables.

```
export LITELLM_SALT_KEY="sk-<paste-a-long-random-key>"
```

Failure mode: do not change it after adding a model. It encrypts your LLM API key credentials, and changing it makes them unreadable.

Disable load_dotenv: `export LITELLM_MODE="PRODUCTION"` stops LiteLLM automatically loading credentials from a local .env file.

Alerting: set `alerting: ["slack"]` under general_settings and export `SLACK_WEBHOOK_URL`, or configure it in the Admin UI under Settings, Logging and Alerts, Alerting Types. It covers LLM exceptions, slow or hanging requests, budget crossings, database exceptions, outages and weekly spend reports.

Image: pin a version (for example `docker.litellm.ai/berriai/litellm:v1.98.0`), do not use `:latest`.

## Checked

2026-11-03. Confirmed on the LiteLLM production page (docs.litellm.ai/docs/proxy/prod): master key must start with sk-, trusted_proxy_ranges, LITELLM_SALT_KEY and not changing it, LITELLM_MODE=PRODUCTION disabling load_dotenv, Slack alerting and its alert types, and pinning an image version instead of :latest.

Method: documentation only; no commands were run.
