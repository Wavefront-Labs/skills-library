---
id: creative-arts.graphic-design.editorial-layout.editorial-templates-for-issue-production
name: editorial-templates-for-issue-production
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, editorial-templates, indesign-template, style-sheets, magazine-design, issue-production, incopy, parent-pages, style-guide, indt]
level: advanced
status: draft
description: "Build editorial issue templates: INDT with parent pages, full style sheets, layers and object styles, an editors style guide, and versioned template upkeep."
sources:
  - https://helpx.adobe.com/indesign/using/creating-documents.html
  - https://helpx.adobe.com/incopy/using/incopy-workflows.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Editorial templates and style sheets for issue production

**Goal:** each issue starts from a template that already contains the grid, styles and recurring page
designs, so designers lay out content instead of rebuilding the magazine every month.

## Template contents (InDesign .indt)
- **Document setup:** trim, bleed, slug with job info text variables (issue, page, file name).
- **Parent pages:** one per page type (feature, department A/B, news, contents, back page), based on a root
  parent with folios and running heads (see parent-pages-based-on-parents skill).
- **Layers:** Text, Images, Ads/Placeholders, Notes (non-printing), Guides.
- **Styles:** paragraph styles in groups (Headlines, Body, Captions, Credits, Departments), based-on chains
  from one root body style; character styles for run-ins, bylines, prices; object styles for picture
  frames, sidebars, caption frames; table and cell styles for listings.
- **Swatches:** brand and section colours only; delete defaults that are unused.
- **Placeholder frames** labelled for each element (headline, standfirst, credit) on page types.
- **Preflight profile** embedded for the printer's requirements.

## Style guide for the team
- A one-page-per-element guide: which style for what, word counts per element (headline 4-8 words, standfirst
  30 words), image ratios and minimum resolution, how to handle pull quotes and credits.
- Share with editors so copy arrives fitting the templates; with InCopy, assignments use the same styles.

## Maintenance
- Change the **template**, not issue files, when the design evolves; log changes with dates.
- Save the template with a version in the file name (`Mag_Template_v2026-10.indt`) and keep old versions.
- Load styles into in-progress issues from the template (Paragraph Styles panel > Load All Text Styles) when
  a definition changes mid-issue.

## Gotchas
- Local overrides (plus signs on styles) creep in issue by issue; clear them and update the template if they
  are real design changes.
- Fonts not licensed for every team member break templates; specify font versions and sources.
- Too many parent pages confuse designers; consolidate after each redesign.

## Verify
- [ ] A new issue file built from the template passes preflight with no added styles.
- [ ] Every recurring page type has a parent page and placeholders.
