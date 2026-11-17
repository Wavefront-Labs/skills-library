---
id: computing-software.cloud-infrastructure-engineering.graylog.data-node-management-ui
name: data-node-management-ui
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [data-node, managed-opensearch, data-node-ui, cluster-management]
level: intro
status: docs-checked
description: "What Graylog Data Node is and how to manage it in System > Data Nodes: node actions, certificates and the Enterprise cluster dashboard."
sources:
  - https://go2docs.graylog.org/current/downloading_and_installing_graylog/install_graylog_data_node.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# data node management ui

Data Node manages OpenSearch for Graylog so you do not install and run it separately. It also secures the data layer with certificates, manages cluster membership and ensures the right OpenSearch version and extensions are present. A migration wizard moves an existing search backend to Data Node.

Manage it at **System > Data Nodes**:
- **Data Nodes** tab: lists nodes with status and certificate expiration. Actions: Renew certificate, Stop/Start (the OpenSearch service), Remove (from the cluster), Show logs (stdout or stderr).
- **Cluster Management** tab: prebuilt dashboard of search backend metrics; requires a Graylog Enterprise license. Without a license or Data Node it shows a static example.

## Checked

2026-11-04. Confirmed against the Data Node install page. Removed: "Install it only through the Data Node package. Do not install OpenSearch directly", which the cited page does not state.

Method: documentation only; no commands were run.
