---
id: computing-software.web-development.directus.config-type-casting-syntax
name: config-type-casting-syntax
category: computing-software
field: web-development
product: directus
tags: [env-type-casting, syntax-prefix, double-underscore-nesting, env-object-syntax]
level: advanced
status: docs-checked
description: "Control how Directus parses environment variables: automatic type casting, explicit type prefixes, double-underscore nesting and wildcard object variables."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/configuration/0.intro.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Automatic casting by value shape:

```
DB_HOST="3306"                    -> 3306
CORS_ENABLED="false"              -> false
STORAGE_LOCATIONS="s3,local,example" -> ["s3","local","example"]
```

Force a type with a prefix: `string:`, `number:`, `regex:`, `array:`, `json:`.

```
number:3306
regex:\.example\.com$
array:https://example.com,https://example2.com
array:string:https://example.com,regex:\.example3\.com$
json:{"items": ["example1", "example2"]}
```

Explicit casting also works with values read via the `_FILE` suffix.

When variables become config objects for libraries (`DB_*`, `REDIS_*`), names become camelCase, and a double underscore nests:

```
DB_CONNECTION_STRING="postgresql://postgres:example@127.0.0.1"
DB_SSL__REJECT_UNAUTHORIZED="false"
```

gives `{ connectionString: ..., ssl: { rejectUnauthorized: false } }`.

For docs variables ending in `*` (e.g. `MY_ENV_*`): `MY_ENV_MAX_LENGTH=1` becomes `{ maxLength: 1 }`, `MY_ENV_BRAND__COLOR=red` becomes `{ brand: { color: 'red' } }`.

## Checked

2026-11-04: automatic casting examples, the five syntax prefixes, double-underscore nesting with camelCase, _FILE casting and the object syntax confirmed against the Directus configuration introduction page. Removed an unsupported Verify line.

Method: documentation only; no commands were run.
