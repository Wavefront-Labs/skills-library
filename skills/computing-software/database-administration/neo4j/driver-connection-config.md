---
id: computing-software.database-administration.neo4j.driver-connection-config
name: driver-connection-config
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, connection-pool, neo4j-scheme, driver-timeouts, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Config"
sources: ["https://neo4j.com/docs/python-manual/current/connect-advanced/", "https://neo4j.com/docs/python-manual/current/connect/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection URIs and lifecycle

Goal: configure connections.
- Schemes: `neo4j`, `neo4j+s`, `neo4j+ssc`, `bolt`, `bolt+s`, `bolt+ssc`. `neo4j+s` accepts only CA-signed certificates and is the Aura default; `neo4j+ssc` also accepts self-signed ones.
- The scheme is dictated by the server; ask the administrator if unsure.
- Always close the driver, either with `with GraphDatabase.driver(URI, auth=AUTH) as driver:` or `Driver.close()`.
Verify: the driver connects with the expected encryption and is closed on shutdown.

## Checked

2026-11-02. Confirmed in the Python driver connect and advanced connection pages. Removed: pool size, acquisition timeout and retry-time tuning (setting names not read).
Method: documentation only; no commands were run.
