---
id: computing-software.cloud-infrastructure-engineering.azure.key-vault-service-limits-throttling-and-caching
name: key-vault-service-limits-throttling-and-caching
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, key-vault, kv-throttling, kv-service-limits, 429-throttling, secret-caching, vault-saturation]
level: practitioner
status: docs-checked
description: "Avoid Key Vault 429 throttling: per-vault transaction limits, saturation metrics, client-side secret caching, backoff and vault-per-app layout."
sources: ["https://learn.microsoft.com/azure/key-vault/general/service-limits", "https://learn.microsoft.com/azure/key-vault/general/overview-throttling", "https://learn.microsoft.com/azure/key-vault/general/monitor-key-vault-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key Vault limits, throttling and caching

**Goal:** Key Vault never becomes the outage - apps read secrets rarely and survive throttling.

## Limits (per vault, per region, per 10 seconds)
- All other secret, managed storage key and vault transactions: **4,000**. Secret CREATE, certificate IMPORT and key
  IMPORT share one **300** limit collectively.
- Key operations are weighted by key type, and enforcement is on their sum. RSA 2,048-bit software-key GET allows 4,000,
  RSA 2,048-bit HSM-key GET 2,000, RSA 4,096-bit HSM-key GET 250 (8x the cost of 2,048-bit). Read the service-limits
  table for your key type.
- CREATE key and RELEASE key (secure key release) share one category: 10 transactions per 10 s for HSM-protected keys,
  20 for software-protected keys. For high SKR throughput use Managed HSM.
- Exceeding a limit returns **HTTP 429**. A request that returns 429 does not count toward the tracked limit.
- A subscription-wide limit for all transaction types is five times the per-vault limit.

## Detect
- Metric **Overall Vault Saturation** (percent, 1-minute grain): alert at a threshold you choose below 100%.
- Metric **Total Service Api Results** (`ServiceApiResult`), split by `StatusCode`: alert on 429 count > 0.
- Use diagnostic logs to find the noisy caller (caller IP and identity); check your log schema for column names.

## Fix patterns
1. **Cache** secrets in memory and re-read only when the cached copy stops working (for example after rotation) - never
   fetch per request.
2. Back off exponentially on 429: Microsoft's recommended sequence waits 1, 2, 4, 8, then 16 seconds between retries.
   Avoid immediate retries and reduce operations per request and request frequency.
3. Separate vaults per application per region/environment (Microsoft's example: five apps in two regions = 10 vaults),
   so one noisy app can't starve others.
4. Do public-key operations (encrypt, wrap, verify) locally by caching the public key material.
5. If Key Vault holds credentials for a service that supports Microsoft Entra authentication, authenticate directly
   with Entra instead; it cuts Key Vault load.
6. Multi-node apps reading the same secrets: one entity reads and fans out to nodes, caching in memory only.
7. For high-throughput key operations use Managed HSM (dedicated instances, higher limits).

## Gotchas
- Startup storms: many pods restarting together each fetching many secrets can trip limits - stagger the load or
  deployment over a longer period, or cache centrally.
- Do not send more than the subscription limit to Key Vault in one region.

## Verify
- [ ] Saturation stays low under peak load test; 429 alert configured; code review confirms no per-request vault calls.

## Checked
2026-10-27. Confirmed against Learn pages "Azure Key Vault service limits" (updated 2026-06-12), "Azure Key Vault
throttling guidance" (2026-07-17) and "Monitor Key Vault data reference": 4,000/300 limits, key weighting, CREATE/RELEASE
10 and 20, 429 behaviour, subscription limit five times, backoff 1-16 s, metric names and grain. Removed: Retry-After
header, 75% alert figure, SDK default retry claim, CSI poll interval figures, App Service/App Configuration caching
specifics, per-page listing cost, paired-region capacity claim, and the KQL query (column names not verified).
Method: documentation only; no commands were run.
