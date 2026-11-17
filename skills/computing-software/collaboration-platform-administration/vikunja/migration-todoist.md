---
id: computing-software.collaboration-platform-administration.vikunja.migration-todoist
name: migration-todoist
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, todoist-import, todoist-app-console, redirect-uri-not-configured, migration-todoist-clientid]
level: practitioner
status: docs-checked
description: "Set up the Todoist importer in Vikunja: create the Todoist app, redirect URL, client ID and secret config, run the import and clean up afterwards."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/todoist.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. In Todoist go to Settings, Integrations, Developer, Build Integrations, then Create a new app named `vikunja` with your Vikunja URL as App service URL.
2. Save the Client ID and Client secret. Set the OAuth redirect URL to `https://<your domain>/migrate/todoist` (must end with `/migrate/todoist`). Click Save settings, then Install for me.
3. Configure Vikunja: `migration.todoist.enable`, `migration.todoist.clientid`, `migration.todoist.clientsecret` (env `VIKUNJA_MIGRATION_TODOIST_CLIENTID` and `_CLIENTSECRET`). The redirect default is `<service.publicurl>/migrate/todoist`.
4. Restart (`docker compose down` then `up -d`, or `sudo systemctl restart vikunja`).
5. Avatar menu, Settings, Import from other services, click the Todoist icon. The import runs in the background, seconds to minutes.

Troubleshooting: `redirect_uri_not_configured` means the redirect URL in the Todoist App Console is wrong or the instance is not reachable (the guide says it must be publicly accessible). No Todoist icon: check env vars, that Vikunja restarted, and the logs.

Cleanup: remove the Todoist integration and the migration config, then restart.

## Checked

2026-11-04. Confirmed against the Vikunja Todoist Migration Setup page (setup/todoist: app creation, settings, install, config variables, restart commands, import steps, troubleshooting, cleanup) and config-raw.json (migration.todoist keys and the default redirect). Nothing removed.

Method: documentation only; no commands were run.
