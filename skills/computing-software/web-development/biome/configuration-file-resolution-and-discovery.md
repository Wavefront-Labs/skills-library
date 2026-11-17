---
id: computing-software.web-development.biome.configuration-file-resolution-and-discovery
name: configuration-file-resolution-and-discovery
category: computing-software
field: web-development
product: biome
tags: [biome, config-resolution, nested-config, config-discovery, home-directory-config, xdg-config-home, biome-json-names]
level: practitioner
status: docs-checked
description: "How Biome finds its config: file name order, working directory then parents then the user config directory, with per-OS paths."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/configuration/configure-biome.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Accepted names, in priority order:** `biome.json`, `biome.jsonc`, `.biome.json`, `.biome.jsonc`.

**Discovery order:**
1. The current working directory. From the CLI that is where you run the command; from an editor it is the project root.
2. Parent folders, recursively.
3. The user config directory: `$XDG_CONFIG_HOME` or `$HOME/.config/biome` on Linux, the `Library/Application Support/biome` folder in the user's home directory on macOS, the `biome\config` folder under the user's AppData Roaming directory on Windows.

If none is found, Biome's default configuration is used.

**Example layout:**

```
app/
  backend/  biome.json, package.json
  frontend/ biome.json
    legacy/ package.json
    new/    package.json
```

Commands run in `app/backend` use `app/backend/biome.json`; commands in `app/frontend/legacy` and `app/frontend/new` use `app/frontend/biome.json`, because discovery walks upward.

Biome also supports nested `biome.json` files; see the big projects guidance (a nested file needs `"root": false`).

Glob patterns match paths relative to the configuration directory.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the unsupported 'common traps' paragraph (replaced by the documented glob-base statement) and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
