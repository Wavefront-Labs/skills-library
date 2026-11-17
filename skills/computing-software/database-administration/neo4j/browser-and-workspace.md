---
id: computing-software.database-administration.neo4j.browser-and-workspace
name: browser-and-workspace
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, browser, workspace, bloom, http-port, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Know which ports Neo4j Browser uses, how Workspace differs from Browser and Bloom, and how to open each against Aura."
sources: ["https://neo4j.com/docs/operations-manual/current/configuration/ports/", "https://neo4j.com/docs/aura/auradb/getting-started/connect-database/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Neo4j Browser and Workspace

Goal: explore interactively.
- Neo4j Browser uses the HTTP connector (default port 7474, unencrypted, enabled by default) or HTTPS (7473, disabled by default), and Bolt on 7687 (also used by cypher-shell and the drivers; encryption off by default).
- When exposing network services, protect them: the ports page gives no firewall recommendation beyond that.
- Neo4j Workspace combines Browser, Bloom and Data Importer in one interface. On Aura it is on by default for AuraDB Free and Professional, and must be switched on (Settings, Enable workspace) for Enterprise.
- On Aura, open Browser with Query, Bloom with Explore, Workspace with Open.
- Bloom Perspectives are stored in the user's browser local storage on AuraDB, so share them by export and import.
Verify: only the ports you intend are reachable, and visual queries use LIMIT.

## Checked

2026-11-09. Confirmed against the operations manual Ports page (docs-operations configuration/ports) and the AuraDB Connecting to an instance page (docs-aura). Removed: Browser commands (`:play`, `:param`, saved scripts) and the result node-limit claim (Browser manual not checked), the claim that Browser speaks to Bolt from the client machine, and "Workspace/Explore/Query are newer (confirm)". The LIMIT tip is advice, not a documented figure.

Method: documentation only; no commands were run.
