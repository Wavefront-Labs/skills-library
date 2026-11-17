---
id: computing-software.systems-network-administration.paperless-ngx.importer-restore
name: importer-restore
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, document-importer, restore, import, batch-size, migration]
level: practitioner
status: docs-checked
description: "Restore or migrate Paperless-ngx with document_importer into a completely empty install, including passphrase and batch size options."
sources:
  - "https://docs.paperless-ngx.com/administration/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing and restoring

```bash
document_importer ../export
```
Point `source` at an export directory or the generated zip. With the compose files, place the export in the `export` folder and use `../export`.

## Preconditions
- The target must be a completely empty installation, both database and directories. For a data-only import, only the database must be empty.
- Use the same Paperless version that created the export where possible. Importing from a previous version may work, but matching versions gives the best results.

## Options
| Option | Meaning |
|---|---|
| `--no-progress-bar` | hide the progress bar |
| `--data-only` | import database data only, not files or thumbnails |
| `--passphrase <PASSPHRASE>` | required if the export used one |
| `--batch-size` | records per insert batch, default 500; lower it to cut memory on very large installs |

## After restoring
- Regenerate any API tokens; the exporter never includes them.
- If the database read cache is enabled, run `python3 manage.py invalidate_cachalot` after any change made outside the application, such as restoring a database dump.
- If you exported without thumbnails or archives, the sanity checker warns about them until they are regenerated with `document_thumbnails` or `document_archiver`.

Other backup styles (volumes, folder copies plus a database dump) are restored by putting those pieces back.

## Checked
2026-11-04. Compared with Document importer, Making backups and Restoring in administration, and the read cache danger note in configuration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: usage, empty install requirement, options and batch size default, API tokens, invalidate_cachalot, sanity checker warnings. Reworded the version-matching and sanity checker lines to match the docs.

Method: documentation only; no commands were run.
