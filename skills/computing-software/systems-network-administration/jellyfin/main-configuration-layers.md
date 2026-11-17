---
id: computing-software.systems-network-administration.jellyfin.main-configuration-layers
name: main-configuration-layers
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, configuration, environment-variables, logging-json, hostwebclient, ffmpeg-probesize]
level: advanced
status: docs-checked
description: "Understand how Jellyfin layers its main configuration and set hostwebclient, FFmpeg probesize, analyzeduration and PublishedServerUrl."
sources: ["https://jellyfin.org/docs/general/administration/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Main configuration layers and options

Jellyfin builds its main server configuration on the ASP.NET configuration framework. Sources load from the configuration directory in this order, and later sources overwrite earlier ones:

1. Hard-coded defaults from the server source, which cannot be changed.
2. `logging.default.json`, reserved for the server and overwritten on each release. Do not edit it.
3. `logging.json`, the file to change for custom logging. Jellyfin uses Serilog, whose own documentation lists the available options. The file is reloaded and applied at runtime.
4. Environment variables with the `JELLYFIN_` prefix. A double underscore replaces the colon, so `HttpListenerHost:DefaultRedirectPath` becomes `JELLYFIN_HttpListenerHost__DefaultRedirectPath`.
5. Command line options, which win. `--nowebclient` sets `hostwebclient` to false.

Documented keys:

| Key | Default | Meaning |
| --- | --- | --- |
| `hostwebclient` | `True` | Server hosts the web client |
| `FFmpeg:probesize` | `"1G"` | FFmpeg `probesize` format option |
| `FFmpeg:analyzeduration` | `"200M"` | FFmpeg `analyzeduration` format option |
| `PublishedServerUrl` | URL from the primary IP | Server URL published in UDP auto discovery responses |

These static settings are distinct from the runtime settings in the Administrator Dashboard.

## Checked

2026-11-03. Confirmed against the Jellyfin Configuration page, Main Configuration: the five source layers and precedence, JELLYFIN_ prefix example, --nowebclient, and the four keys with defaults. Removed: unsupported advice on containers and the invented check.

Method: documentation only; no commands were run.
