---
id: media-communication.content-creation-and-audience-growth.cms-platforms.content-modelling-for-editorial-cms
name: content-modelling-for-editorial-cms
category: media-communication
field: content-creation-and-audience-growth
product: cms-platforms
tags: [cms, cms-platforms, content-modelling, content-model, content-types, headless-cms, contentful, sanity, drupal, strapi, storyblok, arc-xp, newsroom-cms, structured-content, references, editorial-workflow, multi-channel-publishing, cms-selection, cms-migration, fields, validation, localisation]
level: practitioner
status: draft
description: "Design an editorial content model in a CMS (Drupal, Contentful, Sanity, newsroom systems): types, fields, references, workflow states, and how to choose or migrate a CMS."
sources: ["https://www.contentful.com/help/", "https://www.sanity.io/docs", "https://www.drupal.org/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Content modelling for an editorial CMS

**Goal:** structure content so one story can be published to web, app, newsletter and
syndication without copy-paste, and editors can work fast without breaking the site.
Applies to Drupal, Contentful, Sanity, Strapi, Storyblok and newsroom CMSes (Arc XP-class).
For WordPress specifically see
`media-communication.content-creation-and-audience-growth.wordpress.editorial-publishing-workflow`.

## 1. Model content, not pages
The core mistake is modelling "Homepage" and "Article page". Model the **things**:
- **Article** — headline, dek/standfirst, body (rich text), slug, publish date, updated
  date, section (reference), authors (references, many), lead media (reference),
  tags (references), SEO fields (title, description, canonical URL), corrections (list).
- **Author** — name, slug, bio, photo, role, social links.
- **Section / Topic** — name, slug, description, parent.
- **Media asset** — file, alt text (required), caption, credit, rights/expiry.
- **Series**, **Newsletter issue**, **Promo/Collection** (an ordered list of references
  an editor curates — this is what powers a homepage).
Pages are then *views* assembled from collections and queries.

## 2. Field rules that save you later
- **References over repeated text.** An author is a reference, never a typed name, or
  you'll have "J. Smith", "Jane Smith" and "Jane Smith " forever.
- **Required fields at the source:** alt text, credit, section. Validation in the CMS
  beats a style memo.
- **Separate display from data:** `headline` and optional `social_headline`/`seo_title`
  instead of one field forced to do three jobs.
- **Rich text that stays structured:** allow embeds (pull quote, image, related link) as
  typed blocks, not raw HTML. Raw HTML embeds break on app/AMP/email outputs.
- **Dates:** keep `first_published` and `last_updated` separate; never overwrite the first.
- Name fields consistently (`snake_case` or `camelCase`, pick one) — API consumers see them.

## 3. Workflow states and permissions
Minimum: Draft › In review › Ready › Scheduled › Published › Unpublished/Archived.
Map who can move content between states (writer can't publish; desk editor can).
Headless platforms differ: Contentful and Sanity offer workflow/release features on
some tiers; Drupal uses the Content Moderation module. *Check which tier includes
workflows before you promise it to the newsroom.*

## 4. Choosing a CMS (questions to ask)
1. Who edits, how many, how fast? A breaking-news desk needs fast preview and
   live-updating stories; a monthly magazine doesn't.
2. Headless (you build the front end; Contentful/Sanity/Strapi) or coupled (Drupal,
   WordPress)? Headless = flexibility + a permanent developer cost.
3. Preview: can editors see the real page before publishing? Headless setups often fail here.
4. Exit: can you export all content and assets in a usable format (JSON, with references)?
5. Pricing model: per-seat, per-record, per-API-call — model it at 3× today's volume.
Run a two-week pilot with real editors and real stories before signing.

## 5. Migration checklist
- Inventory: count every type, field and the weird legacy cases (embedded HTML, galleries).
- Map old → new fields in a spreadsheet; decide what's dropped.
- Script the migration (via CMS import APIs); rerun it until it's clean — don't hand-fix.
- Preserve URLs or create **301 redirects** for every changed path.
- Freeze edits on the old system for the cutover window; re-sync deltas.

## Gotchas
- Over-modelling: 40 content types nobody understands. Start small; add types when a
  real use repeats three times.
- Changing a field type after launch usually needs a content migration script.
- Localisation multiplies everything — decide field-level vs entry-level translation up front.

## Verify
- [ ] One article renders correctly on web, in a newsletter template and via the raw API.
- [ ] Author, section and tags are references; no free-text author fields remain.
- [ ] Publishing without alt text or section is blocked by validation.
- [ ] An editor can preview an unpublished story exactly as readers will see it.
- [ ] A full content export has been produced and opened once.
