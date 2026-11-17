---
id: computing-software.cloud-infrastructure-engineering.azure.front-door-cdn-and-traffic-manager
name: front-door-cdn-and-traffic-manager
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, front-door, azure-front-door, afd, cdn, traffic-manager, global-load-balancing, origin-groups, origins, routes, rules-engine, caching, compression, private-link-origin, origin-lock-down, x-azure-fdid, managed-certificates, custom-domains, health-probes, anycast, dns-routing, priority-routing, weighted-routing, performance-routing, geographic-routing, endpoint-monitoring]
level: practitioner
status: docs-checked
description: "Front global HTTP apps with Front Door: origin groups, probes, routes, rules engine, caching, Private Link origins, origin lock-down, managed certs; Traffic Manager for the rest."
sources: ["https://learn.microsoft.com/en-us/azure/frontdoor/private-link", "https://learn.microsoft.com/en-us/azure/frontdoor/origin-security", "https://learn.microsoft.com/en-us/azure/frontdoor/health-probes", "https://learn.microsoft.com/en-us/azure/frontdoor/front-door-caching", "https://learn.microsoft.com/en-us/azure/frontdoor/front-door-cdn-comparison", "https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-routing-methods", "https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cdn/resource-manager/Microsoft.Cdn/Cdn/stable/2026-10-01/openapi.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Front Door, CDN and Traffic Manager — global entry points chosen by protocol

**Goal:** one global anycast front for HTTP apps with TLS, WAF, caching and private
origins; DNS-level steering only when the traffic isn't HTTP.

## 1. Which
| Traffic | Service |
|---|---|
| HTTP/HTTPS, multi-region failover, caching, WAF, private origins | **Front Door Standard/Premium** (Premium = Private Link origins + managed WAF rulesets + bot protection) |
| Pure static asset delivery (Front Door covers it; Front Door classic retires 2027-03-31 and Azure CDN Standard from Microsoft classic retires 2027-09-30, so migrate to Front Door Standard/Premium) | Front Door Standard with caching |
| Non-HTTP (TCP/UDP), multi-cloud/on-prem endpoints, DNS-level steering, nested profiles | **Traffic Manager** |
| Regional L7 only | Application Gateway (see its skill); AFD → AGW/App Service/AKS per region is the normal layering |

## 2. Front Door build
```bash
az afd profile create -g rg -n afd-prod --sku Premium_AzureFrontDoor
az afd endpoint create -g rg --profile-name afd-prod -n web --enabled-state Enabled           # web-<hash>.z01.azurefd.net
az afd origin-group create -g rg --profile-name afd-prod -n og-web --probe-request-type HEAD --probe-protocol Https --probe-interval-in-seconds 30 --probe-path /healthz \
  --sample-size 4 --successful-samples-required 3 --additional-latency-in-milliseconds 50
az afd origin create -g rg --profile-name afd-prod --origin-group-name og-web -n uks --host-name web-uks.azurewebsites.net --origin-host-header web-uks.azurewebsites.net --priority 1 --weight 1000 \
  --shared-private-link-resource @private-link.json   # {"privateLink":{"id":"<app-service-id>"},"privateLinkLocation":"uksouth","groupId":"sites","requestMessage":"afd"}
az afd origin create ... -n ukw --host-name web-ukw.azurewebsites.net --priority 2 --weight 1000
az afd route create -g rg --profile-name afd-prod --endpoint-name web -n r-web --origin-group og-web --supported-protocols Http Https --https-redirect Enabled \
  --forwarding-protocol HttpsOnly --link-to-default-domain Enabled --formatted-custom-domains "[{id:<custom-domain-id>}]" --patterns-to-match "/*" \
  --cache-configuration "{query-string-caching-behavior:IgnoreQueryString,compression-settings:{is-compression-enabled:True,content-types-to-compress:[text/html]}}"
az afd custom-domain create -g rg --profile-name afd-prod -n www-example --host-name www.example.com --certificate-type ManagedCertificate --minimum-tls-version TLS12
```
- Routing: lowest **priority** group wins while healthy (active/passive); equal priority +
  **weights** = active/active; `additional-latency` keeps origins within N ms of the fastest in play.
- Probes come from AFD's POPs (`AzureFrontDoor.Backend` service tag); use `HEAD` (the default for new profiles) to a cheap path to lower origin load.
- Custom domain: CNAME `www → web-<hash>.z01.azurefd.net` (or TXT `_dnsauth` for apex via alias record in Azure DNS); managed cert auto-renews; BYO cert from Key Vault (identity on the profile needs *Secrets User*).
- Approve the Private Link request on the origin (`az network private-endpoint-connection approve`) — only then does traffic flow; origin can then have public access **disabled**.

## 3. Lock the origin
Without Private Link: origin must allow only AFD — App Service access restriction with
service tag `AzureFrontDoor.Backend` **and** header check `X-Azure-FDID == <profile frontdoorId>`
(`az afd profile show --query frontDoorId`); AGW/NSG: service tag + a WAF custom rule on
the header. Otherwise anyone can bypass your WAF by hitting the origin directly.

## 4. Rules engine and caching
- Rule sets attached to routes: conditions (request URI, header, path, client address...) → actions (route override, redirect, rewrite, header changes, cache behaviour).
  Order matters; "Stop evaluating remaining rules" is a per-rule option. Use it for `/api/*` → no cache, `/static/*` → long TTL, legacy-URL redirects, and `Strict-Transport-Security` injection.
- Caching honours origin `Cache-Control`; large files are delivered with object chunking when caching is enabled; the route's `queryStringCachingBehavior` controls the cache key.
  Purge: `az afd endpoint purge --content-paths "/static/*" "/index.html"`. Compression applies to files between 1 KB and 8 MB of the configured content types.
- Enable the Front Door access log and health probe log via diagnostic settings to Log Analytics.

## 5. Traffic Manager
```bash
az network traffic-manager profile create -g rg -n tm-api --routing-method Priority --unique-dns-name api-example --ttl 30 \
  --protocol HTTPS --port 443 --path /healthz --interval 10 --timeout 5 --max-failures 2
az network traffic-manager endpoint create -g rg --profile-name tm-api -n uks --type azureEndpoints --target-resource-id <pip-or-app-id> --priority 1
az network traffic-manager endpoint create ... -n onprem --type externalEndpoints --target api-dc1.example.com --priority 2
```
Methods: Priority (failover), Weighted, **Performance** (latency table by client DNS resolver), Geographic (compliance routing by client country), MultiValue (several healthy IPs), Subnet (client CIDR → endpoint). Nested profiles combine (geo → performance). Endpoint monitoring probes from `AzureTrafficManager` tag; TTL small for faster failover — clients still cache. It's DNS only: no TLS termination, no caching, and the client connects straight to the endpoint.

## Gotchas
- AFD is global with a **frontDoorId**; forgetting the header check leaves the origin bypassable even with the service tag (shared by all AFD customers).
- Private Link origins: Premium only; supported origins include App Service (Web/Function App), Blob Storage, Storage static website, and internal load balancers (including AKS via an internal LB).
- Origin host header must match the origin's expected host (App Service default host) or you get 404/redirect loops; set `--origin-host-header`.
- Traffic Manager health is per endpoint from Azure probes — a firewall allowing only your office breaks monitoring and fails everything over.

## Checked
2026-10-28. Confirmed on Microsoft Learn (Front Door private link, origin security, health probes, caching, tier comparison, Traffic Manager routing methods) and the Microsoft.Cdn 2026-10-01 REST spec: Premium-only Private Link, supported Private Link origin types, `AzureFrontDoor.Backend` tag and `X-Azure-FDID`, HEAD probe default, object chunking, 1 KB-8 MB compression window, classic retirement dates, the six Traffic Manager methods, shared private link and cache configuration field names. Corrected: az afd origin/route flags (use `--shared-private-link-resource`, `--formatted-custom-domains`, `--cache-configuration`), the 8 MB figure (compression, not chunking). Removed: Edgio, log field names, TCP_HIT, probe-disable advice, propagation and cert-validation claims, 7-day TTL.
Method: documentation only; no commands were run.

## Verify
- [ ] `curl -sI https://www.example.com` shows `X-Azure-Ref` and a cache-hit indication on the second request for a cacheable path.
- [ ] Hitting the origin hostname directly (no FDID header) returns 403.
- [ ] Stop the priority-1 origin: `FrontDoorHealthProbeLog` marks it unhealthy and traffic shifts to priority 2 with no client 5xx.
- [ ] Traffic Manager: `nslookup api-example.trafficmanager.net` flips to the secondary within TTL after the primary probe fails.
