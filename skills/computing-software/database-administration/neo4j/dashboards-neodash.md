---
id: computing-software.database-administration.neo4j.dashboards-neodash
name: dashboards-neodash
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, neodash, graph-dashboards, read-only-dashboard, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Share Neo4j dashboards with NeoDash: editor vs viewer deployment, read-only user, parameter selectors, access control, Labs support status"
sources: ["https://neo4j.com/docs/cypher-manual/current/", "https://neo4j.com/docs/operations-manual/current/", "https://github.com/neo4j-labs/neodash/blob/master/docs/modules/ROOT/pages/user-guide/publishing.adoc", "https://github.com/neo4j-labs/neodash/blob/master/docs/modules/ROOT/pages/user-guide/faq.adoc", "https://github.com/neo4j-labs/neodash/blob/master/docs/modules/ROOT/pages/user-guide/reports/parameter-select.adoc", "https://github.com/neo4j-labs/neodash/blob/master/docs/modules/ROOT/pages/user-guide/access-control.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dashboards

Goal: share graph dashboards with viewers who must not change anything.

- NeoDash builds Cypher-backed reports. It is a Neo4j Labs project (Apache 2.0): experimental, not covered by a Neo4j licence; the FAQ points production Enterprise use at a NeoDash commercial licence.
- Use two deployments. The editor (Neo4j Desktop, the hosted app, or your own) is for the build phase. A viewer deployment is standalone mode with three settings: editing disabled, one hardcoded database, one hardcoded dashboard. Published dashboards cannot be edited and viewers do not see the Cypher behind the reports.
- Connect the viewer to a dedicated read-only database user. The FAQ works with Community, on-premise and Aura, but recommends Enterprise because it allows a dedicated read-only user.
- Parameterise with a Parameter Select report, which sets a query parameter such as `$neodash_person_name`. Types: node property, relationship property, free text, date picker, custom query (receives `$input`). Options include Multiple Selection (the parameter becomes an array) and Manual Parameter Save.
- Per-dashboard access control: users with write access add labels to a dashboard; an administrator must grant privileges per role on those labels (Neo4j RBAC).

Verify: open the viewer URL, confirm no edit controls or query text appear, and confirm the database user cannot write.

## Checked
2026-11-09

Method: read the NeoDash repo docs pages publishing, faq, parameter-select and access-control (raw asciidoc). Removed: the unsupported "cache or limit heavy queries" advice. Added: editor/viewer split, Labs support status, selector types and access-control labels. Not checked: standalone-mode deployment page.
