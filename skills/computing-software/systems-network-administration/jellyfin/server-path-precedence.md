---
id: computing-software.systems-network-administration.jellyfin.server-path-precedence
name: server-path-precedence
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, data-directory, config-directory, cache-directory, log-directory, jellyfin-data-dir]
level: practitioner
status: docs-checked
description: "Work out which data, config, cache, web and log directories a Jellyfin server uses and how to override each one."
sources: ["https://jellyfin.org/docs/general/administration/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Jellyfin server paths and their precedence

Jellyfin resolves five directories, each from sources listed here in decreasing precedence. Non-Windows systems follow the XDG base directory specification by default.

**Data directory** (also the base for several others)
1. `--datadir`
2. `JELLYFIN_DATA_DIR`
3. `%ProgramData%\Jellyfin\Server` when launched from the Windows tray app
4. `%LocalAppData%\jellyfin` when the Windows server is launched directly
5. `$XDG_DATA_HOME/jellyfin`, if set
6. `$HOME/.local/share/jellyfin`

**Configuration directory**: `--configdir`, `JELLYFIN_CONFIG_DIR`, then `<Data Directory>/config` if it exists or on Windows, then `$XDG_CONFIG_HOME/jellyfin`, then `$HOME/.config/jellyfin`.

**Cache directory**: `--cachedir`, `JELLYFIN_CACHE_DIR`, `<Data Directory>/cache` on Windows, `$XDG_CACHE_HOME/jellyfin`, `$HOME/.cache/jellyfin`.

**Web directory**: `--webdir`, `JELLYFIN_WEB_DIR`, then `jellyfin-web` beside the executable. It only matters while the server hosts the web client.

**Log directory**: `--logdir`, `JELLYFIN_LOG_DIR`, then `<Data Directory>/log`.

On Windows the data folder can also be fixed with a string value `DataFolder` under `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Jellyfin\Server`; `InstallFolder` in the same key sets the install location.

Run the executable with `--help` to list every command line option.

## Checked

2026-11-03. Confirmed against the Jellyfin Configuration page, Server Paths: precedence lists for data, config, cache, web and log directories, Windows registry keys, --help. Removed: unsupported advice on pinning paths and a start-up timing claim.

Method: documentation only; no commands were run.
