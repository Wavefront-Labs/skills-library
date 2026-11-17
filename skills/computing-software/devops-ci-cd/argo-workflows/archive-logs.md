---
id: computing-software.devops-ci-cd.argo-workflows.archive-logs
name: archive-logs
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [archive-logs, archive-location, log-archival, logging-links, artifact-repository]
level: practitioner
status: docs-checked
description: "Turn on archiveLogs at controller, workflow or template level, understand the precedence table, and link the UI to a real logging stack."
sources: ["https://argo-workflows.readthedocs.io/en/latest/configure-archive-logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Archive pod logs
Logs are saved as an artifact, so an artifact repository must be configured. The docs warn against relying on this: it is a naive convenience for viewing logs of garbage-collected Pods in the UI, not an indexing or search system.

Set it in three places:
- controller ConfigMap `archiveLogs`
- Workflow: `spec.archiveLogs: true`
- template: `archiveLocation: {archiveLogs: true}`

Precedence is controller ConfigMap > Workflow spec > template. Controller true always archives. With the controller false, the template value decides: Workflow true with template true archives, Workflow true with template false does not, Workflow false with template true archives, and all false does not.

Alternatives the page suggests: fluentd or promtail to collect, ELK or loki to store and query, grafana for UI. Connect the Argo UI to them with `links` in the controller ConfigMap, using `scope: workflow` for a Workflow's logs and `scope: pod-logs` for a specific Pod. Parametrise URLs with `${metadata.name}`, `${metadata.namespace}`, `${metadata.labels}` and other metadata.

## Checked
2026-11-03. Confirmed against the Argo Workflows Configuring Archive Logs page: the not-recommended warning, the three configuration points, the full precedence table, the suggested alternatives and the link scopes. Removed the earlier loose precedence wording and replaced it with the table.
Method: documentation only; no commands were run.
