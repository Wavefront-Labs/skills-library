---
id: computing-software.cloud-infrastructure-engineering.azure.conditional-access-for-workload-identities
name: conditional-access-for-workload-identities
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, conditional-access, ca-workload-identity, service-principal-risk, workload-identities-premium, service-principals]
level: advanced
status: gated
description: "Restrict service principal sign-ins with Conditional Access for workload identities: location lock-down, service principal risk blocking, scope and licensing limits."
sources: ["https://learn.microsoft.com/entra/identity/conditional-access/workload-identity", "https://learn.microsoft.com/entra/id-protection/concept-workload-identity-risk", "https://learn.microsoft.com/entra/workload-id/workload-identities-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional Access for workload identities

**Goal:** a leaked client secret for a pipeline service principal should be useless from anywhere except your
known egress IPs.

## Scope and prerequisites
- Licence: Workload Identities Premium licences are required to create or modify Conditional Access policies scoped to service principals.
- Applies to **single-tenant service principals registered in your tenant**. Not covered: managed identities,
  Microsoft and third-party SaaS / multitenant apps' service principals.
- Grant control: **Block access** is the only option. Conditions: locations and service principal risk.

## Location lock-down policy
1. Named location with the egress IPs of build agents / NAT gateways.
2. New policy, assignment target = **Workload identities**, select the service principals.
3. Conditions > Locations: include Any location and exclude the selected locations you want to allow.
4. Grant: Block access. Save in **Report-only** first to estimate the effect.

## Risk-based policy
Conditions > Service principal risk: set Configure to Yes and select the risk levels to block. The policy applies only
when a service principal requests a token. Risk is surfaced in Identity Protection (Risky workload identities).
Which levels to block first is your call: start narrow.

## Monitor
Service principal sign-ins appear in the Microsoft Entra service principal sign-in logs; make sure the diagnostic
setting exports that category before querying it in Log Analytics (exact table name and columns not confirmed
(gated: unconfirmed, source is paywalled or blocked)).

## Gotchas
- Hosted agents (GitHub-hosted, Microsoft-hosted DevOps) use wide, changing IP ranges: location policies suit
  self-hosted agents behind a NAT gateway. Consider workload identity federation to remove secrets entirely.
- Continuous access evaluation for workload identities gives faster enforcement of location and risk policies than waiting for token expiry.
- Block "all owned service principals" only after report-only shows no surprises.

## Verify
- [ ] Report-only shows expected allows from agent IPs; a token request from another IP is blocked.

## Checked
2026-10-28. Confirmed (Learn: conditional-access/workload-identity, id-protection/concept-workload-identity-risk,
workload-id/workload-identities-overview): Workload Identities Premium requirement, single-tenant scope, managed identities
and SaaS/multitenant excluded, Block access as the only grant, locations and service principal risk conditions, report-only,
token-request evaluation, CAE for workload identities. Removed: error code 53003 for this case, the High/Medium risk
levels, the named detection list, "token lifetime" detail. Gated: the sign-in log table name.
Method: documentation only; no commands were run.
