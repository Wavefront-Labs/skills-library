---
id: computing-software.cloud-infrastructure-engineering.google-cloud.weighted-traffic-splitting-and-traffic-steering
name: weighted-traffic-splitting-and-traffic-steering
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-load-balancing, weighted-backends, traffic-steering, canary, url-maps]
level: advanced
status: docs-checked
description: "Steer traffic on the global external Application Load Balancer with URL map weighted backend services, header-based routing, mirroring and fault injection."
sources: ["https://docs.cloud.google.com/load-balancing/docs/https/traffic-management-global", "https://docs.cloud.google.com/load-balancing/docs/https/setting-up-global-traffic-mgmt", "https://docs.cloud.google.com/load-balancing/docs/url-map-concepts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Weighted traffic splitting and traffic steering

Advanced traffic management is a feature of the global external Application Load Balancer
(scheme `EXTERNAL_MANAGED`); the classic ALB lacks it, so migrate first. Regional external ALBs
have their own traffic management overview page.

## 1. Canary by weight
`url-map.yaml`:
```yaml
name: um-web
defaultService: projects/<PROJECT_ID>/global/backendServices/web-v1
hostRules: [{hosts: ['www.example.com'], pathMatcher: web}]
pathMatchers:
- name: web
  defaultService: projects/<PROJECT_ID>/global/backendServices/web-v1
  routeRules:
  - priority: 1
    matchRules: [{headerMatches: [{headerName: x-canary, exactMatch: 'true'}]}]
    service: projects/<PROJECT_ID>/global/backendServices/web-v2
  - priority: 2
    matchRules: [{prefixMatch: /}]
    routeAction:
      weightedBackendServices:
      - {backendService: projects/<PROJECT_ID>/global/backendServices/web-v1, weight: 95}
      - {backendService: projects/<PROJECT_ID>/global/backendServices/web-v2, weight: 5}
```
```bash
gcloud compute url-maps validate --source=url-map.yaml --global
gcloud compute url-maps import um-web --source=url-map.yaml --global
```
Each weight must be from 0 to 1000. Raise the canary weight in steps while watching errors per backend service.

## 2. Other steering (route actions)
- `requestMirrorPolicy` sends an identical request to a mirrored backend service; the setup guide shows an optional `mirrorPercent` (0 to 100). Mirroring is supported for managed instance group, zonal NEG and hybrid NEG backends, not internet NEGs, serverless NEGs or Private Service Connect backends.
- `faultInjectionPolicy` adds delay or abort for a share of requests.
- `urlRewrite`, `retryPolicy`, `timeout` per route.
- Within a route rule the first matching match rule wins.

## Gotchas
- Do not configure session affinity together with weighted traffic splitting: the weighted splitting configuration takes precedence. Without affinity, weights apply per request, so a user may see both versions.
- Header matches take exactly one of `exactMatch`, `prefixMatch`, `suffixMatch`, `regexMatch`, `presentMatch` or `rangeMatch`.
- Traffic policies such as session affinity and outlier detection are not supported with internet NEG backends.

## Verify
- [ ] Request logs by backend service show roughly the configured share to v2; requests with `x-canary: true` always reach v2.

## Checked
2026-10-31. Confirmed against the global external ALB traffic management overview and setup guide (weightedBackendServices weight 0 to 1000, mirroring and its backend limits, mirrorPercent, fault injection, urlRewrite, retryPolicy, session affinity note, first-match rule), the Compute v1 discovery document (`HttpHeaderMatch`, `HttpRouteAction` fields) and the migration overview. Removed: network load balancer weighted-LB claims (the page 404s), the log field name and `url-map.yaml` test-case advice.
Method: documentation only; no commands were run.
