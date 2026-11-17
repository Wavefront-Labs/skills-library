---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-component-controller
name: grafana-alloy-component-controller
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [component-controller, dag, reevaluation, component-health, in-memory-traffic, sighup, serverhttpmemory-addr]
level: practitioner
status: docs-checked
description: "How the Alloy component controller builds a DAG, evaluates and reevaluates components, tracks health, keeps last good config on failure, and reloads."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/get-started/components/component-controller.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The component controller

The controller reads and validates the config, manages component lifecycle, evaluates arguments and reports health.

## Graph and evaluation
References between components form a Directed Acyclic Graph. The graph validates references and sets evaluation order: a component is evaluated only after its dependencies, and independent components can evaluate in parallel at startup. Self references (`filename = local.file.self_reference.content`) and cycles (a references b, b references a) make the config invalid.

When a component updates its exports (a `local.file` whose file changed), the controller reevaluates all dependents, cascading until nothing else changes.

## Health
States: **Unknown** (created, not started), **Healthy**, **Unhealthy**, **Exited**. Health combines evaluation health, runtime health and component-specific health (`local.file` is unhealthy if its file is deleted). A component's health is independent of the components it references.

## Failure behaviour
If evaluation fails, the component is marked unhealthy and the reason is logged, but it keeps running with its last valid configuration. Scrapers keep using the last discovered targets if `discovery.kubernetes` loses the API server.

## In-memory traffic
Components that expose HTTP endpoints and opt in (such as `prometheus.exporter.unix`) can communicate in-process, skipping the network, auth and TLS. The internal address defaults to `alloy.internal:12345`; change it with `--server.http.memory-addr` if it clashes.

## Reload
The `/-/reload` HTTP endpoint and `SIGHUP` reload the config file. Removed components are stopped, new ones created, and all components reevaluated.

## Checked

2026-11-08. Read the Component controller page in full. Confirmed: DAG purpose, invalid self and cyclic references, evaluation order and parallel startup, reevaluation cascade, the four health states and their inputs, independence of health from referenced components, last-valid-configuration behaviour on failure, in-memory traffic with the default `alloy.internal:12345` and `--server.http.memory-addr`, and reload through `/-/reload` and SIGHUP.

Method: documentation only; no commands were run.
