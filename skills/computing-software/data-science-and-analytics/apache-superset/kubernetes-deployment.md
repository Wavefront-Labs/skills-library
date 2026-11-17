---
id: computing-software.data-science-and-analytics.apache-superset.kubernetes-deployment
name: kubernetes-deployment
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [kubernetes, helm, operator, deployment, containers]
level: practitioner
status: docs-checked
description: "Choose a Kubernetes route for Superset: the Helm chart is deprecated in favour of the Superset Kubernetes Operator; plan components accordingly."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/installation/kubernetes.mdx
  - https://github.com/apache/superset/blob/master/docs/admin_docs/installation/architecture.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the supported way to run Superset on Kubernetes.

The installation page says Kubernetes is supported through the official Apache Superset Kubernetes Operator, and that the Helm chart under `helm/superset` is deprecated and not recommended for new deployments. The operator documentation is the source of truth: installing the operator, defining Superset deployments with custom resources, configuring dependencies, upgrades and operations.

- New deployments: start with the operator documentation.
- Existing Helm deployments: plan a migration to the operator using the Helm chart migration guide; until then the deprecated chart README holds the legacy reference.

What any deployment contains (architecture page): the Superset application, a metadata database, a caching layer and a worker plus beat. The last two are optional but necessary for Alerts and Reports, caching, async queries and dashboard thumbnails. Installing with Kubernetes or Docker Compose creates all of these components; a PyPI install creates only the application.

Metadata database: Superset is tested with PostgreSQL and MySQL. For production the docs recommend a properly configured, managed, standalone database that you back up regularly (SQLite and the Docker Compose container volume are not recommended for production).

## Checked

2026-11-08: read kubernetes.mdx and architecture.mdx in full. Removed claims not on those pages: Ingress and proxy-fix settings, Secrets handling, Chromium on workers, db upgrade job, probes and scaling tips.
Method: documentation only; no commands were run.
