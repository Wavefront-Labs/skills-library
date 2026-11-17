---
id: computing-software.systems-network-administration.immich.config-file
name: config-file
category: computing-software
field: systems-network-administration
product: immich
tags: [immich-config-file, json, yaml, configuration, gitops]
level: practitioner
status: docs-checked
description: "Manage Immich settings from a JSON or YAML file via IMMICH_CONFIG_FILE, mount it in Docker Compose, and know it locks the matching web UI settings."
sources:
  - https://docs.immich.app/install/config-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: configure Immich declaratively instead of through the admin UI.

Caveat: specifying `IMMICH_CONFIG_FILE` disables editing other properties from the web UI, even if the file contains only some keys.

Step 1, create the file: JSON (for example `immich-config.json`) or YAML. It need not contain every key. The quickest start is the button in Administration, Settings that copies the current configuration to your clipboard; paste it into a file.

Top-level sections in the default config include `backup`, `ffmpeg`, `image`, `job`, `library`, `logging`, `machineLearning`, `server` and `storageTemplate`, plus `trash`. Examples:

- `backup.database`: `cronExpression` `0 02 * * *`, `enabled` true, `keepLastAmount` 14.
- `library.scan`: `cronExpression` `0 0 * * *`; `library.watch.enabled` false.
- `ffmpeg`: `accel`, `accelDecode`, `crf` 23, `preset` `ultrafast`.
- `image.preview.size` 1440, `image.thumbnail.size` 250.

Step 2, point the server at it in `.env`:

```
IMMICH_CONFIG_FILE=/config/immich-config.json
```

The value is the path inside the container (whereas `UPLOAD_LOCATION` and `DB_DATA_LOCATION` are host paths). Reuse it in the compose volumes:

```yaml
volumes:
  - ./immich-config.json:${IMMICH_CONFIG_FILE}
```

Any `microservices` worker container needs the same mount too.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: install/config-file (Steps 1 and 2, default config).
Removed or reworded: the system_metadata storage claim (it is on the database-queries page, not this one).
Method: documentation only; no commands were run.
