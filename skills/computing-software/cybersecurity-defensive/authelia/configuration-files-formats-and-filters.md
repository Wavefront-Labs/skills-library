---
id: computing-software.cybersecurity-defensive.authelia.configuration-files-formats-and-filters
name: configuration-files-formats-and-filters
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, configuration-files, yaml, toml, json, file-filters, templating, config-directory]
level: advanced
status: docs-checked
description: "Load Authelia configuration from multiple YAML, TOML or JSON files or directories, and use file filters and template functions to inject values."
sources:
  - https://www.authelia.com/configuration/methods/files/
  - https://www.authelia.com/configuration/methods/secrets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Point Authelia at configuration with `--config` (or the `X_AUTHELIA_CONFIG` environment variable); it defaults to `configuration.yml`.

```bash
authelia --config /path/to/config.yml
authelia --config /path/to/conf.d/
```

Rules from the documentation:

- A list of files and directories can be given. Directories are loaded non-recursively, and every file in them is considered configuration. Do not store unrelated files there. Individual files must not live inside a listed directory.
- Format follows the extension: `.yml`/`.yaml`, `.toml`, `.json`. Other extensions parse as YAML when named explicitly and are skipped in a directory. Formats can be mixed freely and merge as multiple files of one format do.
- If both an argument and its environment variable are set, the argument wins and the variable is ignored.
- Multiple files merge in the order given and the last duplicate key wins. Do not spread list sections such as access control rules or OpenID Connect clients across several files and expect them to merge; keeping them whole in their own file is fine. Containers look for `/config/configuration.yml` by default, and the environment variable is generally recommended in containers so other commands share the same settings.
- Files can be passed through templating filters with `--config.filters` (or `X_AUTHELIA_CONFIG_FILTERS`). The template filter exposes functions like `env`, `fileContent` and `nindent`.

```yaml
authentication_backend:
  ldap:
    address: 'ldap://{{ env "SERVICES_SERVER" }}'
    tls:
      private_key: |
        {{- fileContent "./test_resources/example_filter_rsa_private_key" | nindent 8 }}
```

`fileContent` reads a file relative to the Authelia working directory, `nindent` adds a new line and indents each line, and the leading `-` trims whitespace before the block. Filters apply in order, so the `template` filter should be the only one or the last. Filters are not covered by the standard versioning policy, the `template` filter is stable, the old `expand-env` filter was removed in v4.40.0, and `--config.filters.values` supplies `.Values` from YAML, TOML or JSON files (referencing a missing key is an error; use `index` to be optional).

Validate YAML with the published JSON schemas in your editor.

Check: run `authelia config template --config.filters=template --config=/path/to/config.yml` and read the rendered output.

## Checked

2026-11-08. Read in full: configuration/methods/files and secrets. Added merge order, filter ordering, versioning policy note and values files.

Method: documentation only; no commands were run.
