---
id: computing-software.data-science-and-analytics.apache-superset.architecture-components
name: architecture-components
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [architecture, components, metadata-database, cache-layer, workers]
level: intro
status: docs-checked
description: "Plan a Superset deployment from its parts: application, metadata database, cache layer, workers and beat, and which features need which."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/installation/architecture.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know which components a Superset install needs.

Components:
- **Superset application**: Python (Flask) backend, API layer and React frontend built with Webpack, plus static assets. A chart or dashboard view triggers a SQL query against the data warehouse and the result is rendered as a visualization.
- **Metadata database**: stores chart and dashboard definitions, user information and logs. Tested with PostgreSQL and MySQL. Quickstart and PyPI installs default to on-disk SQLite, and Docker Compose uses a PostgreSQL container volume; neither is recommended for production. Use a managed standalone database and back it up regularly.
- **Caching layer** (optional but necessary for some features): stores query results so a second chart load comes from cache, and acts as the message broker for the worker. Most people use Redis; other options are supported.
- **Worker and beat** (optional but necessary for some features): workers run tasks such as async queries and report snapshots and emails; beat is the scheduler that tells workers when to run tasks. Most installations use Celery.

Features that need the optional components: Alerts and Reports, caching, async queries, dashboard thumbnails.

Install method matters: Kubernetes and Docker Compose create all components; a PyPI install creates only the application, so you must configure the cache, worker and beat yourself (the page says this is not currently covered in the docs).

Other components such as a load balancer or reverse proxy for HTTPS, or a Mapbox URL for geospatial charts, are covered on the Configuration page, and Superset will not start without certain configuration settings.

## Checked

2026-11-08: read architecture.mdx in full. Removed claims not on the page: Gunicorn, Redis versus RabbitMQ, results backend, "exactly one beat", headless browser and scaling rules.
Method: documentation only; no commands were run.
