---
id: computing-software.digital-privacy-hygiene.vpn-tools.vetting-a-vpn-provider-jurisdiction-and-payment
name: vetting-a-vpn-provider-jurisdiction-and-payment
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, vpn-jurisdiction, vpn-anonymous-payment, vpn-selection, no-logs-audit, ownership, account-number, cash-payment, monero, mullvad, ivpn, proton-vpn]
level: practitioner
status: draft
description: "Vet a VPN's ownership, jurisdiction, audits and account model, and sign up with minimal identity (account numbers, cash or crypto) where your threat model needs it."
sources:
  - "https://www.privacyguides.org/en/vpn/"
  - "https://ssd.eff.org/module/choosing-vpn-thats-right-you"
  - "https://mullvad.net/en/help/no-logging-data-policy"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vetting a VPN provider

**Goal:** choose a provider whose incentives and legal exposure match what you're
trusting it with.

## Ownership and jurisdiction
- Find the **operating company and parent**: many "independent review" sites and VPN
  brands are owned by a few conglomerates. Search the company registry and news.
- **Jurisdiction**: where the company is incorporated and where servers sit. Matters for
  compelled logging/data requests. No jurisdiction is magic; a provider that genuinely
  keeps no logs has little to hand over (real cases where providers had nothing to give
  are stronger evidence than marketing).
- Be wary of free VPNs and VPNs bundled with antivirus or browser "features".

## Evidence of no-logs
- Independent **audits** of infrastructure (not just the app) with public reports.
- Court cases or police raids with nothing found.
- RAM-only/diskless servers.
- Open-source clients.

## Account and payment privacy
| Provider pattern | What you give |
|---|---|
| Account number only (Mullvad, IVPN) | No email; random number |
| Email account (most) | Use an alias |
| Payment | Card links your identity; **cash by mail** (Mullvad, IVPN historically), Monero, or gift cards reduce linkage |

## Red flags
- "Military-grade encryption" + lifetime deals + affiliate-only reviews.
- Logs "connection timestamps and bandwidth" while claiming no-logs.
- Requires lots of personal info, or app requests broad permissions.

## Verify
- [ ] You can name the provider's owner, jurisdiction and latest audit.
- [ ] Sign-up method matches threat model (alias/no email; private payment if needed).
