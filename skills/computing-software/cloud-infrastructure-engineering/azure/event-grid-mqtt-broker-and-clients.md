---
id: computing-software.cloud-infrastructure-engineering.azure.event-grid-mqtt-broker-and-clients
name: event-grid-mqtt-broker-and-clients
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, event-grid, event-grid-namespaces, mqtt, mqtt-broker, mqtt-clients, mqtt-v5, x509-authentication, client-groups, topic-spaces, permission-bindings, message-routing, iot]
level: advanced
status: docs-checked
description: "Run the Event Grid namespace MQTT broker: clients with X.509 or Entra auth, client groups, topic spaces and permission bindings, routing to topics/Event Hubs, and testing with mosquitto."
sources: ["https://learn.microsoft.com/en-us/azure/event-grid/mqtt-overview", "https://learn.microsoft.com/en-us/azure/event-grid/mqtt-support", "https://learn.microsoft.com/en-us/azure/event-grid/mqtt-client-authentication", "https://learn.microsoft.com/en-us/azure/event-grid/mqtt-client-certificate-authentication", "https://learn.microsoft.com/en-us/azure/event-grid/mqtt-topic-spaces", "https://learn.microsoft.com/en-us/azure/event-grid/mqtt-routing", "https://learn.microsoft.com/en-us/azure/event-grid/mqtt-routing-event-schema", "https://learn.microsoft.com/en-us/azure/event-grid/mqtt-publish-and-subscribe-cli", "https://learn.microsoft.com/en-us/azure/event-grid/quotas-limits", "https://learn.microsoft.com/en-us/azure/event-grid/monitor-mqtt-delivery-reference", "https://learn.microsoft.com/en-us/cli/azure/eventgrid/namespace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event Grid MQTT broker and clients

**Goal:** a managed MQTT v3.1.1/v5 broker for devices and apps with per-client identity, topic-level
authorization, and routing of messages into Azure for processing.

## 1. Namespace and broker
```bash
az eventgrid namespace create -g rg-iot -n egns-iot -l uksouth --topic-spaces-configuration "{state:Enabled}"
az eventgrid namespace show -g rg-iot -n egns-iot --query "topicSpacesConfiguration.hostname" -o tsv   # broker hostname; clients connect on TCP 8883
```
Capacity is set in throughput units (TUs, up to 40 per namespace; most MQTT limits scale per TU, for example 1,000 messages per second and 1 MB per second inbound per TU). MQTT 3.1.1 and 5 use TCP 8883; MQTT over WebSocket uses TCP 443.

## 2. Identity: clients and groups
```bash
# client authenticated by X.509 certificate thumbprint or chain (subject name match)
az eventgrid namespace client create -g rg-iot --namespace-name egns-iot -n sensor-0001 \
  --authentication-name sensor-0001 --client-certificate-authentication "{validationScheme:ThumbprintMatch,allowed-thumbprints:[<thumbprint>]}" \
  --attributes "{type:sensor,site:leeds}"
az eventgrid namespace client-group create -g rg-iot --namespace-name egns-iot -n sensors --group-query "attributes.type IN ['sensor']"
```
- Authentication options: X.509 (thumbprint, CA chain via uploaded CA certificate with
  `SubjectMatchesAuthenticationName`), **Entra ID JWT** (apps/services), custom webhook auth.
- Put the client's *authentication name* in the MQTT `username` field of the CONNECT packet (otherwise configure alternative source fields for the authentication name at namespace scope). The `ClientId` is the session name.
- **Client groups** select clients by attribute query; authorization targets groups, not individuals.

## 3. Authorization: topic spaces and permission bindings
```bash
az eventgrid namespace topic-space create -g rg-iot --namespace-name egns-iot -n telemetry \
  --topic-templates 'devices/${client.authenticationName}/telemetry/#'
az eventgrid namespace permission-binding create -g rg-iot --namespace-name egns-iot -n sensors-pub \
  --client-group-name sensors --topic-space-name telemetry --permission Publisher
```
- Template variables (`${client.authenticationName}`, `${client.attributes.site}`) confine each
  device to its own topics — the core multi-tenant safety control.
- Separate topic spaces for commands (`devices/${client.authenticationName}/commands`, Subscriber).

## 4. Routing and test
- **Routing**: namespace → *Routing* → a namespace topic (or custom topic); routed messages
  become CloudEvents with the MQTT topic as `subject`; event subscriptions then deliver to Azure services or webhooks. Enrichments can add client attributes.
- Test with any MQTT 3.1.1 or 5 client that supports client certificates: connect to the namespace hostname on 8883 with the client certificate, username set to the authentication name, then publish and subscribe within the permitted topic spaces.
- Metrics: `MQTT.SuccessfulPublishedMessages`, `MQTT.FailedPublishedMessages`, `MQTT.Connections`, `MQTT.RequestCount` (dimensions include Result and Error); diagnostic logs record failed and successful MQTT connections.

## Gotchas
- Client ID (the session name) and authentication name are different fields; a client whose username or certificate does not match its registered authentication name is refused.
- Only QoS 0 and 1 are supported; retained messages and Last Will and Testament are supported.
- Per-session and per-namespace rate limits apply (for example 1,000 inbound messages per second per session); bursty fleets need more TUs.

## Verify
- [ ] A test device publishes to its own telemetry topic and is refused when publishing to another device's topic.
- [ ] Routed events arrive at the downstream Event Hub/Function with the MQTT topic in `subject`.
- [ ] Connection and failed-publish metrics alert on auth failure spikes.

## Checked
Checked 2026-10-24 against azure-docs Event Grid MQTT pages (overview, support, client authentication, client certificate authentication, topic spaces, routing, routing event schema, publish and subscribe CLI, quotas and limits, MQTT metrics reference) and the azure-docs-cli eventgrid namespace reference. Confirmed: ports 8883 and 443 (WebSocket); QoS 0 and 1 only; retained messages and Last Will supported; topic template variables ${client.authenticationName} and ${client.attributes.x}; permission values Publisher and Subscriber; SubjectMatchesAuthenticationName and ThumbprintMatch validation schemes; routed message subject is the MQTT topic; limits per TU; 40 TU maximum. Fixed: metric names use the MQTT. prefix (not Mqtt.); the thumbprint property is written allowed-thumbprints in the CLI example; topic templates are single-quoted so the shell does not expand ${...}. Removed unconfirmed: hostname pattern, TLS version, sku example, mosquitto commands, IoT Hub comparison.

Method: documentation only; no commands were run.
