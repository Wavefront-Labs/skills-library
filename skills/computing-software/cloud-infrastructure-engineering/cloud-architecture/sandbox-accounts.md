---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.sandbox-accounts
name: sandbox-accounts
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, sandbox-accounts, sandbox-subscription, experimentation, budget-guardrails, auto-cleanup, aws-nuke]
level: practitioner
status: draft
description: "Provide sandbox accounts for experimentation with isolation from corporate networks, budgets and hard limits, restricted services, expiry and automated cleanup."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/considerations/sandbox-environments", "https://docs.aws.amazon.com/prescriptive-guidance/latest/designing-control-tower-landing-zone/sandbox.html", "https://github.com/ekristen/aws-nuke"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sandbox accounts and their guardrails

## Design
- Separate sandbox management group / OU / folder with its own policies.
- **No connectivity** to corporate networks or production (no peering to the hub); internet only.
- No production or sensitive data (policy + training).
- **Budgets** per sandbox with alerts at 50/80/100% and automated action at 100% (stop/deny).
- **Restricted services and SKUs**: deny expensive instance families/GPUs, marketplace purchases,
  reservations/commitments, and regions outside the allowed set.
- **Lease model**: sandbox expires after N days (30-90); renew on request.
- **Cleanup**: on expiry, delete resources (aws-nuke / cloud-nuke, resource group deletion,
  project deletion) and recycle or close the account.

## Steps
1. Create the OU/management group with SCPs/policies above.
2. Vending: self-service request with owner, purpose, budget, expiry tag.
3. Automate expiry notifications (7 days, 1 day) and cleanup.
4. Report active sandboxes, spend and expired-but-not-cleaned.

## Gotchas
- aws-nuke is destructive; run only against sandbox account IDs with an explicit allow-list config.
- Budgets are not hard caps by default; cost lags hours, so add usage restrictions too.
- Sandboxes quietly becoming production. Expiry forces migration to a proper account.

## Verify
- [ ] Sandbox cannot reach corporate networks (test).
- [ ] Expired sandbox cleaned automatically.
