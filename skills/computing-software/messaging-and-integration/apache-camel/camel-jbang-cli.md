---
id: computing-software.messaging-and-integration.apache-camel.camel-jbang-cli
name: camel-jbang-cli
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, camel-cli, jbang, dev-mode, export]
level: intro
status: docs-checked
description: "Camel CLI (JBang): install options, camel init, run and run --dev, export to Spring Boot, Quarkus or Main, ps, log and trace, and why it is not for production."
sources:
  - https://camel.apache.org/manual/camel-jbang.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Camel CLI (Camel JBang)

A development tool for developers and AI agents, not for running integrations in production: it has no security or permissions, so anyone running as the same user has full control. For production use `camel export` to generate a Spring Boot, Quarkus or Camel Main project.

Install:
- JBang: `jbang app install camel@apache/camel`
- Linux/macOS script: `curl -fsSL https://camel.apache.org/install.sh | sh` (latest release; add `-s -- --version LTS` for the newest LTS, and `camel self-update` then stays on LTS)

Commands:
- `camel init hello.yaml` creates a starter route.
- `camel run hello.yaml` resolves and caches the needed Camel JARs from Maven (components are auto-detected) and runs the routes.
- `camel run hello.yaml --dev` runs with live reload.
- `camel export` generates a Maven project.
- `camel get`, `camel ps`, `camel log`, `camel trace` inspect running integrations through a local connector.

Routes can be YAML, Java or XML. Also available: Dev Services (local databases and brokers via Camel test-infra and containers), validation of routes and properties before running, health checks, metrics, message history, a Camel TUI dashboard and a Camel CLI MCP server exposing the catalog to AI assistants.

There is no `camel dev` command on the page; dev mode is the `--dev` flag. Full flags are in the Command Reference.

Verify: `camel init hello.yaml && camel run hello.yaml` starts and logs the sample route.

## Checked

Method: docs-checked 2026-11-09 against the full Camel CLI overview page (read as its raw AsciiDoc source in the apache/camel repository, which builds camel.apache.org/manual/camel-jbang.html). Subpages and the command reference were not read.
