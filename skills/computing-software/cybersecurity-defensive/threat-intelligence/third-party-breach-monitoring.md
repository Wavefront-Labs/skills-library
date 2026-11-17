---
id: computing-software.cybersecurity-defensive.threat-intelligence.third-party-breach-monitoring
name: third-party-breach-monitoring
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [third-party-breach-monitoring, digital-risk-protection, third-party-risk, supply-chain, vendor-risk, security-ratings]
level: practitioner
status: draft
description: "Monitor third parties for breaches and exposure: supplier watchlists, breach notifications, leak sites, security ratings and advisories, with triage into supplier response."
sources: ["https://csrc.nist.gov/pubs/sp/800/161/r1/final", "https://www.ncsc.gov.uk/collection/supply-chain-security", "https://www.cisa.gov/resources-tools/resources/defending-against-software-supply-chain-attacks"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Third-party breach monitoring

## Watchlist
From vendor management: suppliers with access to your data, network or identities, ranked by
criticality (tier 1 = holds sensitive data or privileged access). Include domains, brand names,
products used, and key subsidiaries. Sync automatically from the vendor inventory.

## Signals
- Leak sites and dark web mentions of suppliers.
- Breach disclosures: SEC 8-K Item 1.05 filings, regulator breach portals, supplier status pages and
  security advisories, news.
- Security ratings platforms (BitSight, SecurityScorecard) alerts on sharp score drops, exposed
  services, or infected hosts in supplier IP space.
- Vulnerability advisories for supplier products you run (PSIRTs, KEV).
- Credential leaks for supplier staff with access to your systems.

## Triage
1. Is the signal credible and about the right entity?
2. What does the supplier have of ours (data, access, software)?
3. Contact the supplier via contractual security contact; request confirmation and details in writing.
4. If plausible impact: start supplier breach response (credential rotation, access restriction,
   hunting, legal assessment).

## Reporting
Monthly to third-party risk management: signals, confirmed incidents, supplier responsiveness; feed
into supplier risk ratings and contract renewals.

## Gotchas
- Name collisions (common company names) cause false alarms; match on domains and context.
- Suppliers' sub-processors (fourth parties) are invisible without contractual disclosure.

## Verify
Watchlist coverage = 100% of tier 1/2 suppliers; each confirmed supplier incident has a recorded
response with timeline.
