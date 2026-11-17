---
id: computing-software.web-development.strapi.config-dump-restore
name: config-dump-restore
category: computing-software
field: web-development
product: strapi
tags: [strapi, configuration-dump, configuration-restore, migration, production, cli]
level: practitioner
status: docs-checked
description: "Move stored configuration between Strapi environments with configuration:dump and configuration:restore and its three strategies."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# configuration:dump and configuration:restore

## Dump (alias `config:dump`)
Dumps configuration as a JSON array to a file or stdout, to help migrate to production.

```bash
strapi configuration:dump -f dump.json
strapi config:dump > dump.json
```

Options: `-f, --file <file>` (default stdout), `-p, --pretty`.

Credentials entered for third-party services (e.g. auth providers) are also dumped. Avoid committing the file; instead copy it directly to the target environment, store it securely and download at deploy time, or encrypt it before committing.

## Restore (alias `config:restore`)
Input must be a JSON array.

```bash
strapi configuration:restore -f dump.json
strapi config:restore --file dump.json -s replace
cat dump.json | strapi config:restore
```

Options: `-f, --file <file>` (default stdin), `-s, --strategy <strategy>`: `replace` (default), `merge`, `keep`.

- replace: create missing keys, replace existing ones.
- merge: create missing keys, merge existing keys with the new value.
- keep: create missing keys, keep existing ones as is.

## Checked

Checked 2026-11-04 against the Strapi CLI page (Configuration section: dump, restore, options, strategies, credentials caution). Nothing removed.

Method: documentation only; no commands were run.
