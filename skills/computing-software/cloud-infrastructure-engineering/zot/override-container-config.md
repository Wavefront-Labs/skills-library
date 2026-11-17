---
id: computing-software.cloud-infrastructure-engineering.zot.override-container-config
name: override-container-config
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, container-config, custom-config, bind-mount, volume-mount]
level: intro
status: docs-checked
description: "Replace the default Zot container configuration by mounting a custom config file and a storage directory, changing the listen port and data location."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/admin-guide/admin-getting-started.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A locally built Zot image reads its default configuration from `/etc/zot/config.json` and stores data under `/var/lib/registry`. Auth is disabled by default.

To override, mount your own file over the config path and mount a storage directory that matches the `rootDirectory` in your config:

```
podman run --rm -p 8080:8080 \
  -v $(pwd)/custom-config.yml:/etc/zot/config.yml \
  -v $(pwd)/registry:/tmp/zot \
  zot:latest
```

This example listens on port 8080 and stores content in `/tmp/zot`, so the port published with `-p` and the `rootDirectory` in the config must agree with the mounts.

Default mount without override:

```
podman run --rm -it -p 5000:5000 -v $(pwd)/registry:/var/lib/registry zot:latest
```

Docker takes the same flags.

Tips:
- Validate the file first with `zot verify <configfile>`.
- Config may be JSON or YAML.
- Published image names are `ghcr.io/project-zot/zot` (full) and `ghcr.io/project-zot/zot-minimal`.

## Checked

Container deployment section and zot verify section read.

Method: docs-checked 2026-11-09 against zot docs admin-guide/admin-getting-started.md and admin-guide/admin-configuration.md (verify section).
