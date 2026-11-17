---
id: computing-software.cloud-infrastructure-engineering.graylog.azure-event-hubs-input
name: azure-event-hubs-input
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [azure-event-hubs, consumer-group, sas-policy, forward-proxy, azure-logs]
level: practitioner
status: docs-checked
description: "Ingest Azure logs via Event Hubs: Listen SAS policy, consumer group, connection string and optional HTTPS forward proxy."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/azure_event_hubs_input.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# azure event hubs input

Pull input for Azure Event Hubs. Supported log types: Azure Active Directory (audit and sign-in), Azure Audit, Azure Network Watcher, Azure Kubernetes Service, Azure SQL.

Azure setup:
- Add a Shared Access Signature policy with only the **Listen** permission, since Graylog only reads.
- A consumer group is required. The `$Default` group is sufficient; a custom one can be named in the input.
- Note the primary or secondary connection string and the other required values for the Graylog input.

Proxy: an HTTPS-capable forward proxy can be set on the input. With proxy support, connection uses port 443 with AMQP over WebSockets.

Prerequisite: an Azure subscription with Event Hubs configured.

Page conflict: the docs say the number of Graylog nodes that can process messages equals the number of partitions, yet the configuration table says the input currently supports running on a single Graylog node. Treat single-node as the safe assumption.

## Checked

2026-11-04. Confirmed against the Azure Event Hubs input page. Page conflict recorded: it says the number of Graylog nodes that can process messages equals the number of partitions, and also that the input currently supports only a single Graylog node.

Method: documentation only; no commands were run.
