---
id: computing-software.web-development.directus.config-files-env-file
name: config-files-env-file
category: computing-software
field: web-development
product: directus
tags: [config-path, config-file-formats, env-file-suffix, docker-secrets]
level: practitioner
status: docs-checked
description: "Configure Directus through .env, JSON, YAML or JS config files with CONFIG_PATH and load secrets from files with the _FILE suffix."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/configuration/0.intro.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All Directus configuration is environment variables. By default it reads the `.env` file next to your project's `package.json`. Change the file with `CONFIG_PATH`:

```bash
CONFIG_PATH="/path/to/config.js" npx directus start
```

Supported formats:
- `.env` (also used for any extension that is not json/yaml/js)
- `config.json` with variables as keys
- `config.yaml` or `.yml`
- `config.js` (ESM by default; `.cjs` for CommonJS) as either an object, or a function receiving `process.env` and returning the object, which lets you generate config at startup

```js
export default function (env) {
  return { HOST: "0.0.0.0", PORT: 8055, DB_CLIENT: "pg" };
}
```

Secrets from files: append `_FILE` to a Directus variable name and give a path, e.g. `DB_PASSWORD_FILE="/run/secrets/db_password"`. This pairs with Docker Secrets to keep sensitive data out of compose files.

## Checked

2026-11-04: default .env location, CONFIG_PATH, supported formats, ESM/.cjs and object/function structures, and the _FILE suffix confirmed against the Directus configuration introduction page. Removed an unsupported Verify line.

Method: documentation only; no commands were run.
