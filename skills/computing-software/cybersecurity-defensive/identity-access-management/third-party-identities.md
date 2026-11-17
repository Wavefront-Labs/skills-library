---
id: computing-software.cybersecurity-defensive.identity-access-management.third-party-identities
name: third-party-identities
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [third-party-identities, contractor-accounts, b2b-collaboration, vendor-access, sponsor-model, identity-lifecycle, external-identities]
level: practitioner
status: draft
description: "Govern contractor and third-party identities: sponsor ownership, separate account types, B2B guests vs internal accounts, expiry dates, vendor remote access and offboarding."
sources: ["https://learn.microsoft.com/en-us/entra/id-governance/entitlement-management-external-users", "https://www.cisecurity.org/controls/v8", "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Contractor and third-party identities

Third parties are a top breach path (vendor credentials, stale contractor accounts). They are not in
HR, so joiner-mover-leaver automation misses them unless you build a source of truth.

## Model
- **Source of record:** a contractor register or VMS (vendor management system) feeding the IGA/IdP with sponsor, company, start, **end date**.
- **Sponsor:** every external identity has an internal sponsor accountable for need and recertification.
- **Account type:** prefer B2B guest (user authenticates at their own IdP; your Conditional Access still applies) over creating internal accounts. Where internal accounts are needed (device logon, legacy apps), mark them (`employeeType=Contractor`, naming prefix) and put them in a dedicated OU/admin unit.
- **Expiry:** mandatory `accountExpires` / Entra lifecycle workflows; maximum 90-180 days, extension via sponsor approval.
- **Access packages** (Entra entitlement management) for connected organisations with automatic expiry and access reviews.

## Vendor remote access
Through a PAM/ZTNA gateway with session recording, per-session approval, MFA, no standing VPN accounts.

## Offboarding
Contract end -> account disabled same day; sponsor departure triggers sponsor reassignment or
disablement of all sponsored accounts.

## Gotchas
- Shared vendor accounts ("vendorsupport") break accountability; issue named accounts.
- Guests inviting other guests; restrict guest invite settings.
- Guest accounts persist after the partner's own IdP deletes the user (they lose sign-in, but group memberships remain until removed).

## Verify
- [ ] 100% of external accounts have sponsor and end date.
- [ ] No external account active past its end date.
- [ ] Quarterly sponsor access review completed.
