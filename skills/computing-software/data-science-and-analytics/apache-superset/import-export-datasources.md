---
id: computing-software.data-science-and-analytics.apache-superset.import-export-datasources
name: import-export-datasources
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [import-export, datasources, cli, yaml, versioned-export]
level: practitioner
status: docs-checked
description: "Move Superset databases and datasets between environments with export_datasources and import_datasources, flags, import_directory and re-encryption."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/importing-exporting-datasources.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: promote database and dataset definitions between instances.

The CLI imports and exports datasources (which include databases) as YAML, in the hierarchy databases > tables > columns and metrics.

Export:

```bash
superset export_datasources
superset export_datasources -f <filename>
```

The first prints to stdout; with `-f` the output is saved as a ZIP. Default (null) values are omitted unless you pass `-d`; pass `-b` to include back references (for example a column carrying its table id). `superset export_datasource_schema` lists every importable field. Datasources can also be exported in the UI (Sources > Databases, select items, Actions > Export to YAML); to import such a file it must be nested inside its parent element.

Import from a ZIP:

```bash
superset import_datasources -p <path / filename>
superset import_datasources -p <path / filename> -u 'admin'
```

`-u` sets the user used for the import; the default is `admin`.

Import a directory of exported assets (databases, datasets, dashboards, charts; saved queries and tags are not imported):

```bash
superset import_directory <path / directory> -u 'admin'
```

If the user does not exist the command fails immediately instead of importing without an owner.

Secrets: an exported database includes the `masked_encrypted_extra` field (service account JSON, OAuth tokens and similar). On import these values are decrypted and re-encrypted with the destination instance's `SECRET_KEY`, so the receiving instance needs a valid `SECRET_KEY` first.

Dashboard ZIP import: with overwrite enabled, existing charts with a matching UUID are replaced by the full imported configuration; without it, conflicting charts are left unchanged and skipped. UUIDs are stable across import and export, so they identify the same chart across environments.

Legacy:
- Superset 4.x.x importing from 2.x.x or 3.x.x uses `superset legacy_import_datasources -p <path or filename>` (JSON or a directory of JSON; options `-r` recursive, `-u` user).
- On 2.x.x and 3.x.x, `import_datasources` expects a ZIP when `VERSIONED_EXPORT` is True, otherwise YAML (all `yaml` or `yml` files under the path; `-r` recurses).
- The sync flag `-s columns,metrics` deletes columns and metrics not present in the YAML and can delete content of your metadata database. Without `-s`, import only adds and overrides fields.

## Checked

2026-11-08: read importing-exporting-datasources.mdx in full. Corrected the `-d` and `-b` flag meanings (they were swapped) and the `-p`/`-f` descriptions; removed `-s`/`-r` as current-version options, pipeline and rights advice not on the page. Semantic-view sections of the page are out of scope for this skill.
Method: documentation only; no commands were run.
