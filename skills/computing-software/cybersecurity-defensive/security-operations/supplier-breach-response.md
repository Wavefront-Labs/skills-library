---
id: computing-software.cybersecurity-defensive.security-operations.supplier-breach-response
name: supplier-breach-response
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [supplier-breach-response, third-party-risk, incident-response, supply-chain, saas-security, token-rotation]
level: advanced
status: draft
description: "Respond when a supplier or SaaS provider is breached: impact assessment, credential and token rotation, data exposure analysis, contractual notices and monitoring."
sources: ["https://www.cisa.gov/resources-tools/resources/defending-against-software-supply-chain-attacks", "https://www.ncsc.gov.uk/collection/supply-chain-security", "https://csrc.nist.gov/pubs/sp/800/161/r1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Supplier and third-party breach response

## Trigger
Vendor notice, news/leak site claim, ISAC advisory, or your own detection (malicious updates,
anomalous API use by a vendor integration).

## Assess impact within hours
1. **Relationship map**: what the vendor has: data (types, volume, regulated?), network access
   (VPN, jump hosts), identities (accounts in your IdP, OAuth apps, API keys, service principals),
   software in your estate (agents, libraries, appliances).
2. **Exposure**: which of those the breach could affect according to vendor information; assume
   worst case until confirmed.
3. **Indicators**: request IOCs from the vendor; hunt for them across logs (retro-hunt the breach window).

## Contain
- Rotate secrets the vendor held: API keys, OAuth client secrets, SSH keys, service account passwords.
- Revoke OAuth grants/refresh tokens for the vendor app; review app permissions (consented scopes).
- Disable or restrict vendor VPN/jump access; require re-enrolment with MFA.
- For compromised software: block update channels, isolate affected appliances, follow vendor and
  CISA guidance (e.g. emergency directives).

## Data exposure
Determine what of your data was in the breached system; involve privacy/legal for notification
assessment (you may be the controller with obligations even though the vendor was breached).

## Contract and communication
- Invoke contract clauses: notification timelines, cooperation, audit rights, cost recovery.
- Ask structured questions in writing (dates, root cause, data affected, IOCs, remediation, attestations).
- Single point of contact; keep a log of vendor statements.

## Afterwards
Enhanced monitoring of vendor integrations for weeks, review vendor risk rating, minimise access and
data shared, and add supplier compromise to tabletop scenarios.

## Gotchas
- Vendor statements early on are often incomplete; plan for scope to grow.
- Forgotten integrations (old API keys) are common; inventory from logs, not only procurement records.

## Verify
Every credential linked to the vendor rotated (evidence list), hunt results documented, legal
notification decision recorded.
