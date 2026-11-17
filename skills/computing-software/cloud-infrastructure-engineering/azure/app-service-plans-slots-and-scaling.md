---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-plans-slots-and-scaling
name: app-service-plans-slots-and-scaling
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service, app-service-plan, deployment-slots, slot-swap, swap-with-preview, sticky-settings, custom-domains, managed-certificate, app-service-scaling, autoscale, automatic-scaling, premium-v3, zone-redundancy, always-on, health-check, app-settings, key-vault-references, deployment-center, zip-deploy, run-from-package, app-service-backup, kudu, diagnostic-logs, linux-app-service]
level: practitioner
status: docs-checked
description: "Run web apps on App Service: plan tiers and zone redundancy, slot swaps with warm-up, run-from-package, custom domains with managed certs, health check and autoscale."
sources: ["https://learn.microsoft.com/azure/app-service/overview-hosting-plans", "https://learn.microsoft.com/azure/app-service/deploy-staging-slots", "https://learn.microsoft.com/azure/app-service/monitor-instances-health-check", "https://learn.microsoft.com/azure/app-service/manage-backup", "https://learn.microsoft.com/azure/app-service/manage-automatic-scaling", "https://learn.microsoft.com/azure/reliability/reliability-app-service", "https://learn.microsoft.com/azure/app-service/configure-ssl-certificate", "https://learn.microsoft.com/azure/azure-resource-manager/management/azure-subscription-service-limits"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Service — plans, slots and scaling that don't surprise you on release day

**Goal:** zero-downtime deploys via warmed slots, a plan tier that matches the SLA,
custom domains with certificates that renew themselves, and autoscale that reacts to
the right metric.

## 1. Plan and app
```bash
az appservice plan create -n asp-web-prod -g rg -l uksouth --sku P1v3 --is-linux --zone-redundant --number-of-workers 3
az webapp create -n web-prod-001 -g rg -p asp-web-prod --runtime "DOTNETCORE:10.0" --assign-identity [system] --https-only true --basic-auth Disabled
az webapp config set -n web-prod-001 -g rg --always-on true --min-tls-version 1.2 --ftps-state Disabled --http20-enabled true
az webapp config appsettings set -n web-prod-001 -g rg --settings WEBSITE_RUN_FROM_PACKAGE=1 DB_CONN="@Microsoft.KeyVault(VaultName=kv;SecretName=db)"
```
- Tiers: **Free/Shared** share compute; **Basic, Standard, Premium v2/v3/v4** run on dedicated VMs;
  **Isolated v2** is App Service Environment (dedicated, inside your VNet, up to 200 instances).
  Slots per app depend on the tier (see the subscription and service limits page); VNet integration
  and private endpoints need Basic or above; zone redundancy is a Premium v2-v4 feature.
  Plan = the VM set; apps on one plan share instances — isolate noisy apps onto their own plan.
- Linux and Windows plans differ in runtime stacks and some features; check the docs for your stack.
- `--always-on` so the app isn't unloaded after 20 minutes without requests (required for continuous WebJobs).
- `WEBSITE_RUN_FROM_PACKAGE=1` makes `wwwroot` a read-only mount of the deployed zip:
  atomic deploys, no file locks, instant rollback by redeploying the previous package.

## 2. Deploy
- `az webapp deploy -n web-prod-001 -g rg --src-path app.zip --type zip --slot staging`
  (OneDeploy; `--type` selects the artifact type, e.g. `zip`, `war`, `jar`, `static`). Deployment Center wires GitHub Actions /
  Azure Pipelines with the app's OIDC credentials; **publish profiles are passwords** — disable
  basic authentication for SCM and FTP once OIDC works (`az webapp create --basic-auth Disabled` for new apps).
- Kudu/SCM site `https://<app>.scm.azurewebsites.net`: console, process explorer, log stream,
  `/api/zipdeploy`. Lock it down with the same access restrictions as the app (`--scm-site`).

## 3. Slots and swaps
```bash
az webapp deployment slot create -n web-prod-001 -g rg -s staging --configuration-source web-prod-001
az webapp config appsettings set ... --slot-settings ENV=staging       # sticky: stays with the slot on swap
az webapp deployment slot swap -n web-prod-001 -g rg -s staging --target-slot production --action preview   # phase 1: apply prod settings to staging, warm up
# validate https://web-prod-001-staging.azurewebsites.net then
az webapp deployment slot swap ... --action swap     # or --action reset to abort
```
- Swap moves **instances**, not files: staging is warmed with production settings first,
  the site's `applicationInitialization` paths (web.config) or `WEBSITE_SWAP_WARMUP_PING_PATH`
  + `WEBSITE_SWAP_WARMUP_PING_STATUSES=200,202` must return OK or the swap fails (good).
- **Settings that do not swap**: custom domain names, non-public certificates and TLS settings, scale settings, WebJobs schedulers,
  and (configurable) IP restrictions, Always On, diagnostic log settings, CORS and managed identities; app settings and
  connection strings swap unless marked as slot settings. Review the list in the staging slots article.
- Auto-swap for CD into production; **traffic routing** `az webapp traffic-routing set --distribution staging=10` for canaries.
- Slots share the plan's instances — a load test against staging affects production.

## 4. Domains and TLS
```bash
az webapp config hostname add -n web-prod-001 -g rg --hostname www.example.com   # after creating the DNS records the portal asks for
az webapp config ssl create -n web-prod-001 -g rg --hostname www.example.com      # free App Service managed certificate
az webapp config ssl bind -n web-prod-001 -g rg --certificate-thumbprint <t> --ssl-type SNI
```
Root domains: a managed certificate needs the app reachable from the internet (no IP restrictions) for
creation and renewal. For other certificates use Key Vault import (`az webapp config ssl import`). Front Door in front? Then terminate TLS there and restrict the app to Front Door's service tag + `X-Azure-FDID` header.

## 5. Scaling and health
- **Health check** (portal: Monitoring, Health check; set a path):
  App Service pings the path every minute; an instance that fails 10 requests (configurable) is removed from the load balancer
  and replaced if it stays unhealthy for one hour.
- **Autoscale** (Azure Monitor): `az monitor autoscale create --resource <plan-id> --min-count 3 --max-count 10 --count 3`,
  example rules on `CpuPercentage > 70` for 10 min → +1 (cooldown 5 min), scale-in at < 30 % for 15 min → −1;
  schedule profiles for known peaks. Scale on **HttpQueueLength**/response time for IO-bound apps, not CPU.
- **Automatic scaling**: `az appservice plan update --elastic-scale true --max-elastic-worker-count 20`
  + per-app `--prewarmed-instance-count` — platform-driven HTTP scaling, no rules.
- Scale-up (tier) causes a restart; scale-out doesn't. Instance count applies to all apps on the plan.
- Zone redundancy: Premium v2-v4, set at plan create; the platform enforces a minimum of two instances and spreads them across zones.

## 6. Ops
- Logs: `az webapp log config`, `az webapp log tail`; diagnostic settings (HTTP, console and app log categories) → Log Analytics for anything serious.
- *Diagnose and solve problems* blade (availability, CPU, memory, SNAT port exhaustion — the classic hidden limit; fix with connection pooling, private endpoints, or NAT Gateway on VNet integration).
- Backups: automatic backups (hourly, 30-day retention, not configurable; Basic and above) and custom backups to storage with DB; restore to a slot first.
- Restart vs *Advanced Application Restart* (per-instance) when one instance is sick.

## Gotchas
- Swapping with a pending app-setting change on production applies it to the staging slot's code first — settings and code must be promoted together.
- `WEBSITE_RUN_FROM_PACKAGE` + Kudu edits = edits silently discarded (read-only wwwroot).
- Managed certificates need the app reachable from the internet for creation and renewal — private-only apps need imported (Key Vault) certs.
- Autoscale on a plan with slots counts slot traffic; health-check path must be unauthenticated and cheap.
- `az webapp up` picks defaults you may not want in prod.

## Verify
- [ ] `az webapp show --query "{state:state,https:httpsOnly,plan:appServicePlanId}"` and `az appservice plan show --query "{sku:sku.name,zr:zoneRedundant,workers:sku.capacity}"` match design.
- [ ] Swap with preview: staging warm-up path returns 200 with production settings; swap completes with no 5xx in `AppServiceHTTPLogs` during the minute.
- [ ] `curl -sI https://www.example.com` shows the managed cert chain; renewal visible in *Certificates* with the next expiry > 30 days.
- [ ] Autoscale test (load generator) adds instances within ~10 min and removes them after cooldown; health-check metric shows all instances healthy.

## Checked
2026-10-27. Confirmed on Microsoft Learn: App Service plan overview (tiers), staging slots article (settings that do not swap, warm-up app settings),
health check article (1-minute ping, 10 requests, one hour), backup article (automatic backups hourly, 30 days, Basic and above), Always On 20 minutes
(configure-common), reliability article (zone redundancy minimum two instances), automatic scaling article, limits page (ASE 200 instances), and the CLI
reference for appservice plan, webapp, webapp deployment slot, webapp config ssl, hostname, traffic-routing and monitor autoscale (flags used).
Removed or reworded: three-instance zone-redundancy minimum, SNAT 128-port figure, DigiCert and wildcard/apex certificate claims, asuid TXT detail, 2-failure
health check figure, `az webapp config set --basic-auth-enabled` (not a flag of that command), log-category names, plan-OS claim.

Method: documentation only; no commands were run.
