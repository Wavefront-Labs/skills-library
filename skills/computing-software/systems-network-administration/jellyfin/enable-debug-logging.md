---
id: computing-software.systems-network-administration.jellyfin.enable-debug-logging
name: enable-debug-logging
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, logging, debug-logging, logging-json, serilog, troubleshooting]
level: practitioner
status: docs-checked
description: "Turn Jellyfin debug logging on and off by editing the Serilog MinimumLevel in logging.json, and know when it reloads."
sources: ["https://jellyfin.org/docs/general/administration/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enabling and restoring debug logging

Debug logging cannot be enabled from the web UI; edit `logging.json` in the Jellyfin configuration directory. Some platforms also have `logging.default.json`, which supplies defaults that a custom `logging.json` overrides.

Create `logging.json` with:

```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Debug"
    }
  }
}
```

If the file already exists, edit only the `Serilog` `MinimumLevel` section and change nothing else.

**Caution:** debug output is very large; loading the homepage alone generates over 4000 lines. Do not leave it on in production for long. When sharing extensive debug logs in an issue, compress them.

Debug lines carry the `DBG` tag, although some components also log extra detail at `INF`.

**Reload behaviour:** if `logging.json` existed before the last server start, the change is applied automatically without a restart. If you created the file after the last start, restart the server.

**Restore normal logging** by deleting the override file you created, or setting the section back to:

```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": { "Microsoft": "Warning", "System": "Warning" }
    }
  }
}
```

Logs live in the log directory (see `computing-software.systems-network-administration.jellyfin.server-path-precedence`); for transcoding failures check the ffmpeg logs first.

## Checked

2026-11-03. Confirmed against the Jellyfin Troubleshooting and Configuration pages: logging.json and logging.default.json, both JSON snippets, DBG tag, 4000-line warning, reload behaviour, compress-logs note, ffmpeg logs. Nothing removed.

Method: documentation only; no commands were run.
