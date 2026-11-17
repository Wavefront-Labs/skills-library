---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-architecture
name: woodpecker-architecture
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [architecture, server, agent, autoscaler]
level: intro
status: docs-checked
description: "Understand Woodpecker server, agent and autoscaler roles, database default and parallelism."
sources: ["https://woodpecker-ci.org/docs/administration/general"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker architecture

Woodpecker has two essential components and one optional one.

- The server provides the UI, processes webhooks from the forge, serves the API and analyzes the pipeline YAML. It also sends status back to the forge.
- The agent executes workflows through a backend (Docker, Kubernetes or local) and connects to the server over gRPC. Several agents can coexist, so job limits and backend choice can be tuned per agent.
- The optional autoscaler starts cloud VMs to process pending builds and destroys them afterwards.

Parallelism: add more agents, or raise `WOODPECKER_MAX_WORKFLOWS` on an agent. It defaults to 1.

Database: SQLite by default with no configuration. For larger instances use PostgreSQL or MariaDB.

Users are not stored natively: they come from your forge through OAuth2, and the forge is also used to report pipeline status.

Terms to keep straight: a pipeline is a sequence of workflows triggered by an event; a workflow is a YAML file of steps and services with its own isolated workspace; a step runs in a container; a service is a step that runs from the start to the end of a workflow and is reachable by name; a task is a workflow waiting in the queue.

Agents and server share a secret (`WOODPECKER_AGENT_SECRET`) and the agent addresses the server's gRPC port, 9000 by default.

## Checked

2026-11-03. Read the Woodpecker general administration page and confirmed server, agent and optional autoscaler roles and gRPC connection. Nothing removed. 

Method: documentation only; no commands were run.
