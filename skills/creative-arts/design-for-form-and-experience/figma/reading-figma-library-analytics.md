---
id: creative-arts.design-for-form-and-experience.figma.reading-figma-library-analytics
name: reading-figma-library-analytics
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [library-analytics, figma-analytics, component-usage, detachments, insertions, adoption-metrics, figma-libraries, figma]
level: practitioner
status: draft
description: "Read Figma library analytics to see component and style usage by team, insertions and detachments over time, and turn them into design system priorities."
sources:
  - "Figma Help Center - Library analytics (help.figma.com/hc/en-us/articles/4500009496215)"
  - "Figma Help Center - Analytics availability on Organization and Enterprise plans (help.figma.com)"
  - "Figma Developers - Library Analytics REST API (developers.figma.com/docs/rest-api/library-analytics-endpoints)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Library analytics

**Availability:** Organization and Enterprise plans; open from the library file (**Assets > Libraries > library name > Analytics**) or from the admin view.

## What it shows
- **Components:** number of **insertions** (instances placed) and **detachments** over time, **by team** and by component; the **top used** components, those **never used**.
- **Styles and variables:** usage counts across files, which styles are applied vs detached or overridden.
- **Teams and files:** which teams adopt the library and which do not; **usage by file** over a date range (weekly, monthly); **actions** (adds, detaches) trends.
- **Libraries in use:** versions published and how many files are on the latest version.

## How to use it
1. **Adoption:** compare library users to the team list; contact teams with low usage to find blockers (missing components, poor docs). Trend monthly into the system dashboard (`creative-arts.design-for-form-and-experience.design-systems.measuring-design-system-adoption`).
2. **Quality signal:** **high detachment rate** for a component means it fails real needs (missing variant, rigid layout); open an issue, add properties or variants.
3. **Cleanup:** deprecate **unused** components after confirming with code usage; archive.
4. **Roadmap:** prioritise improvements by use volume; large insertion counts justify polish and accessibility audits.
5. **Communicate:** share top insights in release notes and the status page.

## API access (Enterprise)
The **Library Analytics REST API** returns usage and action data by component, style and variable, per team and file; export weekly into a data warehouse or spreadsheet for dashboards. Needs a token with `library_analytics:read`.

## Gotchas
- Insertions count placing instances, not production use in code; combine with code coverage metrics.
- Detach counts include intentional one-off illustrations; sample files before concluding.

## Verify
- [ ] Monthly adoption and detachment trend captured.
- [ ] Top detached components investigated and fixed.
- [ ] Unused items reviewed for deprecation.
