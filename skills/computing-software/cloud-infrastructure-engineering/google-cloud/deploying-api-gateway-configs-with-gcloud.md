---
id: computing-software.cloud-infrastructure-engineering.google-cloud.deploying-api-gateway-configs-with-gcloud
name: deploying-api-gateway-configs-with-gcloud
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, api-management, gcloud-api-gateway, api-gateway-deploy, openapi, cloud-run]
level: practitioner
status: docs-checked
description: "Deploy Google Cloud API Gateway: OpenAPI 2.0 spec with x-google-backend, immutable API configs, gateway updates, backend service account auth to Cloud Run, and rollback."
sources: ["https://cloud.google.com/api-gateway/docs/get-started-cloud-run", "https://cloud.google.com/api-gateway/docs/openapi-overview", "https://cloud.google.com/api-gateway/docs/creating-api-config", "https://cloud.google.com/sdk/gcloud/reference/api-gateway"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying API Gateway configs with gcloud

## 1. Spec (OpenAPI 2.0 shown; 3.0.x and 3.1.x are also supported)
```yaml
swagger: '2.0'
info: {title: orders-api, version: 1.0.0}
schemes: [https]
produces: [application/json]
x-google-backend:
  address: https://orders-abc123-ew.a.run.app
  deadline: 30.0
paths:
  /orders/{id}:
    get:
      operationId: getOrder
      parameters: [{name: id, in: path, required: true, type: string}]
      x-google-backend:
        address: https://orders-abc123-ew.a.run.app
        path_translation: APPEND_PATH_TO_ADDRESS
      responses: {'200': {description: OK}}
```
`path_translation`: `APPEND_PATH_TO_ADDRESS` appends the request path to the backend address; `CONSTANT_ADDRESS` uses the address as the fixed path and sends path parameters as query parameters. The default is `APPEND_PATH_TO_ADDRESS` for a top-level `x-google-backend` and `CONSTANT_ADDRESS` for an operation-level one, so set it explicitly.

## 2. Create API, config, gateway
```bash
gcloud services enable apigateway.googleapis.com servicemanagement.googleapis.com servicecontrol.googleapis.com
gcloud api-gateway apis create orders-api
gcloud api-gateway api-configs create orders-v3 --api=orders-api --openapi-spec=openapi.yaml \
  --backend-auth-service-account=apigw-backend@<P>.iam.gserviceaccount.com
gcloud api-gateway gateways create orders-gw --api=orders-api --api-config=orders-v3 --location=europe-west1
gcloud api-gateway gateways describe orders-gw --location=europe-west1 --format='value(defaultHostname)'
```
The service account used to create an API config for a Cloud Run backend must have `roles/run.invoker`. The token audience defaults to the backend `address`; override it with `jwt_audience`.

## 3. Update and roll back
API configs are **immutable**: create a new config name per change, then
`gcloud api-gateway gateways update orders-gw --api=orders-api --api-config=orders-v4 --location=europe-west1`.
Rollback = update back to the previous config.

## Gotchas
- OpenAPI 3.x uses a different extension syntax (`x-google-api-management` backends); update the gcloud CLI first or uploads can fail.
- The default gateway hostname ends in `gateway.dev`.

## Verify
- [ ] `curl https://<defaultHostname>/orders/123` returns backend data; Cloud Run logs show requests from the backend SA.

## Checked
2026-10-27. Confirmed against API Gateway OpenAPI overview, creating-API-config, get-started-Cloud-Run pages and the x-google-backend extension reference (path_translation values and defaults, jwt_audience default); gcloud flag check for api-gateway apis, api-configs and gateways commands. Removed: custom-domain claim, update-time claim, config-retention advice. Corrected: OpenAPI 3.x is supported.
Method: documentation only; no commands were run.
