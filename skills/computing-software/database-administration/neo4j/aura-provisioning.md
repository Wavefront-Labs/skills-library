---
id: computing-software.database-administration.neo4j.aura-provisioning
name: aura-provisioning
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, aura, auradb, provisioning, bolt-uri, cypher-shell, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Create a Neo4j AuraDB instance, save its generated credentials, and connect with the neo4j+s URI from Browser, Workspace or cypher-shell."
sources: ["https://neo4j.com/docs/aura/auradb/getting-started/create-database/", "https://neo4j.com/docs/aura/auradb/getting-started/connect-database/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provisioning Aura instances

Goal: use managed Neo4j.
- Open the Aura Console, choose New Instance, and create an AuraDB Free, Professional or Enterprise instance. Only one AuraDB Free instance is allowed per account.
- Professional: pick the cloud provider, region and instance size (the console shows the running cost; tick the confirmation), then set the instance name and Neo4j version. Enterprise sizing and pricing follow your contract.
- Copy the generated Username and password, or download the credentials as a text file, before continuing. They are the credentials used to connect.
- Connect using the Connection URI shown under the instance status. It has the form `neo4j+s://<id>.databases.neo4j.io`.
- Ways in: the Query button (Browser), Explore (Bloom), Open (Workspace), Neo4j Desktop as a remote connection, or `./cypher-shell -a <connection_uri> -u <username> -p <password>`.
Verify: the driver or cypher-shell connects over the neo4j+s URI.

## Checked

2026-11-09. Confirmed against the neo4j/docs-aura sources for create-database and connect-database, and the migration page for the URI form. Removed: "plan backup retention by tier" and the "confirm current tiers" hedge (not on these pages; tiers named are the three the create page covers), and the draft disclaimer.

Method: documentation only; no commands were run.
