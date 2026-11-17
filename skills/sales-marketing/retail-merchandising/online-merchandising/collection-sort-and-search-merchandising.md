---
id: sales-marketing.retail-merchandising.online-merchandising.collection-sort-and-search-merchandising
name: collection-sort-and-search-merchandising
category: sales-marketing
field: retail-merchandising
product: online-merchandising
tags: [online-merchandising, ecommerce-merchandising, digital-shelf, retail-merchandising, collections, category-pages, product-sort-order, pinning, boosting, burying, search-merchandising, synonyms, zero-results, cross-sell, recommendations, shopify, shopify-search-and-discovery, algolia, bloomreach, plp, pdp, conversion-rate]
level: practitioner
status: draft
description: "Merchandise an online store: curate collections, set sort rules (pin, boost, bury), fix site search with synonyms and zero-result redirects, and place cross-sells on product pages."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Collection, sort and search merchandising — the digital shelf

**Goal:** the products a shopper is most likely to buy (and you most want to sell) appear
in the first rows of every collection and search, and every product page offers a
sensible next item.

## 1. Collections (category pages / PLPs)
- Build collections around how customers shop: by type ("dresses"), occasion ("wedding
  guest"), and need ("under £50"). Use **automated/smart collections** driven by product
  tags or attributes (e.g. Shopify: *Products › Collections › Create › Automated*, with
  conditions like `Product tag is wedding-guest`) so new stock lands in them automatically.
- Tag hygiene is the foundation: a controlled tag list (lowercase, documented) beats
  free-for-all tags. Audit monthly for products in no collection.
- Keep collections at a size that pages well: hundreds of items need filters (size,
  colour, price) — make sure filter attributes are filled for every product.

## 2. Sort order — the first two rows matter most
Most shoppers on mobile see 4–6 products before scrolling. Decide the default sort per
collection:
- **Best selling** for evergreen categories; **newest** for fashion drops; **manual** for
  editorial/campaign collections.
- **Pin** hero products to the top positions; **boost** by a business signal (margin,
  stock depth, new-in); **bury/demote** items with broken size runs (e.g. fewer than 3
  sizes available) or out of stock. Out-of-stock at position 1 is the costliest mistake.
- In Shopify, manual sort is drag-and-drop per collection; rule-based boosting and burying
  usually needs a merchandising/search app (Shopify Search & Discovery offers boosts
  on search; Algolia, Bloomreach, Klevu and others offer rules). Exact menus vary by app — check
  the app's docs.

## 3. Search merchandising
1. Export the **top 100 search terms** and the **zero-result terms** from your search
   analytics (Shopify: *Analytics › Reports › Top online store searches* and *with no
   results*; names vary by plan/version).
2. Fix zero results with **synonyms** (`hoodie, hooded sweatshirt, hoody`), misspellings, and
   redirects (search "returns" → returns policy page).
3. For the top 20 terms, check the first row of results by hand. Pin the right products
   for high-volume, high-intent queries ("black dress", "gift for dad").
4. Repeat monthly; seasonal terms shift fast.

## 4. Cross-sell slots on product pages (PDP)
- Two slots usually beat five: **"complete the look / goes with"** (complementary) and
  **"you may also like"** (substitutes, for shoppers about to bounce).
- Set **manual complementary products** for top sellers (Search & Discovery app supports
  complementary products in Shopify); let the algorithm fill the long tail.
- Exclude out-of-stock and much higher-priced items from complementary slots.

## 5. Measure
Per collection and search term: click-through from list to product, add-to-cart rate,
conversion, revenue per visit. Change one thing at a time; compare 2+ weeks against the
same period before (or A/B test if your platform supports it).

## Gotchas
- Manual sorts rot: a pinned product sells out and sits at position 1. Review pinned
  slots weekly or use rules that auto-demote out-of-stock.
- Boosting margin too hard tanks conversion; blend signals.
- Search analytics often lowercase and truncate terms — group variants before deciding.
- Platform menu paths above are from memory and change frequently; confirm in-app.

## Verify
- [ ] Every product sits in at least one collection; filter attributes complete.
- [ ] No out-of-stock or broken-size item in the first two rows of any key collection.
- [ ] Top 20 zero-result terms fixed with synonyms or redirects.
- [ ] Top 20 search terms show the right products in row one.
- [ ] Best sellers have hand-picked complementary products.
- [ ] Conversion and revenue/visit tracked per change against a baseline.
