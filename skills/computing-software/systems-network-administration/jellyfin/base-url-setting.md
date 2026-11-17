---
id: computing-software.systems-network-administration.jellyfin.base-url-setting
name: base-url-setting
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, base-url, subpath, reverse-proxy, android-tv, 404]
level: advanced
status: docs-checked
description: "Serve Jellyfin under a path such as /jellyfin with the Base URL setting and avoid its redirect and client caveats."
sources: ["https://jellyfin.org/docs/general/post-install/networking/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Base URL

Jellyfin can run under a path like `https://example.com/jellyfin`. The Base URL setting is a URL prefix added to every path: with Base URL `/jellyfin`, `http://myserver/web/index.html` becomes `http://myserver/jellyfin/web/index.html`. It helps to run several instances under one domain, or when Jellyfin lives at a subpath beside other services.

The value is normalised to include a leading `/`. Changing it requires a server restart, so existing paths stay valid until you are ready.

**Caution:** the Base URL is known to break HDHomeRun, the DLNA plugin, Sonarr, Radarr and MrMC.

**Three caveats**
1. Changing the Base URL (`/` to `/baseurl`, or `/baseurl` to `/newbaseurl`) is handled by automatic redirects. Removing it entirely (empty value) is not: all URLs with the old path throw 404 errors.
2. Clients generally do not follow Base URL redirects. In the Android TV app the `Host` setting must include it, such as `http://myserver:8096/baseurl`, or the connection fails.
3. Reverse proxy configurations must be updated. Generally passing `/` back to Jellyfin works in all cases and paths are normalised; this is the standard configuration in the docs' examples. Take care with more advanced routing.

Check: after the restart open the new prefixed URL and a client login.

## Checked

2026-11-08. Confirmed against the Jellyfin Networking page: Base URL prefix example, use cases, leading slash normalisation, restart requirement, broken integrations, three caveats including 404 on removal and the Android TV Host setting. Page read in full.

Method: documentation only; no commands were run.
