---
id: computing-software.cloud-infrastructure-engineering.azure.event-grid-private-endpoints-and-ip-filtering
name: event-grid-private-endpoints-and-ip-filtering
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, event-grid, eg-private-endpoint, eg-ip-filtering, managed-identity-delivery, network-security]
level: advanced
status: docs-checked
description: "Lock down Event Grid topics and namespaces with private endpoints and IP filtering, and deliver events to private destinations using managed identity."
sources: ["https://learn.microsoft.com/en-us/azure/event-grid/network-security", "https://learn.microsoft.com/en-us/azure/event-grid/configure-private-endpoints", "https://learn.microsoft.com/en-us/azure/event-grid/mqtt-configure-private-endpoints", "https://learn.microsoft.com/en-us/azure/event-grid/configure-firewall", "https://learn.microsoft.com/en-us/azure/event-grid/managed-service-identity", "https://learn.microsoft.com/en-us/azure/event-grid/send-events-webhooks-private-destinations", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-ip-filtering"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event Grid network security

**Goal:** publishers reach Event Grid privately, and Event Grid delivers events to destinations that are not public.

## Inbound (publishing)
- **Private endpoints** for inbound traffic (target sub-resource `topic` for topics; `topicspace` for MQTT-enabled namespaces). Name resolution goes through the `privatelink.eventgrid.azure.net` CNAME.
- **IP filtering** (topics and domains): allow listed IPv4 addresses or CIDR ranges on public access; other publishers receive 403 (Forbidden).
- Disable public network access when all publishers are private:
```bash
az eventgrid topic update -g rg -n egt1 --public-network-access disabled
az eventgrid topic update -g rg -n egt1 --public-network-access enabled --inbound-ip-rules 203.0.113.0/24 allow
```

## Outbound (delivery) to private destinations
Event Grid delivery runs from the Event Grid service, not your VNet, and delivery with a managed identity cannot use private endpoints: the traffic goes over public IP space but is encrypted and carries Event Grid's identity. To reach destinations that restrict public access:
1. Enable a system-assigned managed identity on the topic or domain.
2. Grant it data-plane rights on the destination (`Azure Service Bus Data Sender`, `Azure Event Hubs Data Sender`, `Storage Queue Data Message Sender`); for dead-lettering it also needs `Storage Blob Data Contributor` on the storage account.
3. On Event Hubs, or Service Bus Premium, enable **Allow trusted Microsoft services** (Azure Event Grid is a listed trusted service when the topic or domain has a system-assigned identity; the Service Bus Standard tier has no trusted-services option).
4. Create the subscription with `--delivery-identity systemassigned` (`deliveryWithResourceIdentity`).
Webhooks (Functions, Logic Apps, custom endpoints) must be reachable by Event Grid; for private functions, deliver to Service Bus/Event Hubs/Storage queue and have the function trigger from there over private link. Webhooks on private hosts can be reached through Azure Relay.

## Gotchas
- Private endpoints cover inbound traffic (publishing; pull delivery on namespaces), not Event Grid's outbound delivery.
- The `AzureEventGrid` service tag can be used in network security rules for both inbound and outbound traffic.

## Verify
- [ ] From outside the allowed IP ranges, a publish to the topic endpoint is refused (403).
- [ ] Delivery metrics show successes to the private Service Bus queue.

## Checked
Checked 2026-10-24 against azure-docs Event Grid pages (network-security, configure-private-endpoints, mqtt-configure-private-endpoints, configure-firewall, managed-service-identity, send-events-webhooks-private-destinations) and the Service Bus and Event Hubs trusted-services includes. Confirmed: sub-resource topic and topicspace; privatelink.eventgrid.azure.net; IP firewall with IPv4/CIDR and 403 for others; --inbound-ip-rules and --public-network-access flags; role names Service Bus Data Sender, Event Hubs Data Sender, Storage Queue Data Message Sender and Storage Blob Data Contributor for dead-lettering; managed identity delivery does not use private endpoints; Event Grid is a trusted service for Service Bus and Event Hubs. Removed unconfirmed: domain sub-resource name, trusted-services exception for Storage, system-topic inbound statement, the curl endpoint path.

Method: documentation only; no commands were run.
