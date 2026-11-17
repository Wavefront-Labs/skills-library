---
id: computing-software.cloud-infrastructure-engineering.velero.label-selector-filtering
name: label-selector-filtering
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [label-selector, selector, or-selector, notin, phased-restore]
level: practitioner
status: docs-checked
description: "Filter backups and restores by labels with --selector and --or-selector, including notin sets, negation and the dependency exception."
sources:
  - https://velero.io/docs/main/resource-filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--selector` includes resources matching a label selector, on backup and on restore.

```bash
velero backup create NAME --selector key=value
velero backup create NAME --selector "key notin (value)"
velero restore create --from-backup NAME --selector key=value
velero restore create --from-backup NAME --selector "!key"
```

`notin` also matches resources that lack the label key entirely, so it restores resources with any other value plus those without the key. `!key` restores only resources that do not have that label key. Set-based selectors suit phased restores: labelled resources first, then everything else.

Exception: resources pulled in as dependencies by restore item actions (a restored pod service account or its PVCs) are restored even if the selector would exclude them.

`--or-selector` includes resources matching at least one selector in a list. The separator is the literal text ` or `, not an operator. It cannot be used together with `--selector`.

```bash
velero backup create backup1 --or-selector "foo=bar or baz=qux"
velero restore create restore-prod --from-backup=prod-backup \
  --or-selector "env in (prod,production) or environment in (prod, production)"
```

## Checked

Checked 2026-11-08 against the Velero Resource filtering page (raw markdown, read in full): the `--selector` and `--or-selector` sections, notin and negation behaviour and the dependency note. All claims confirmed; nothing removed.

Method: documentation only; no commands were run.
