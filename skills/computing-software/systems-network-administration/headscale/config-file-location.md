---
id: computing-software.systems-network-administration.headscale.config-file-location
name: config-file-location
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, config, configtest, search-path, headscale-config]
level: intro
status: docs-checked
description: "Where Headscale reads config.yaml, how to override the path with -c or HEADSCALE_CONFIG, validate with configtest, and fetch the matching example."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Config file location and validation

Headscale reads a YAML file named `config.yaml`, searched in this order:

1. `/etc/headscale`
2. `$HOME/.headscale`
3. the current working directory

Override with the flag `-c` / `--config` or the environment variable `HEADSCALE_CONFIG`.

## Validate

```
headscale configtest
```

## Get the example config

Use the example from the same tag as your release; `main` may include unreleased changes.

```
curl -o config.yaml https://raw.githubusercontent.com/juanfont/headscale/v<VERSION>/config-example.yaml
wget -O config.yaml https://raw.githubusercontent.com/juanfont/headscale/v<VERSION>/config-example.yaml
```

Replace `<VERSION>` with your release number. Release tags are listed at github.com/juanfont/headscale/tags. The development version lives at `.../main/config-example.yaml`.

## Note

The configuration page itself lists no individual keys; `config-example.yaml` from the matching tag is the reference for keys.

## Checked

2026-11-04. Confirmed against the Headscale configuration page (search paths, `-c`/`--config`, `HEADSCALE_CONFIG`, `configtest`, same-tag example config, wget and curl downloads). Removed the claim that commands touching the database directly need a full server config, which the page does not state.

Method: documentation only; no commands were run.
