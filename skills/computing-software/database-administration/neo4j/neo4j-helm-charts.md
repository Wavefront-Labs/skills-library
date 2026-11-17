---
id: computing-software.database-administration.neo4j.neo4j-helm-charts
name: neo4j-helm-charts
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, helm-chart, neo4j-statefulset, persistent-volume, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Kubernetes deployment"
sources:
  - https://neo4j.com/docs/operations-manual/current/kubernetes/quickstart-standalone/install-neo4j/
  - https://neo4j.com/docs/operations-manual/current/kubernetes/helm-charts-setup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Neo4j Helm charts

Goal: deploy Neo4j on Kubernetes.
- Install with the official chart: `helm install my-neo4j neo4j/neo4j --namespace neo4j -f values.yaml`.
- Settings, volumes and credentials are given in the values file; see the Kubernetes configuration and persistent volumes pages.
Verify: pod ready and `cypher-shell` connects via service.

## Checked

2026-11-02. Confirmed in the Kubernetes quickstart pages (`helm install ... neo4j/neo4j -f values.yaml`). Removed: cluster chart names, request/limit advice and PV speed advice (not confirmed).
Method: documentation only; no commands were run.
