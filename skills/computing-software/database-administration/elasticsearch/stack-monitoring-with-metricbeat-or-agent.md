---
id: computing-software.database-administration.elasticsearch.stack-monitoring-with-metricbeat-or-agent
name: stack-monitoring-with-metricbeat-or-agent
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, stack-monitoring, metricbeat, elastic-agent, monitoring-cluster, elasticsearch-operations]
level: practitioner
status: docs-checked
description: "Set up Elastic Stack Monitoring with Metricbeat or Elastic Agent to a separate monitoring cluster: scope, roles, ingest node."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/monitoring-production.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/configuring-metricbeat.html
  - https://www.elastic.co/guide/en/kibana/current/kibana-alerts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stack Monitoring with Metricbeat / Elastic Agent

**Goal:** monitoring data that survives the production cluster's failure, shown in Kibana's Monitoring UI.

## Architecture
- Production cluster(s) -> collector (Elastic Agent, recommended, or Metricbeat) -> a **separate monitoring cluster** -> Kibana Monitoring UI.
- In production, send data to a separate monitoring cluster so historical data stays available when the monitored nodes are not, and so monitoring does not load the production cluster.
- Legacy collection methods are deprecated and should not be used.
- The monitoring cluster needs at least one ingest node, because the monitoring features use ingest pipelines.

## Metricbeat
```bash
metricbeat modules enable elasticsearch-xpack
```
`modules.d/elasticsearch-xpack.yml`:
```yaml
- module: elasticsearch
  xpack.enabled: true
  period: 10s
  hosts: ["https://localhost:9200"]
  #scope: node
  #username: "user"
  #password: "secret"
  #ssl.certificate_authorities: ["/etc/pki/root/ca.pem"]
```
- **Scope.** Default `scope: node`: one Metricbeat per Elasticsearch node, or some metrics are not collected. It collects most metrics from the elected master, so scale master-eligible nodes for that load, and do not use it with dedicated master nodes. Preferred: a single Metricbeat with `scope: cluster` and `hosts` pointing to an endpoint (such as a load-balancing proxy) that directs requests to the master-ineligible nodes.
- **Security.** On the production cluster use a user with the `remote_monitoring_collector` built-in role (or the `remote_monitoring_user` built-in user). Use https in `hosts` or set `ssl.enabled: true` when TLS is on.
- **Output.** `metricbeat.yml` sets `output.elasticsearch.hosts` to the monitoring cluster. On a secured monitoring cluster, give the writing user the `remote_monitoring_agent` role (or use `remote_monitoring_user`).
- Optional: `metricbeat modules disable system`, because system-module data is not shown on the Monitoring page.
- Start Metricbeat on each node and view the data in Kibana.

## Elastic Agent
Prerequisite: a user on the production cluster with `remote_monitoring_collector`. In Kibana, open Integrations, add the **Elasticsearch** integration, set the hosts under **Metrics (Stack Monitoring)**, enter the user under **Advanced options**, and choose the scope (`cluster` for a single endpoint such as a load-balancing proxy, otherwise `node` with an agent on every node, not for dedicated masters). Add it to an agent policy and deploy an Elastic Agent on the Elasticsearch host through **Fleet -> Agents -> Add agent**. Wait a minute or two for incoming data.

## Gotchas
- Monitoring a cluster from itself hides outages: the failure you need to see stops the data.
- Size and retention of the monitoring cluster are your decision; check the monitoring data lifecycle settings of your version rather than assuming defaults.

## Verify
The Kibana Monitoring page lists the cluster and every node with current data.

## Checked
2026-11-09. Confirmed against the Elastic docs-content pages (served as the source for the cited guide URLs): "Enable stack monitoring for Elasticsearch on a self-managed cluster", "Collecting monitoring data with Metricbeat" and "Collecting monitoring data with Elastic Agent": architecture, legacy deprecation, module enable command, YAML keys, scope semantics, role names, ingest-node requirement, Fleet steps.
Removed as unsupported: `scope: node` described as local-only, `remote_monitoring_user` as the collect-only role, the alert rule list and thresholds (80 percent disk, 85 percent JVM), the `.monitoring-es-8-mb` data stream name and "tens of GB per day", the `xpack.monitoring.collection.enabled` and `monitoring.ui.elasticsearch.hosts` settings, the Elastic Cloud shipping advice, and the "under 1 minute" freshness check.
Method: documentation only; no commands were run.
