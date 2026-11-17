---
id: computing-software.cloud-infrastructure-engineering.azure.app-configuration-and-feature-flags
name: app-configuration-and-feature-flags
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-configuration, feature-flags, feature-management, dynamic-configuration, configuration-refresh, sentinel-key, labels, key-vault-references, snapshots, configuration-snapshots, feature-filters, targeting-filter, percentage-rollout, time-window-filter, variants, experimentation, geo-replication, soft-delete, purge-protection, managed-identity-app-config, app-config-rbac, azure-app-configuration-provider, kubernetes-provider, config-import-export, azure-app-configuration-push]
level: practitioner
status: draft
description: "Centralise config and feature flags with App Configuration: key/label conventions, Key Vault references, sentinel-key refresh, targeting/percentage/time-window filters, variants, snapshots."
sources: ["Microsoft Learn - Azure App Configuration overview, keys/labels and best practices", "Microsoft Learn - Use dynamic configuration and refresh (sentinel key) in .NET/Java/Python/Node", "Microsoft Learn - Feature management: feature flags, filters (targeting, percentage, time window) and variants", "Microsoft Learn - Snapshots, geo-replication, soft delete and purge protection in App Configuration", "Microsoft Learn - Azure App Configuration Kubernetes Provider"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Configuration and feature flags — settings and switches outside the deploy

**Goal:** one store per environment for non-secret settings and feature flags, read by
identity, refreshed at runtime without restarts, with flags that roll out to a
percentage/targeted users and a snapshot that pins what a release saw.

## 1. Store and conventions
```bash
az appconfig create -g rg -n appcs-orders-prod -l uksouth --sku Standard --enable-purge-protection true --retention-days 7 --disable-local-auth true --public-network-access Disabled --assign-identity [system]
az appconfig replica create -g rg -s appcs-orders-prod -n ukwest -l ukwest       # geo-replica: read endpoint failover in the provider libraries
az appconfig kv set -n appcs-orders-prod --key "Orders:Api:Timeout" --value 30 --label prod --content-type "application/json" -y
az appconfig kv set-keyvault -n appcs-orders-prod --key "Orders:Db:Password" --secret-identifier https://kv-orders.vault.azure.net/secrets/db-password --label prod -y   # Key Vault reference
az appconfig kv export -n appcs-orders-prod -d file --path prod.json --format json --label prod -y   # and import for IaC/seed
```
- Tiers: Free (dev), **Standard** (SLA, 1 GB, geo-replication, snapshots), **Premium** (more throughput/storage, 30-day soft delete). One store per environment (or one store with `label` = env — keep it simple: **store per environment**, labels for app/region variants).
- Keys: hierarchical with `:` (`App:Section:Setting`) — maps to `IConfiguration` sections; labels for variants (`prod`, `canary`, `eu`); `\0` (no label) as base. Avoid secrets in values — use **Key Vault references** (the app's identity needs *Secrets User* on the vault; the store never reads the secret).
- Content types: `application/json` for structured values; Feature flags live at `.appconfig.featureflag/<name>` with `application/vnd.microsoft.appconfig.ff+json`.
- Access: **Entra only** (`--disable-local-auth`), roles *App Configuration Data Reader* (apps) / *Data Owner* (pipelines); private endpoint `privatelink.azconfig.io`; **soft delete + purge protection** so a deleted store is recoverable.

## 2. Consume with dynamic refresh
.NET:
```csharp
builder.Configuration.AddAzureAppConfiguration(o => o
  .Connect(new Uri("https://appcs-orders-prod.azconfig.io"), new DefaultAzureCredential())
  .Select("Orders:*", "prod").Select("Shared:*", "prod")
  .ConfigureKeyVault(kv => kv.SetCredential(new DefaultAzureCredential()))
  .ConfigureRefresh(r => r.Register("Orders:Sentinel", refreshAll: true).SetRefreshInterval(TimeSpan.FromSeconds(30)))
  .UseFeatureFlags(ff => { ff.Select("*", "prod"); ff.SetRefreshInterval(TimeSpan.FromSeconds(30)); }));
builder.Services.AddAzureAppConfiguration().AddFeatureManagement();   // + app.UseAzureAppConfiguration() middleware triggers refresh on requests
```
- **Sentinel key** pattern: change many keys, then bump `Orders:Sentinel` — one watched key, one consistent refresh (`refreshAll`), no half-applied config. Providers for Java (Spring), Python, JavaScript, Go follow the same model; **Kubernetes provider** (`AzureAppConfigurationProvider` CRD) syncs keys/flags into a ConfigMap/Secret with refresh — no SDK in the app.
- Refresh is lazy (on next request after the interval) — background workers must call `IConfigurationRefresher.TryRefreshAsync()` on their loop.
- Load only what the app needs (`Select` with prefixes) — each key counts toward request quota (Standard: ~ 30 k requests/hour per store before throttling; the provider caches and uses conditional requests).
- Replicas: the provider fails over to the geo-replica automatically; also distributes load (auto-replica discovery) — enable for anything with an availability target.

## 3. Feature flags done properly
```bash
az appconfig feature set -n appcs-orders-prod --feature NewCheckout --label prod -y
az appconfig feature filter add -n appcs-orders-prod --feature NewCheckout --label prod --filter-name Microsoft.Targeting \
  --filter-parameters Audience='{"Users":["alice@example.com"],"Groups":[{"Name":"beta","RolloutPercentage":50}],"DefaultRolloutPercentage":5,"Exclusion":{"Users":[],"Groups":[]}}' -y
az appconfig feature filter add ... --filter-name Microsoft.TimeWindow --filter-parameters Start='"Mon, 01 Dec 2026 00:00:00 GMT"' End='"Fri, 05 Dec 2026 00:00:00 GMT"' -y
az appconfig feature enable -n appcs-orders-prod --feature NewCheckout --label prod -y
```
- Filters: **Targeting** (users/groups/default percentage, sticky by user ID via the `ITargetingContextAccessor` you implement), **Percentage** (random per evaluation unless your context is sticky), **TimeWindow**, custom filters (`IFeatureFilter`: region, tenant tier). Requirement type `All`/`Any` across filters.
- **Variants** (A/B, kill-switch with config payload): `variants: [{name: "control", configuration_value: ...}, {name: "treatment"}]` with allocation by user/group/percentile and seed for stickiness; `IVariantFeatureManager.GetVariantAsync` → telemetry events (App Insights `FeatureEvaluation`) for **experimentation** (Split-style analysis in the portal).
- Lifecycle: flag → rollout 1 % → 10 % → 50 % → 100 % → remove the flag from code within a sprint (stale flags are debt; tag flags with owner/expiry in the flag's `description`/tags and review monthly).
- Kill switches: flags for *disabling* expensive features under load (`DisableRecommendations`) — evaluated without a user context, refreshed in 30 s.

## 4. Snapshots and release pinning
`az appconfig snapshot create -n appcs-orders-prod -s rel-2026-10-14 --filters '{"key":"Orders:*","label":"prod"}' '{"key":".appconfig.featureflag/*","label":"prod"}' --composition-type key_label`
— an immutable, named set of key-values; the provider can `SelectSnapshot("rel-2026-10-14")` so a deployment reads exactly what was validated; also the rollback artefact ("point prod at yesterday's snapshot"). Archive old snapshots (retention) rather than delete.

## 5. CI/CD and governance
- Source of truth in Git (`config/prod.json` exported format) → pipeline `az appconfig kv import -s file --path ... --format json --label prod --strict` (strict = delete keys not in file) via a workload-identity service connection with *Data Owner*; feature flags enabled by ops via portal/CLI are allowed only if the repo import isn't strict for `.appconfig.featureflag/*` — decide and document.
- Diagnostic settings `HttpRequest`/`Audit` → Log Analytics: who changed which key (alert on prod changes outside pipeline identity). Revision history per key (7 days Standard, 30 Premium) with `az appconfig revision list`.
- Policy: *App Configuration should disable public network access*, *... should use customer-managed key* (Premium), *... should use private link*.

## Gotchas
- Secrets accidentally stored as plain values are visible to every *Data Reader* — scan on import (`kv list --query "[?contains(value,'password')]"` style) and enforce Key Vault references in review.
- Refresh without a sentinel + `refreshAll:false` registers each key; changing 50 keys = 50 watch registrations and partial refreshes between them.
- Percentage filter without a sticky context flips per request — users see the feature flicker; implement targeting context (user ID) and use Targeting.
- Local auth disabled breaks tools/pipelines still using connection strings — migrate them first; `az appconfig` itself works with `--auth-mode login`.
- Free tier has 1 000 requests/day and no SLA; a chatty provider in a 10-pod deployment exhausts it in minutes.
- Snapshot composition `key_label` keeps label dimension; `key` flattens and last-wins by filter order — choose deliberately.
- Kubernetes provider writes a ConfigMap; pods only see changes if they reload (volume mount file watch) — env-var projection needs a rollout.

## Verify
- [ ] `az appconfig show --query "{sku:sku.name,local:disableLocalAuth,pna:publicNetworkAccess,purge:enablePurgeProtection}"` → Standard/true/Disabled/true; replica exists; app reads with managed identity (`Audit` logs show the identity).
- [ ] Change a value + bump the sentinel: the running app reflects it within the refresh interval without restart; Key Vault reference resolves to the secret value only in the app, never in the store.
- [ ] Targeting flag at 10 %: ~10 % of distinct test users (sticky) get the feature; TimeWindow flag off outside the window; variant telemetry appears in App Insights.
- [ ] Release pipeline imports from Git (strict) and creates a snapshot; the deployed app's `SelectSnapshot` matches the release tag; revision history shows only the pipeline identity for prod changes.
