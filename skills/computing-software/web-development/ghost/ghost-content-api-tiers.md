---
id: computing-software.web-development.ghost.ghost-content-api-tiers
name: ghost-content-api-tiers
category: computing-software
field: web-development
product: ghost
tags: [ghost, content-api, tiers, membership, pricing, benefits]
level: practitioner
status: docs-checked
description: "Read Ghost membership tiers from the Content API, including how to include monthly and yearly prices and benefits."
sources:
  - https://github.com/TryGhost/docs/blob/main/content-api/tiers.mdx
  - https://github.com/TryGhost/docs/blob/main/content-api/parameters.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: show a site's membership tiers in a custom front end.

Endpoint: `GET /content/tiers/`. It returns the site's tiers filtered by their visibility criteria, in order of increasing monthly price. Fields in the sample: `id`, `name`, `description`, `slug`, `active`, `type` (`free` or `paid` in the samples), `welcome_page_url`, `created_at`, `updated_at`, `stripe_prices`, `benefits` and `visibility`.

The first sample response has `benefits: null` and no `monthly_price` or `yearly_price`. Request them with `include` (tiers support `monthly_price`, `yearly_price`, `benefits`):

`curl "https://example.com/ghost/api/content/tiers/?key=<KEY>&include=benefits,monthly_price,yearly_price"`

In the sample with those includes, the free tier has `monthly_price: null`, `yearly_price: null` and `benefits: []`; the paid tier has `monthly_price` and `yearly_price` as integers (500 and 5000 in the sample), `currency` (`usd` in the sample) and a `benefits` array. The response also carries `meta.pagination`.

Filtering: `filter=visibility:public` returns only publicly visible tiers (from the parameters page, browse requests only). Default order for tiers is `monthly_price ASC`.

Tip: render the pricing table from this endpoint rather than hard-coding prices.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, no imported snippets): content-api/tiers.mdx (110 lines) and content-api/parameters.mdx. Sample fields, includes, null and empty values, `visibility:public` filter and `monthly_price ASC` order confirmed. Removed: "5.00 monthly price" reading of 500 (page gives no unit), the claim that `welcome_page_url` is where Ghost sends new members, "paid tier and free tier" definitions beyond the sample values, and the Verify step. The page states no prose about the default omission of prices; that is taken from the first sample only.
Method: documentation only; no commands were run.
