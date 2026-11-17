---
id: computing-software.cloud-infrastructure-engineering.azure.front-door-classic-and-cdn-migration-to-standard-premium
name: front-door-classic-and-cdn-migration-to-standard-premium
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, front-door, afd-migration, cdn-migration, front-door-classic, azure-cdn-classic, front-door-standard, front-door-premium, waf-policy-upgrade, zero-downtime-migration, retirement]
level: practitioner
status: docs-checked
description: "Migrate Front Door (classic) to Standard/Premium with the built-in validate, prepare, migrate tool: WAF tier choice, Key Vault identity, endpoint cutover."
sources: ["https://learn.microsoft.com/en-us/azure/frontdoor/tier-migration", "https://learn.microsoft.com/en-us/azure/frontdoor/migrate-tier", "https://learn.microsoft.com/en-us/azure/frontdoor/migrate-cdn-to-front-door", "https://learn.microsoft.com/en-us/cli/azure/afd/profile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Front Door classic to Front Door Standard or Premium

**Goal:** move a Front Door (classic) profile onto Standard or Premium with the zero-downtime
migration tool (control plane only; the data plane stays the same). Front Door (classic) retires
on March 31, 2027 and no longer supports profile creation, new domain onboarding or managed
certificates.

## 1. Tier is decided by the WAF policy
| Classic WAF policy | New tier |
|---|---|
| Only custom rules (or none) | **Standard** by default; you can upgrade to Premium during migration |
| Managed rules, or managed plus custom | **Premium**; cannot downgrade during migration. To get Standard, remove the managed rules or the WAF association first |

- After migration Standard can be upgraded to Premium, but Premium cannot be downgraded to Standard.
- If the profile exceeds Standard quota limits, migration moves it to Premium.
- CLI, PowerShell, API or Terraform migration needs WAF policies created separately; the portal can copy them.

## 2. Phases (portal: classic profile, Settings, Migration)
1. **Validate**: checks compatibility (can take up to two minutes); errors come with recommendations.
   All custom domains must use HTTPS (a free Front Door managed certificate works). Session
   affinity moves from domain level to the origin group, so two domains sharing a backend pool
   must have consistent session affinity or validation fails.
2. **Prepare**: creates the new profile (default name `<endpointprefix>-migrated`) and a copy of each WAF
   policy (default suffix `-standard` or `-premium`), or you pick an existing matching policy.
   Rename the profile or WAF policy here; rules engine and route names get default names.
   Classic can no longer be changed once Prepare starts. You get a read-only view of the new profile.
3. **Enable managed identity and grant Key Vault access** (only if you bring your own certificate):
   system- or user-assigned identity, then *Grant* adds it to every Key Vault used by the classic profile.
   Managed certificates need neither.
4. **Migrate**: before committing you can *Abort*, which deletes the new profile (delete WAF policy
   copies by hand) and leaves classic active. After committing there is no abort or rollback:
   classic becomes Disabled (and can be deleted), the new profile becomes Active, and
   charges for Standard/Premium start. Deleting the new profile afterwards deletes production.

Migration states: Prepare = classic *Migrating* / new *Creating*; commit = *CommittingMigration*;
done = classic *Migrated* / new *Active*; abort = *AbortingMigration* then classic *Active*.
The documented path is the portal, PowerShell and the Learn migration articles; this skill does
not list CLI migrate commands because `az afd profile` has none in the reference.

## 3. After commit: endpoint cutover
- The classic endpoint (`contoso.azurefd.net`) keeps routing to the new profile, whose endpoint
  looks like `<endpointname>-<hash>.z01.azurefd.net`. Both work during the transition.
- Custom domains: update DNS to the new endpoint. Direct users of the classic default hostname:
  switch applications and clients to the new hostname.
- Finish cutover by March 31, 2028: from April 1, 2028 classic endpoints are unsupported and may stop working.
- Diagnostic logs and metrics are not migrated; log fields differ. Enable diagnostic settings on the
  new profile (health probe logging is available) and use the built-in reports.
- DevOps: resource provider changes from `Microsoft.Network` (classic) to `Microsoft.Cdn`; update
  scripts, modules and API calls.
- URL redirect/rewrite from classic routing rules become rule set rules named `urlRedirectMigrated`
  and `urlRewriteMigrated`.
- Azure Policy for Front Door WAF is not available on Standard/Premium.

## 4. Other Azure CDN migrations
Azure CDN from Edgio was retired on January 15, 2025 and the Learn article
`migrate-cdn-to-front-door` describes moving it to Front Door gradually with Traffic Manager
(the guide starts by routing 10 percent of traffic to Front Door). Retirement dates for Azure CDN from
Microsoft (classic) are not covered here; check the Azure updates page.

## Verify
- [ ] Validation passes; the prepared profile is reviewed in its read-only view.
- [ ] Key Vault access granted if BYOC certificates are used, before Migrate.
- [ ] After commit, DNS and clients point at the `z01.azurefd.net` endpoint, and diagnostics are on.

## Checked
2026-10-28. Confirmed against Learn `tier-migration` and `migrate-tier` (both last updated
2026-08-27): retirement date, tier selection by WAF rules, phases, abort/commit behaviour, resource
states, naming defaults, endpoint cutover and the March 31, 2028 deadline, logs not migrated,
Microsoft.Cdn namespace. Confirmed from `migrate-cdn-to-front-door`: Edgio retirement date and the
Traffic Manager gradual approach. Removed: the `az afd profile check-migration/migrate/migration-commit/
migration-abort` commands (not in the CLI reference), the CDN classic CLI flow and its 30 Sep 2027 date,
the claim that commit moves the classic hostname and deletes classic, the Terraform and IaC import advice,
the pricing line, and the Key Vault Secrets User role detail.
Method: documentation only; no commands were run.
