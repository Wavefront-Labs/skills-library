---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-addons
name: woodpecker-addons
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [addons, addon-forge, log-store]
level: sme
status: docs-checked
description: "Load experimental Woodpecker addon forges and log stores from external binaries."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/addons", "https://woodpecker-ci.org/docs/development/addons"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker addons

Addons extend the server. Currently they can provide forges and the log service. Addon forges are experimental and their implementation can change and break at any time. You must trust the author: an addon forge may see authentication codes and other sensitive information.

Addon forge: download the right addon version and point the server at the file.

```ini
WOODPECKER_ADDON_FORGE=/path/to/your/addon/forge/file
```

In containers, mount the addon binary at `/opt/addons/`.

Log store addon:

```ini
WOODPECKER_LOG_STORE=addon
WOODPECKER_LOG_STORE_FILE_PATH=/path/to/your/addon/forge/file
```

An example addon forge is the Radicle addon for peer-to-peer, Git-based code collaboration.

Addons are written in Go, use RPC to talk to the server via the go-plugin library, and import Woodpecker's Go packages. They run as a separate process, so they cannot read the server configuration and must parse their own environment variables. Addon logs carry a field `addon` with the addon file name; report addon bugs to the addon's repository, not the main one.

## Checked

2026-11-08. Read the Woodpecker addons administration page and the addons development page in full (raw markdown). Confirmed experimental warning, trust warning, WOODPECKER_ADDON_FORGE, /opt/addons/ mount, log store addon variables, Radicle example. Removed: built-in log store options (database, file), when-to-use-addons advice, and custom agent / core.RunAgent text, none of which the cited page states. Added the development-page facts (go-plugin RPC, separate process, addon log field). Added the development page to sources.

Method: documentation only; no commands were run.
