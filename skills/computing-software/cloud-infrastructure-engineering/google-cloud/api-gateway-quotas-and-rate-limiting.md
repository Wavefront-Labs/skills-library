---
id: computing-software.cloud-infrastructure-engineering.google-cloud.api-gateway-quotas-and-rate-limiting
name: api-gateway-quotas-and-rate-limiting
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, api-gateway, api-gateway-quotas, rate-limiting, x-google-management, metric-costs, api-keys]
level: practitioner
status: docs-checked
description: "Rate-limit API Gateway and Cloud Endpoints APIs per consumer with x-google-management quota metrics and limits, x-google-quota metric costs, API keys, and quota overrides."
sources: ["https://cloud.google.com/endpoints/docs/openapi/quotas-configure", "https://cloud.google.com/api-gateway/docs/creating-api-config", "https://cloud.google.com/api-gateway/docs/authenticate-api-keys", "https://cloud.google.com/endpoints/docs/openapi/openapi-extensions#x-google-management"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway quotas and rate limiting

Quotas in API Gateway / Endpoints are **per consumer project**, identified by the API key (the
consumer is the project that owns the key). Pass an API key so the gateway can identify the project.
The Endpoints quota page is marked Beta. API Gateway applies quota metrics and limits to the whole API, not to one API config, so keep them consistent across active configs before creating a new one.

## OpenAPI 2.0 config
```yaml
swagger: "2.0"
info: {title: orders-api, version: "1.0"}
x-google-management:
  metrics:
  - name: read-requests
    displayName: Read requests
    valueType: INT64
    metricKind: DELTA
  quota:
    limits:
    - name: read-limit
      metric: read-requests
      unit: 1/min/{project}
      values: {STANDARD: 600}
securityDefinitions:
  api_key: {type: apiKey, name: key, in: query}
paths:
  /orders:
    get:
      operationId: listOrders
      security: [{api_key: []}]
      x-google-quota:
        metricCosts: {read-requests: 1}
      x-google-backend: {address: https://orders-abc-nw.a.run.app}
      responses: {"200": {description: ok}}
```
Deploy as a new API config and update the gateway:
```bash
gcloud api-gateway api-configs create v7 --api=orders-api --openapi-spec=openapi.yaml --backend-auth-service-account=gw@<P>.iam.gserviceaccount.com
gcloud api-gateway gateways update orders-gw --api=orders-api --api-config=v7 --location=europe-west2
```

## Limits
Only per-minute, per-project limits are supported: `unit` must be `"1/min/{project}"`, `values` must contain `STANDARD`, `valueType` must be `INT64` and `metricKind` `DELTA`. Expensive endpoints get higher `metricCosts`.

## Keys
Enable the managed service (`<api>.apigateway.<P>.cloud.goog`) in consumer projects and create keys
restricted to that API.

## Gotchas
- Quotas are per-minute counters, not a substitute for DDoS or WAF protection.
- For richer rate limiting and quotas at the proxy layer, see Apigee.

## Verify
- [ ] Requests beyond the configured per-minute limit from one consumer project are rejected; a key from another project is unaffected.

## Checked
2026-10-27. Confirmed against the Cloud Endpoints configuring-quotas page (metrics, limits, metricCosts; unit 1/min/{project}; STANDARD; INT64; DELTA; per-minute per-project only; Beta label), API Gateway creating-API-config page (quotas apply to the whole API) and API keys page (key identifies the project for quotas). The API Gateway quotas-configure page returned 404, so the source list was changed to the Endpoints page. Removed: 429 RESOURCE_EXHAUSTED status, console and Service Usage override instructions, key rotation advice, Cloud Armor and spike-arrest statements.
Method: documentation only; no commands were run.
