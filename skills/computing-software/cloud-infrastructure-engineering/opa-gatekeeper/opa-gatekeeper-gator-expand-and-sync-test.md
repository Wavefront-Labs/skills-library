---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-gator-expand-and-sync-test
name: opa-gatekeeper-gator-expand-and-sync-test
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, gator, gator-expand, gator-sync-test, requires-sync-data, expansiontemplate, syncset]
level: advanced
status: docs-checked
description: "Preview expanded resources with gator expand and verify data-sync configuration against template requirements with gator sync test."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/gator.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper gator expand and sync test

`gator expand` outputs the resources your ExpansionTemplates would generate. Give it a file or directory (`--filename`, `--image`, repeatable) holding the resources under test, the ExpansionTemplates, and optional mutators. Output is YAML by default or JSON, to stdout or `--outputfile`. If mutators or constraints use `match.namespaceSelector`, you must supply the resource Namespace too; a resource in a non-default namespace without its Namespace definition makes the command exit 1. It also exits 1 on parse or expansion problems.

Templates that need replicated data declare it in the annotation `metadata.gatekeeper.sh/requires-sync-data`: a JSON list of requirements, each with alternative clauses naming group, version and kind. Satisfying any one clause fulfils the requirement. The annotation is descriptive, not prescriptive: what is synced is set in SyncSet and Config resources.

`gator sync test` checks that configuration. Supply templates, a `GVKManifest` of kinds the cluster supports, and SyncSets and/or a Config. Use `--omit-gvk-manifest` to assume all kinds are supported, but then a config may cache unsupported kinds. Exit `0` means everything ingested and all requirements are fulfilled; `1` means an error or an unmet requirement.

## Checked

2026-11-04. Confirmed against gator.md (gator expand and gator sync test sections). Removed or corrected: nothing.

Method: documentation only; no commands were run.
