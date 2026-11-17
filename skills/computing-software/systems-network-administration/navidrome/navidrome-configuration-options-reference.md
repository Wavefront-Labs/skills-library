---
id: computing-software.systems-network-administration.navidrome.navidrome-configuration-options-reference
name: navidrome-configuration-options-reference
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, navidrome-toml, nd-environment-variables, musicfolder, datafolder, baseurl, address, port, sessiontimeout, config-file]
level: practitioner
status: docs-checked
description: "Find and set Navidrome options in navidrome.toml or ND_ environment variables: paths, network binding, base URL, scanner schedule and watcher, caches, UI defaults and toggles."
sources: ["https://www.navidrome.org/docs/usage/configuration/options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome configuration options

Every option can be set in the config file (`navidrome.toml`, default `./navidrome.toml`, or `-c/--configfile`) or as an environment variable `ND_<OPTION>` with dots turned into underscores (`Backup.Path` becomes `ND_BACKUP_PATH`). Two cannot be set by env var: `Tags` and `Jukebox.Devices`. Precedence is environment variables, then command-line arguments (all lowercase), then the config file. Docker installations automatically look for `navidrome.toml` in `/data`.

Basics: `MusicFolder` (may be read-only, becomes library 1), `DataFolder`, `CacheFolder`, `LogLevel` (`error`, `warn`, `info`, `debug`, `trace`), `LogFile` (otherwise stderr), `Address` (default all IPs; IPv4, IPv6 or `unix:/path/to/file`), `Port` (4533), `BaseUrl` (for proxies: `/music` or a full URL), `TLSCert` and `TLSKey`, `UnixSocketPerm`, `SessionTimeout`, `EnforceNonRootUser`.

Scanner:
- `Scanner.Schedule` (cron syntax), `Scanner.ScanOnStartup`, `Scanner.WatcherWait` (wait after a change before scanning; `0` disables the watcher), `Scanner.FollowSymlinks`, `Scanner.IgnoreDotFolders`, `Scanner.PurgeMissing` (`never`, `always`, `full`), `Scanner.ArtistJoiner`, `Scanner.ArtistSplitExceptions`.
- Search: `Search.Backend` (`fts` for FTS5 with BM25 ranking, or `legacy`) and `Search.FullString`.

Caches: `ImageCacheSize`, `TranscodingCacheSize` (`"0"` disables), `EnableArtworkPrecache`.

UI and features toggles: `EnableSharing`, `EnableDownloads`, `EnableFavourites`, `EnableStarRating`, `EnableUserEditing`, `EnableReplayGain`, `EnableNowPlaying`, `EnableGravatar`, `EnableExternalServices` (false disables all integrations), `EnableLogRedacting`, `DefaultTheme`, `DefaultLanguage`, `UIWelcomeMessage`, `ShareURL`.

Integrations: `LastFM.*`, `ListenBrainz.*`, `Deezer.*`, `Jellyfin.*`, `Jukebox.*`, `Prometheus.*`, `Plugins.*`, `Backup.*`, `PID.*`, `ExtAuth.*`, `Subsonic.*`, `Transcoding.*`.

`Tags` and `Jukebox.Devices` need the config file.

Verify: `navidrome --help` lists the command-line flags, such as `--musicfolder` and `--datafolder`.

## Checked

2026-11-04. Confirmed against the Navidrome Configuration Options page: env var naming, the two file-only options, basics, scanner, search, cache, toggle and integration option names, defaults and values. Fixed the Docker config file claim (the page says Docker installations look in `/data` automatically). Removed the unconfirmed claims that settings are logged at startup and that environment variables are easiest in containers.

Method: documentation only; no commands were run.
