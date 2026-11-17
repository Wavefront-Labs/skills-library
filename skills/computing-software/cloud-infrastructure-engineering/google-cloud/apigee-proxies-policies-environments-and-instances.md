---
id: computing-software.cloud-infrastructure-engineering.google-cloud.apigee-proxies-policies-environments-and-instances
name: apigee-proxies-policies-environments-and-instances
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, apigee, apigee-proxies, api-proxy-deploy, apigee-policies, apigee-flows, apigee-environments, apigee-instances, environment-groups]
level: advanced
status: docs-checked
description: "Build and deploy Apigee API proxies: bundle structure, flows and common policies (API key, OAuth, SpikeArrest, Quota), plus instances, environments and environment groups."
sources: ["https://docs.cloud.google.com/apigee/docs/api-platform/fundamentals/build-simple-api-proxy", "https://docs.cloud.google.com/apigee/docs/api-platform/fundamentals/what-are-flows", "https://docs.cloud.google.com/apigee/docs/api-platform/fundamentals/environments-overview", "https://docs.cloud.google.com/apigee/docs/api-platform/reference/policies/spike-arrest-policy", "https://docs.cloud.google.com/sdk/gcloud/reference/apigee/apis/deploy", "https://docs.cloud.google.com/apigee/docs/reference/apis/apigee/rest/v1/organizations.envgroups/create"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Apigee: proxies, policies, environments and instances

## 1. Topology
- **Instance**: runtime in one region; an environment can be attached to several instances. One or more per org.
- **Environment** (`dev`, `test`, `prod`): deployment target; attached to instances.
- **Environment group**: the hostnames (`api.example.com`) that route requests to its environments; base paths of proxies in one group share a hostname.
```bash
TOKEN=$(gcloud auth print-access-token); ORG=<ORG>
curl -s -H "Authorization: Bearer $TOKEN" https://apigee.googleapis.com/v1/organizations/$ORG/instances
curl -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  https://apigee.googleapis.com/v1/organizations/$ORG/environments -d '{"name":"prod"}'
curl -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  https://apigee.googleapis.com/v1/organizations/$ORG/instances/<INSTANCE>/attachments -d '{"environment":"prod"}'
curl -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  https://apigee.googleapis.com/v1/organizations/$ORG/envgroups -d '{"name":"public","hostnames":["api.example.com"]}'
```

## 2. Proxy bundle
```
apiproxy/
  orders.xml                      # proxy descriptor
  proxies/default.xml             # ProxyEndpoint: BasePath /v1/orders, PreFlow, Flows, PostFlow, RouteRule
  targets/default.xml             # TargetEndpoint: backend URL (or TargetServer), SSL
  policies/VerifyKey.xml  SpikeArrest.xml  Quota.xml  AssignMessage-RemoveKey.xml
```
ProxyEndpoint PreFlow (request): `VerifyAPIKey` (or `OAuthV2` VerifyAccessToken) → `SpikeArrest`
(smooths bursts, e.g. `30ps`) → `Quota` (per app/product, e.g. 10,000/day) → `AssignMessage` to strip
the key before calling the backend. Conditional flows (`<Condition>request.verb = "POST" and proxy.pathsuffix MatchesPath "/"</Condition>`)
handle per-operation policies; FaultRules shape error responses.

## 3. Deploy
```bash
zip -r orders.zip apiproxy
gcloud apigee apis deploy <REV> --api=orders --environment=prod --organization=$ORG   # REVISION is positional (default: latest); --override swaps a conflicting base path
curl -X POST -H "Authorization: Bearer $TOKEN" -F file=@orders.zip \
  "https://apigee.googleapis.com/v1/organizations/$ORG/apis?name=orders&action=import"
gcloud apigee deployments list --api=orders --organization=$ORG
```
A deployed revision can no longer be modified; save changes as a new revision. In CI, promote the **same revision** dev → test → prod and run proxy tests against each environment.

## Gotchas
- By default a proxy's base path must not already be used by a deployed proxy in the target environment; `--override` undeploys the conflicting one.

## Checked
2026-10-31. Confirmed against the gcloud reference for `apigee apis deploy` (positional REVISION defaulting to latest, `--override`, `--organization`, revisions immutable once deployed), the Apigee environments overview (environment groups hold hostnames and route to environments; instances are regions), the flows and SpikeArrest pages, and the REST reference for instance attachments and environment groups. Removed unconfirmed: VPC peering/PSC wording, apigeecli/Maven/apickli, quota-counter, API-product and DNS/certificate gotchas. Bundle file names and the quota figure are illustrative examples.
Method: documentation only; no commands were run.

## Verify
- [ ] `curl https://api.example.com/v1/orders -H 'x-apikey: <KEY>'` returns 200; without key 401; burst returns 429 from SpikeArrest.
- [ ] Deployment shows the same revision across environments after promotion.
