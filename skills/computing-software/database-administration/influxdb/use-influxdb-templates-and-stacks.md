---
id: computing-software.database-administration.influxdb.use-influxdb-templates-and-stacks
name: use-influxdb-templates-and-stacks
category: computing-software
field: database-administration
product: influxdb
tags: [templates, stacks, influx-apply, export, community-templates]
level: practitioner
status: docs-checked
description: "Apply, validate and export InfluxDB templates, and track installed resources with stacks."
sources:
  - https://docs.influxdata.com/influxdb/v2/tools/influxdb-templates/use/
  - https://docs.influxdata.com/influxdb/v2/tools/influxdb-templates/create/
  - https://docs.influxdata.com/influxdb/v2/tools/influxdb-templates/stacks/init/
  - https://docs.influxdata.com/influxdb/v2/tools/influxdb-templates/stacks/update/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```sh
influx template -f template.yml                 # summarise
influx template validate -f template.yml
influx apply -o ORG -f template.yml [--stack-id ID] [--force yes] [--secret=KEY=VALUE]
influx export all -o ORG -t TOKEN -f out.yml
influx stacks init -o ORG -n NAME -d DESCRIPTION -u URL
```

`-f` takes a file and `-u` a URL (both repeatable). `influx apply` prompts for confirmation unless `--force yes`. Applying without a stack ID initialises a new stack and all new resources; supplying `--stack-id` updates the existing stack, and InfluxDB updates, adds and removes resources to resolve differences. Template resources are identified by `metadata.name`. Community templates are hosted in the influxdata/community-templates repository (raw base: https://raw.githubusercontent.com/influxdata/community-templates/master/).

## Checked

Method: docs-checked 2026-11-09 against the Use templates page (summary, validate, apply sections), the export portions of the Create templates page, and the stacks init and update pages. Dropped the unconfirmed rollback claim and the `influx stacks remove` line, which none of the four pages documents beyond a nav link.
