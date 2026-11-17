---
id: computing-software.cybersecurity-defensive.application-security.api-inventory-management
name: api-inventory-management
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [api-security, api-inventory, shadow-apis, zombie-apis, openapi, api-discovery, api-gateway]
level: practitioner
status: docs-checked
description: "Build and maintain an API inventory: discover endpoints from gateways, traffic and code, record owner, version and data class, and retire shadow and zombie APIs."
sources: ["https://owasp.org/API-Security/editions/2023/en/0x11-t10/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API inventory management

**Goal:** one list of every API host, version and endpoint you expose, with an owner, so nothing
undocumented or deprecated stays reachable.

## Sources to reconcile
1. **Gateways and load balancers:** export routes from your API gateways and ingress objects.
2. **Code:** OpenAPI files in repos and framework route dumps.
3. **Traffic:** WAF/gateway logs grouped by host+method+normalised path; reveals endpoints not in any spec.
4. **External:** DNS and certificate transparency records for your API and staging hostnames.

## Inventory record
`host | base path | version | owner team | environment | auth type | data classification | internet exposed | spec link | status (active/deprecated/retire-by)`.

## Process
- New APIs register in the inventory as part of the release checklist; CI fails if a service has no spec.
- Diff traffic-observed endpoints against the spec weekly; unknown endpoints get a ticket to the owner.
- Deprecation: announce, monitor callers, then remove the route and DNS.
- Non-production APIs must not be internet-reachable with production data.

## Gotchas
- Old versions kept for one big customer quietly lose patching; give them an owner or kill them.
- Mobile apps hard-code endpoints; check app binaries for hosts.
- Inventory without data classification cannot prioritise testing.

## Verify
- [ ] Every gateway route maps to an inventory row with an owner.
- [ ] No traffic to endpoints marked retired.
- [ ] Staging/dev API hosts are not publicly resolvable or are access-restricted.

## Checked

2026-10-28. Confirmed in the OWASP API Security Top 10 2023 list: API9:2023 Improper Inventory Management (documentation of exposed endpoints). Removed: the `get-rest-apis`, Kong `GET /routes`, `kubectl get ingress -A`, `rails routes`, actuator `mappings` and `/openapi.json` examples, the `Deprecation`/`Sunset` headers and RFC 8594, and the `api.*` host patterns; none were in the fetched pages. NIST SP 800-228 and OpenAPI 3.1 were dropped from sources (not fetched).
Method: documentation only; no commands were run.
