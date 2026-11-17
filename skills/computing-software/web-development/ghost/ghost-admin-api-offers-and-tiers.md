---
id: computing-software.web-development.ghost.ghost-admin-api-offers-and-tiers
name: ghost-admin-api-offers-and-tiers
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, offers, tiers, paid-membership, stripe]
level: advanced
status: docs-checked
description: "Create Ghost paid tiers and discount offers via the Admin API with the required fields and fixed-offer currency rule."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/offers/creating-an-offer.mdx
  - https://github.com/TryGhost/docs/blob/main/admin-api/tiers/creating-a-tier.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define a paid tier and a discount offer programmatically.

Tier: `POST /admin/tiers/` with required `name`. The endpoint creates public and hidden tiers. New tiers are always `active`. The docs example creates a paid tier with custom monthly and yearly prices, description, benefits and a welcome page.

Offer: `POST /admin/offers/` with required fields `name`, `code`, `cadence`, `duration`, `amount`, `tier.id` and `type`. When `type` is `fixed`, `currency` is also required and must match the tier's currency. New offers are created as active by default.

Sequence:
1. Create (or look up) the tier and record its id.
2. Create the offer pointing at `tier.id`.
3. Share the offer's code with members.

The Admin API endpoint table lists Browse, Read, Edit and Add for tiers and offers (no Delete).

Verify: read the tier through the Content API with `include=monthly_price,yearly_price,benefits` and check the numbers.

## Checked

2026-11-04. Confirmed: required tier and offer fields, public and hidden tiers, always-active new tiers, fixed offers needing a matching currency, default-active offers (creating a tier and creating an offer pages), Content API tier includes. Removed: the Stripe gotcha and the "updates have their own pages" pointer, which these pages do not support.

Method: documentation only; no commands were run.
