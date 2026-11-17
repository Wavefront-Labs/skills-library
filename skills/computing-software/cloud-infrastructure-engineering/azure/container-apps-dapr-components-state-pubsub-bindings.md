---
id: computing-software.cloud-infrastructure-engineering.azure.container-apps-dapr-components-state-pubsub-bindings
name: container-apps-dapr-components-state-pubsub-bindings
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, container-apps, dapr, dapr-components, dapr-pubsub, dapr-state, dapr-bindings, managed-identity]
level: practitioner
status: docs-checked
description: "Enable Dapr on Azure Container Apps and define environment-level components (state store, pub/sub, bindings, secrets) with managed identity and app scoping."
sources: ["https://learn.microsoft.com/en-us/azure/container-apps/dapr-overview", "https://learn.microsoft.com/en-us/azure/container-apps/dapr-components", "https://learn.microsoft.com/en-us/azure/container-apps/enable-dapr", "https://learn.microsoft.com/en-us/azure/container-apps/dapr-component-resiliency", "https://docs.dapr.io/reference/components-reference/supported-state-stores/setup-azure-cosmosdb/", "https://docs.dapr.io/reference/components-reference/supported-pubsub/setup-azure-servicebus-topics/", "https://learn.microsoft.com/en-us/cli/azure/containerapp/env/dapr-component"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container Apps Dapr components

**Goal:** apps talk to state stores and brokers through Dapr building blocks, authenticated with
managed identity, with each component visible only to the apps that need it.

## Enable Dapr on an app
```bash
az containerapp dapr enable -n ca-orders -g rg --dapr-app-id orders --dapr-app-port 8080 --dapr-app-protocol http
```
The sidecar listens on HTTP port 3500 and gRPC port 50001; the app calls e.g.
`POST http://localhost:3500/v1.0/state/statestore`.

## Component YAML (Container Apps schema, not raw Dapr CRD)
```yaml
# statestore.yaml — Cosmos DB with managed identity
componentType: state.azure.cosmosdb
version: v1
metadata:
  - name: url
    value: https://cosmos-orders.documents.azure.com:443/
  - name: database
    value: orders
  - name: collection
    value: state
  - name: azureClientId
    value: <uami-client-id>
scopes: [orders, billing]
```
```bash
az containerapp env dapr-component set -n cae-prod -g rg --dapr-component-name statestore --yaml statestore.yaml
```
Pub/sub with Service Bus:
```yaml
componentType: pubsub.azure.servicebus.topics
version: v1
metadata:
  - name: namespaceName
    value: sb-orders.servicebus.windows.net
  - name: azureClientId
    value: <uami-client-id>
scopes: [orders, shipping]
```
App subscribes programmatically (Dapr calls `/dapr/subscribe`) or declaratively; publish via
`POST /v1.0/publish/<component>/<topic>`.
Bindings (`bindings.azure.storagequeues`, `bindings.cron`) trigger the app at `POST /<binding-name>`.

## Secrets
Prefer managed identity metadata (`azureClientId`). If a component needs a secret, use
`secretStoreComponent` pointing at a secret store component, or `secretRef` metadata with `secrets:` referencing
Container Apps secrets — never inline values.

## Gotchas
- Without `scopes`, every Dapr-enabled app in the same environment loads all deployed components; always scope.
- Component names are referenced by code — renaming breaks apps.
- Identity: the UAMI must be assigned to the **app** (not the environment) and hold the data role (Cosmos SQL role, Azure Service Bus Data Sender/Receiver).
- Dapr is managed by the platform; check the supported components list for Container Apps.
- Resiliency policies (`az containerapp env dapr-component resiliency create`) configure retries, timeouts and circuit breakers per component.

## Verify
- [ ] `az containerapp env dapr-component list -n cae-prod -g rg -o table` shows components and scopes.
- [ ] A test state save/get round trip through the sidecar succeeds.
- [ ] An app that is not in the component's `scopes` cannot use it.

## Checked
Checked 2026-10-24 against azure-docs container-apps pages (dapr-overview, dapr-components, enable-dapr, dapr-component-resiliency), the azure-docs-cli containerapp reference (dapr enable, env dapr-component set and list, resiliency create and their flags), and the Dapr docs repository (Cosmos DB state store and Service Bus topics component specs, subscription methods, publish and state API paths). Confirmed: Container Apps component schema keys (componentType, version, metadata, scopes, secretStoreComponent), default of every app loading all components, ports 3500 and 50001, azureClientId and namespaceName metadata, url/database/collection metadata for Cosmos DB. Removed unconfirmed: the ERR_STATE_STORE_NOT_FOUND error name and the component-loaded log line.

Method: documentation only; no commands were run.
