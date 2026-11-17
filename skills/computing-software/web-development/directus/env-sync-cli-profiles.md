---
id: computing-software.web-development.directus.env-sync-cli-profiles
name: env-sync-cli-profiles
category: computing-software
field: web-development
product: directus
tags: [env-sync-cli, d6s-profile, directus-config-json, credential-store]
level: practitioner
status: docs-checked
description: "Install the Directus Environment Sync CLI (d6s) and add connection profiles that keep URLs in directus.config.json and tokens in a private credential store."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/10.environment-sync/1.quickstart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: Docker (for the quickstart), Node.js 22 or later, git. Source and target must run the same Directus version (patch included) and the same database vendor; pin one explicit version everywhere.

```bash
npm install -g @directus/cli@12
d6s --version
```

Pin to major 12: the unpinned name has a deprecated 9.x package. It installs two equal commands, `directus-cli` and `d6s`.

Add a profile per instance (name + URL + token):

```bash
d6s profile add source --url http://localhost:8055 --token source-token
d6s profile add target --url http://localhost:8056 --token target-token
d6s profile test-connection source
```

The first add creates `directus.config.json` with only name, url and `auth: { type: token }`. Tokens go to a user-only credentials file under your home `.directus` directory, so commit the config but never the credentials.

The quickstart shows `test-connection` printing that it authenticated to the URL as the admin user.

Next: the pull, diff and push loop skill.

## Checked

2026-11-04: Node.js 22 requirement, same-version and same-vendor rule, npm install command, d6s and directus-cli aliases, profile add and test-connection commands, directus.config.json contents and credentials location confirmed against the Directus Environment Sync quickstart. Replaced a Verify line with the page's example output.

Method: documentation only; no commands were run.
