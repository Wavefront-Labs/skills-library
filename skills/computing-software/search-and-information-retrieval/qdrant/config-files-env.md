---
id: computing-software.search-and-information-retrieval.qdrant.config-files-env
name: config-files-env
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [configuration, config-yaml, environment-variables, run-mode, config-files]
level: practitioner
status: docs-checked
description: "Layer Qdrant configuration from config.yaml, RUN_MODE files, local.yaml and QDRANT__ environment variables."
sources:
  - "https://qdrant.tech/documentation/ops-configuration/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Qdrant reads configuration from several layers; later layers win.

1. built-in defaults
2. `config/config.yaml`
3. `config/{RUN_MODE}.yaml`; the Docker image sets `RUN_MODE=production`
4. `config/local.yaml`
5. a file given with `--config-path`
6. environment variables, highest priority

Environment variables use the prefix `QDRANT__` with double underscores for nesting:

```bash
docker run -p 6333:6333 \
  -e QDRANT__SERVICE__API_KEY=<key> \
  -e QDRANT__LOG_LEVEL=INFO \
  qdrant/qdrant
```

That sets `service.api_key` and `log_level`.

An invalid configuration makes Qdrant terminate at startup with an error naming the key, so mistakes show immediately instead of running with wrong values.

For file-based setup, mount individual files into the container, for example `-v $(pwd)/config.yaml:/qdrant/config/config.yaml`, or `dev.yaml` with `-e RUN_MODE=dev`. The docs describe `local.yaml` as typically used for machine-specific settings not tracked in version control. Other formats (`.toml`, `.json`, `.ini`) are also supported. Qdrant Cloud does not allow modifying the configuration.

Because the environment layer wins, a stray `QDRANT__` variable can override a value in a config file, so check the environment when a setting appears ignored.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant configuration page (landing_page repo, ops-configuration/configuration.md), read in full. Removed the unconfirmed secrets-versus-files advice and the directory mount example; the layering order, QDRANT__ naming and validation behaviour are confirmed.
