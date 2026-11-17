---
id: computing-software.cloud-infrastructure-engineering.google-cloud.api-gateway-endpoints-and-apigee
name: api-gateway-endpoints-and-apigee
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, api-gateway, cloud-endpoints, apigee, apigee-x, apigee-hybrid, openapi, api-config, espv2, extensible-service-proxy, api-keys, jwt-validation, api-products, developer-portal, api-quotas, rate-limiting-api, api-analytics, api-management, grpc-transcoding]
level: practitioner
status: docs-checked
description: "API management on GCP: API Gateway for serverless backends (OpenAPI, API keys, JWT), Cloud Endpoints ESP/ESPv2, and Apigee for developer portals, quotas and analytics."
sources: ["https://cloud.google.com/api-gateway/docs/about-api-gateway", "https://cloud.google.com/api-gateway/docs/quickstart-console", "https://cloud.google.com/api-gateway/docs/authenticating-users-jwt", "https://cloud.google.com/endpoints/docs/openapi/architecture-overview", "https://cloud.google.com/apigee/docs/api-platform/get-started/what-apigee", "https://cloud.google.com/apigee/docs/api-platform/architecture/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway, Cloud Endpoints and Apigee

**Goal:** an API front door that authenticates callers, enforces quotas, and gives you
per-consumer analytics — sized to the problem: Gateway for a few services, Apigee for a programme.

## 1. Choose
| | **API Gateway** | **Cloud Endpoints** (ESPv2) | **Apigee X / hybrid** |
|---|---|---|---|
| Form | managed gateway in front of Cloud Run functions, Cloud Run and App Engine backends | you deploy ESP or ESPv2 (a proxy) in front of your backend | API management platform: proxy layer, developer portal, analytics, security |
| Config | OpenAPI 2.0 or 3.x with `x-google-backend`, or gRPC files (`--grpc-files`) | OpenAPI or gRPC service config | API proxies with policies |
| Auth | API keys, Google ID tokens, JWTs from any issuer you configure (`x-google-issuer`) | same mechanisms and syntax | security policies at the proxy, Advanced API security |
| Quotas | per consumer project (API key) via `x-google-management` | same (Endpoints quota docs are Beta) | quotas and rate limiting at the proxy layer |
| Pick when | a team exposes a few serverless APIs | you already run GKE and want in-cluster gateway | enterprise API programme, partner onboarding, monetisation |

## 2. API Gateway
```yaml
# openapi.yaml (OpenAPI 2.0 shown; 3.x is also supported)
swagger: "2.0"
info: {title: orders, version: 1.0.0}
host: orders-gw.example.com
schemes: [https]
securityDefinitions:
  api_key: {type: apiKey, name: x-api-key, in: header}
  firebase: {authorizationUrl: "", flow: implicit, type: oauth2,
             x-google-issuer: "https://securetoken.google.com/<FIREBASE_PROJECT>",
             x-google-jwks_uri: "https://www.googleapis.com/service_accounts/v1/metadata/x509/securetoken@system.gserviceaccount.com",
             x-google-audiences: "<FIREBASE_PROJECT>"}
x-google-management:
  metrics: [{name: read-requests, displayName: Reads, valueType: INT64, metricKind: DELTA}]
  quota: {limits: [{name: read-limit, metric: read-requests, unit: "1/min/{project}", values: {STANDARD: 1000}}]}
paths:
  /orders/{id}:
    get:
      operationId: getOrder
      security: [{api_key: []}, {firebase: []}]
      x-google-quota: {metricCosts: {read-requests: 1}}
      x-google-backend: {address: https://orders-api-xyz-ew.a.run.app, path_translation: APPEND_PATH_TO_ADDRESS, deadline: 30.0}
      responses: {"200": {description: ok}}
```
```bash
gcloud api-gateway apis create orders
gcloud api-gateway api-configs create v1 --api=orders --openapi-spec=openapi.yaml --backend-auth-service-account=gw@<P>.iam.gserviceaccount.com
gcloud api-gateway gateways create orders-gw --api=orders --api-config=v1 --location=europe-west1
```
- The service account in `--backend-auth-service-account` signs the token for the backend; for a Cloud Run backend it must have `roles/run.invoker`.
- API keys: enable the API's managed service (`<api>-<hash>.apigateway.<P>.cloud.goog`) in the project that owns the key, and restrict the key to that API (`gcloud services api-keys create --api-target=service=<managed-service>`).
- New config = new `api-configs create` + `gateways update --api-config`.

## 3. Cloud Endpoints (ESPv2)
Deploy the service config with `gcloud endpoints services deploy openapi.yaml` (flags include `--validate-only` and `--async`). Endpoints components are ESP or ESPv2 (the proxy that injects authentication, monitoring and logging), Service Control, Service Management, the gcloud CLI and the console. ESP is NGINX-based and runs in front of the backend; see the architecture overview for the platforms ESP supports.

## 4. Apigee X essentials
- Apigee is an API proxy layer between your backends and clients, with policies for security, traffic management, rate limiting and quotas; it supports REST, gRPC, SOAP and GraphQL (what-is-Apigee page).
- Provisioning offers two networking options: with VPC peering (an external Application Load Balancer fronting a managed instance group of bridge VMs that you scale and patch) or without VPC peering (Private Service Connect with service attachments and endpoint attachments for southbound targets).
- Insights: a developer portal for API discoverability, Advanced API security, API monitoring and analytics. The what-is-Apigee and architecture pages apply to Apigee and Apigee hybrid.

## Gotchas
- API Gateway supports OpenAPI 2.0, 3.0.x and 3.1.x; 3.x uses a different extension syntax (`x-google-api-management` backends), and the gcloud CLI must be current before creating 3.x configs.
- `x-google-audiences` is optional: API Gateway accepts JWTs whose `aud` is `https://<SERVICE_NAME>`; list extra client IDs there (comma-separated in OpenAPI 2.0).
- Quota metrics and limits apply to the whole API, not one API config: keep them consistent across active configs before creating a new one.

## Verify
- [ ] A request without a key is rejected; a key from another project is rejected until the managed service is enabled there; a valid key succeeds.
- [ ] Exceeding the per-minute limit rejects further requests until the next minute.
- [ ] Backend Cloud Run logs show the gateway service account as caller.

## Checked
2026-10-27. Confirmed against API Gateway about, OpenAPI overview, API keys, JWT, creating-API-config and get-started-Cloud-Run pages; Endpoints architecture overview and quotas page; Apigee what-is and architecture pages; gcloud reference pages for api-gateway (api-configs create flags), services api-keys create and endpoints services deploy. Removed: per-call and platform cost rows, Apigee 60-day evaluation, provisioning time and /22 + /28 ranges, policy and org/environment hierarchy lists, ESPv2 image and flags, the serverless NEG command and custom-domain claim (flags not on the gcloud page), spectral, rollout timing, response-code and latency verify claims. Corrected: API Gateway supports OpenAPI 3.x as well as 2.0; x-google-audiences is optional.
Method: documentation only; no commands were run.
