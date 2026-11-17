---
id: computing-software.cloud-infrastructure-engineering.azure.application-gateway-v2-listeners-rules-and-backends
name: application-gateway-v2-listeners-rules-and-backends
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, application-gateway, app-gateway, agw, application-gateway-v2, listeners, routing-rules, backend-pools, backend-settings, http-settings, health-probes, path-based-routing, multi-site-listener, ssl-termination, end-to-end-tls, key-vault-certificates, rewrite-rules, url-rewrite, autoscaling, private-frontend, agic, app-gateway-for-containers, mutual-tls, 502-bad-gateway]
level: practitioner
status: docs-checked
description: "Configure Application Gateway v2: multi-site and path routing, Key Vault TLS via managed identity, end-to-end TLS, probes, rewrite rules, autoscale and 502 triage."
sources: ["https://learn.microsoft.com/en-us/azure/application-gateway/configuration-infrastructure", "https://learn.microsoft.com/en-us/azure/application-gateway/configuration-listeners", "https://learn.microsoft.com/en-us/azure/application-gateway/configuration-http-settings", "https://learn.microsoft.com/en-us/azure/application-gateway/key-vault-certs", "https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-ssl-policy-overview", "https://learn.microsoft.com/en-us/azure/application-gateway/understanding-pricing", "https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-private-deployment", "https://learn.microsoft.com/en-us/cli/azure/network/application-gateway/ssl-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application Gateway v2 — layer-7 routing with TLS from Key Vault

**Goal:** one regional L7 entry point that terminates TLS with auto-rotated certs,
routes by host and path to the right backend, re-encrypts where required, and tells
you why a backend is unhealthy.

## 1. Model
Frontend IP (public Standard IP and/or private) → **Listener** (port, protocol, host
names, cert) → **Routing rule** (basic or path-based, priority) → **Backend pool**
(IPs/FQDNs/NICs/VMSS/App Service) + **Backend settings** (port, protocol, cookie affinity,
timeout, host override, probe) ± **Rewrite set** ± **WAF policy**.
```bash
az network public-ip create -g rg -n pip-agw --sku Standard --zone 1 2 3
az identity create -g rg -n id-agw; az role assignment create --assignee <id-principal> --role "Key Vault Secrets User" --scope <kv-id>
az network application-gateway create -g rg -n agw-prod -l uksouth --sku Standard_v2 --zones 1 2 3 \
  --min-capacity 2 --max-capacity 10 --vnet-name vnet-hub --subnet snet-agw \
  --public-ip-address pip-agw --priority 100 --http-settings-port 443 --http-settings-protocol Https \
  --identity id-agw --key-vault-secret-id "https://kv.vault.azure.net/secrets/wildcard-example" --frontend-port 443
az network application-gateway address-pool create -g rg --gateway-name agw-prod -n be-api --servers api.internal.example.com
az network application-gateway probe create -g rg --gateway-name agw-prod -n pr-api --protocol Https --path /healthz --host-name-from-http-settings true --interval 30 --threshold 3 --match-status-codes 200-399
az network application-gateway http-settings create ... -n bs-api --port 443 --protocol Https --host-name-from-backend-pool true --probe pr-api --timeout 30 --cookie-based-affinity Disabled
az network application-gateway http-listener create ... -n ls-api --frontend-port port_443 --frontend-ip appGatewayFrontendIP --host-names api.example.com --ssl-cert <cert-name>
az network application-gateway rule create ... -n rl-api --rule-type Basic --priority 200 --http-listener ls-api --address-pool be-api --http-settings bs-api
```
- Subnet: dedicated, `/24` recommended (v2 scales instances with IPs), only gateways in it;
  NSG must allow `GatewayManager` 65200-65535 inbound, `AzureLoadBalancer`, and your client ports.
- On v2, rule **priority** defines listener processing order: give wildcard and basic
  listeners a higher number than site-specific and multi-site listeners so the specific ones run first.
- Backend as FQDN (App Service, private endpoint names) → set `--host-name-from-backend-pool true`
  so the Host header and SNI match the backend cert; for App Service add an access
  restriction allowing only the gateway's subnet/service tag.

## 2. TLS
- Cert from **Key Vault** (`--key-vault-secret-id` *unversioned* for auto-rotation; gateway
  polls every four hours) via a **user-assigned identity** with *Key Vault Secrets User* (RBAC) or
  `get` secret permission. Vault firewall: enable *trusted services* or private endpoint reachable from the gateway subnet.
- **End-to-end TLS**: backend settings `Https` + trusted root cert upload only when the
  backend cert isn't from a public CA (`--root-certs` on http-settings, well-known CA
  certs are trusted automatically on v2). Backend cert CN/SAN must match the host sent.
