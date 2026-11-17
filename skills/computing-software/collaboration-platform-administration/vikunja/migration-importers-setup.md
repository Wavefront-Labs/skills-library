---
id: computing-software.collaboration-platform-administration.vikunja.migration-importers-setup
name: migration-importers-setup
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, migrators, oauth-importers, planka-import, file-imports, migration-limits]
level: practitioner
status: docs-checked
description: "Enable Vikunja's importers: OAuth sources, Planka and file imports, the public URL requirement, SSRF block for LAN Planka, and the migration.* limits."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/migration.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sources and method: Todoist, Trello and Microsoft To Do (OAuth); Planka (server URL and credentials); TickTick, WeKan, CSV and Vikunja export (file upload).

OAuth importers need credentials and `migration.<service>.enable: true` in config. The OAuth redirect happens in the browser, so the instance only needs to be reachable from that browser, but `service.publicurl` must be right so the redirect URL works. (The Todoist guide separately says the instance must be publicly accessible.) Default redirect URLs end in `/migrate/todoist`, `/migrate/trello`, `/migrate/microsoft-todo`.

Planka needs no setup, but outgoing requests use the SSRF-safe client, which refuses non-routable addresses. Planka on the same host or LAN fails until `outgoingrequests.allownonroutableips` is true, loosening protection for all outgoing requests.

Users start via Settings, Import from other services, pick the service, Get Started. If an icon is missing, check the config was loaded in the Vikunja log. OAuth errors usually mean the Vikunja domain is not in the service's allowed redirects or origins. Large accounts can take hours.

Limits: `migration.maxcsvrows` 100000, `migration.maxitems` 100000, `migration.vikunjafile.maxsize` 256MB, `maxfiles` 10000, `maxuserstorage` 1GB, `migration.claimtimeout` 5m.

## Checked

2026-11-04. Confirmed against the Vikunja Migration from third-party services page (setup/migration: sources and methods, OAuth prerequisites, Planka SSRF warning, settings path, redirect errors, duration) and config-raw.json (default redirect URLs, enable keys and the limit defaults), plus the Todoist guide for its public accessibility warning. Nothing removed.

Method: documentation only; no commands were run.
