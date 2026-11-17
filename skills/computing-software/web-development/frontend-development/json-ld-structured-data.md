---
id: computing-software.web-development.frontend-development.json-ld-structured-data
name: json-ld-structured-data
category: computing-software
field: web-development
product: frontend-development
tags: [json-ld-structured-data, schema-org-markup, rich-results, seo, structured-data, html]
level: practitioner
status: docs-checked
description: "Adding schema.org structured data as JSON-LD (Article, Product, BreadcrumbList, Organization), escaping it safely and validating with Rich Results Test."
sources:
  - https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
  - https://schema.org/docs/gs.html
  - https://validator.schema.org/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# JSON-LD structured data

## 1. Shape
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Trail Shoe 2",
  "image": ["https://example.com/p/shoe-1x1.jpg", "https://example.com/p/shoe-16x9.jpg"],
  "sku": "TS2-42",
  "brand": { "@type": "Brand", "name": "Example" },
  "offers": { "@type": "Offer", "price": "129.00", "priceCurrency": "GBP",
              "availability": "https://schema.org/InStock", "url": "https://example.com/p/ts2" },
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "212" }
}
</script>
```
Check Google's intro-to-structured-data page for supported formats.

## 2. Common types worth doing
| Type | Use |
|---|---|
| `Organization` / `WebSite` | home page: logo, `sameAs` profiles |
| `BreadcrumbList` | every deep page; `itemListElement` with `position`, `name`, `item` |
| `Article` / `BlogPosting` | `headline`, `datePublished`, `dateModified`, `author` (Person with `url`) |
| `Product` + `Offer` | price, availability, reviews |
| `Event`, `JobPosting`, `Recipe`, `LocalBusiness` | when the page really is one |
Rich result eligibility changes over time; check Google's current structured data gallery before adding a type.

## 3. Safe embedding
Never interpolate raw strings into the script block: serialise data with a JSON serialiser and check how your framework injects it.

## 4. Rules that cause manual actions
- Markup must describe content visible on the page (no hidden reviews, no fake ratings).

## Verify
- [ ] Google's Rich Results Test shows the type as eligible, no errors.
- [ ] validator.schema.org parses without warnings for non-Google types.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on Google's structured data intro, product, product snippet, breadcrumb, article, job posting, organization and policies pages and on schema.org Product, Offer and AggregateRating: script type application/ld+json, Product with offers (price, priceCurrency) and aggregateRating (ratingValue, reviewCount), BreadcrumbList, Article properties, JobPosting, Rich Results Test, markup must match visible content.

Removed: the escaping code sample, server-render claim and Search Console report wording (not on the pages read).

Method: documentation only; no commands were run.