- Policy: `az network application-gateway ssl-policy set -g rg --gateway-name agw-prod --policy-type Predefined -n AppGwSslPolicy20220101S`; for custom suites use `--policy-type Custom` or `CustomV2` with `--min-protocol-version` (`TLSv1_2`/`TLSv1_3`).
- Mutual TLS on the listener (client cert validation with CA chain) via SSL profiles.
- HTTP→HTTPS: listener on 80 + rule with `--redirect-config` (type Permanent, target listener).

## 3. Rewrite and routing tricks
- Rewrite sets: add `X-Forwarded-Proto: https`, strip `Server`, rewrite `Location` headers
  from the backend's internal host to the public one (classic App Service redirect problem),
  URL path rewrite (`/api/v1/(.*)` → `/v1/{var_uri_path_1}`), conditional on `{http_req_*}`/`{var_*}` server variables.
- Path-based rule: `--rule-type PathBasedRouting` with a URL path map (`/api/*` → be-api, `/static/*` → be-blob, default → be-web).
- Session affinity only for legacy apps (gateway-managed cookie `ApplicationGatewayAffinity`); connection draining on backend settings for graceful deploys.
- Request timeout default is 20 s on backend settings (range 1–240 s for an external backend, 1–86,400 s for a private one) — raise for long APIs or requests fail.

## 4. Scale and placement
- v2 autoscaling: `--min-capacity` (one capacity unit covers 2,500 persistent connections and 2.22 Mbps of throughput, plus compute) and `--max-capacity`; metrics `Current capacity units`, `Estimated billed capacity units`.
- **Private-only** gateway (no public frontend IP): see the Private Application Gateway deployment page for requirements (NSG rules for GatewayManager inbound and Internet outbound).
- For AKS: **AGIC** (ingress controller programming an AGW) or **Application Gateway for Containers**.
- WAF_v2 SKU adds the WAF policy (see waf skill).

## 5. Troubleshooting
- **502 Bad Gateway** / backend *Unhealthy* in *Backend health*: probe path returns non-2xx/3xx (fix `--match-status-codes` or the app), host header mismatch (set host from backend pool / probe `--host`), cert chain untrusted on end-to-end TLS, NSG/UDR on the backend subnet blocks the gateway subnet, DNS for FQDN backends not resolvable from the gateway's VNet (custom DNS/Private Resolver).
- `az network application-gateway show-backend-health -g rg -n agw-prod` shows the exact reason per server.
- Diagnostics: access, performance and firewall logs (resource-specific tables `AGWAccessLogs`, `AGWPerformanceLogs`, `AGWFirewallLogs`).
- Timeouts: backend settings request timeout; 413: request body limit (WAF).

## Gotchas
- A UDR on the gateway subnet sending `0.0.0.0/0` to a virtual appliance or firewall (forced tunnelling) is not supported on v2; a default route advertised by ER/VPN gateways breaks management traffic, so override it with a `0.0.0.0/0` UDR to Internet and BGP propagation disabled.
- Vault firewall or disabled public access without a private endpoint reachable from the AGW subnet means certificate fetch fails.
- Each listener/rule/pool counts toward subscription limits (see Azure subscription and service limits); batch changes in one ARM/Bicep deploy, not many CLI calls.

## Checked
2026-10-28. Confirmed on Microsoft Learn (Application Gateway infrastructure configuration, listeners, backend settings, Key Vault certificates, SSL policy overview, pricing/capacity unit, private deployment, diagnostics) and the az network application-gateway ssl-policy reference: /24 subnet recommendation, GatewayManager ports 65200-65535, rule priority ordering, four-hour Key Vault polling, 20 s default request timeout and ranges, capacity-unit figures, predefined policy names and `ssl-policy set` flags, forced tunnelling unsupported on v2, log table names. Corrected: listener matching (priority, not most-specific), ssl-policy flags, log names. Removed: priority range, instance-minimum, SKU-switch, 0-byte, host-with-port, listener-count and AGfC claims.
Method: documentation only; no commands were run.

## Verify
- [ ] `show-backend-health` → every server `Healthy`; `curl -vk https://api.example.com/healthz` via the gateway returns 200 with the Key Vault cert's issuer.
- [ ] Rotating the Key Vault certificate version is reflected on the listener within about four hours (`openssl s_client -servername ...` shows the new serial).
- [ ] Path rule test: `/api/x` lands on the API pool (access log `serverRouted_s`), `/` on the web pool.
- [ ] Autoscale metric shows ≥ 2 instances across zones; stopping one backend produces no client errors.
