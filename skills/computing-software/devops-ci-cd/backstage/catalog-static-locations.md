---
id: computing-software.devops-ci-cd.backstage.catalog-static-locations
name: catalog-static-locations
category: computing-software
field: devops-ci-cd
product: backstage
tags: [catalog-locations, url-locations, file-locations, backstage]
level: practitioner
status: docs-checked
description: "Register catalog-info.yaml files with catalog.locations in app-config using url and file location types."
sources:
  - https://backstage.io/docs/features/software-catalog/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The simplest way to feed the catalog is declarative locations in `app-config.yaml`:

```yaml
catalog:
  locations:
    - type: url
      target: https://github.com/example-org/artist-web/blob/main/catalog-info.yaml
    - type: file
      target: ../../examples/all.yaml
```

- `url` locations are handled by the built-in `UrlReaderProcessor`, which needs a matching entry under `integrations` (for example GitHub) to know how to fetch the URL.
- `file` locations read from the local filesystem. Use them only for development, tests and example data, never production. They do not support `$text`, `$json` or `$yaml` placeholders, though you can reference other files relative to the current one. The path is relative to the backend's working directory, typically `packages/backend/`.
- Inside a container built from the default image the path is relative to the image root, such as `./examples/all.yaml`, and the files must be present in the image.

Locations added through static configuration cannot be removed through the catalog locations API; remove them from the config.

Errors in a `catalog-info.yaml` are logged and do not abort processing. If two files declare the same `metadata.name`, one is processed and the rest are skipped with a log message.

## Checked

2026-11-03. Confirmed on the catalog configuration page: `catalog.locations` with `url` and `file` types, `UrlReaderProcessor` needing an integration, `file` locations only for development and examples, no `$text`/`$json`/`$yaml` placeholders in them, the path relative to the backend working directory (typically `packages/backend/`), the container path form `./examples/all.yaml` with files copied into the image, static locations not removable through the locations API, errors logged without aborting, and duplicate `metadata.name` handling. Removed: the advice to prefer discovery providers.

Method: documentation only; no commands were run.
