---
id: computing-software.search-and-information-retrieval.apache-solr.aliases-routed
name: aliases-routed
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [aliases, createalias, routed-alias, time-routed-alias, category-routed-alias]
level: practitioner
status: docs-checked
description: "Use Solr aliases: standard CREATEALIAS for zero-downtime switches, plus routed aliases by time or category with router.start, interval, maxFutureMs, ALIASPROP and DELETEALIAS."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/alias-management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# aliases-routed

`/admin/collections?action=CREATEALIAS&name=<alias>&collections=<list>` registers or repoints an alias.

Routed aliases act as a super-collection: updates are routed to the right collection; queries go to all collections in the alias. They support up to two routing dimensions, `time` or `category`. One dimension uses `router.` parameters; two use `router.0.` and `router.1.`.

Time example parameters: `router.name=time`, `router.start=NOW/DAY`, `router.field=evt_dt`, `router.interval=+1DAY` (URL-encoded as %2B1DAY), `router.maxFutureMs=3600000`, plus `create-collection.*` settings such as `create-collection.collection.configName`.

The alias name prefixes the dependent collections, for example `timedata_2018_01_15`. When a document arrives for a window with no collection, Solr creates it (and intervening collections if the interval is shorter than `maxFutureMs`).

Routed parameters become alias properties; change them with CREATEALIAS again or with ALIASPROP, which accepts any key and value without validation. Also `LISTALIASES` and `DELETEALIAS`.

## Checked

2026-11-04. Confirmed against the Alias Management page: CREATEALIAS, routed alias dimensions and `router.` / `router.0.` prefixes, time example parameters, alias-name prefix, ALIASPROP, LISTALIASES. Removed an unsourced usage tip.

Method: documentation only; no commands were run.
