---
id: creative-arts.design-for-form-and-experience.figma.publishing-and-updating-a-figma-library
name: publishing-and-updating-a-figma-library
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [library-publishing, library-updates, figma-libraries, team-library, publish-library, library-changes, review-changes, figma]
level: practitioner
status: docs-checked
description: "Publish a Figma team library, write release notes, review the asset list, and update consuming files safely, with versioning conventions and handling of breaking changes."
sources:
  - https://help.figma.com/hc/en-us/articles/360025508373-Publish-styles-and-components-to-a-library
  - https://help.figma.com/hc/en-us/articles/360039150733-Update-libraries-in-files
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing and updating a Figma library

## Publish
1. Keep the library in its own file: components, styles, variables, with documentation pages.
2. Open the **Assets** tab, click the **Libraries** icon, and under **This file** click **Publish**.
3. Add a description (Figma prompts for one on every publish and shows it to people accepting updates and in version history), review the list of added, modified and removed assets, and uncheck anything not ready. Example release note: "Button: added Loading state; renamed Ghost to Tertiary".
4. On Organization or Enterprise plans, pick where to publish from the dropdown, then click **Publish**.
5. Link release notes to code releases (`creative-arts.design-for-form-and-experience.design-systems.versioning-deprecating-and-changelogging`).

Requirements: edit access to the file; Professional, Education, Organization, Government or Enterprise plan (Starter cannot publish). Edits to the source file do not reach other files until published. To keep an asset out of future publishes, right-click it and choose **Hide when publishing**.

## Consumers
- Users of the library see a blue badge on the library icon in their sidebar and can review and accept updates.
- Instances keep overrides when you swap variants if layer names match. Instance structure cannot be changed; to reorder layers you must detach the instance or edit the main component.
- Changes to a component in a published library cannot be pushed from another file's instance; edit the library file and publish.

## Practice (team convention, not Figma rules)
- Publish small and often; keep unfinished work on a branch (`creative-arts.design-for-form-and-experience.figma.branching-and-merging-library-files`).
- Deprecate before removing: keep the old variant with a notice, remove in a planned release.
- Announce changes with a changelog link; review library analytics afterwards (`creative-arts.design-for-form-and-experience.figma.reading-figma-library-analytics`).

## Verify
- [ ] Every publish has a reviewed asset list and a description.
- [ ] Breaking changes are deprecated first and communicated.
- [ ] Consumer files updated or notified.

## Checked
2026-11-01. Confirmed on the Figma Help Center pages Publish styles and components to a library, and Update libraries in files: publish steps, description prompt, badge, Hide when publishing, access and plan requirements, override and detach behaviour. Removed: Alt+3 shortcut, admin enablement and org-wide library claims, "Update all" and "Review changes" wording, version rollback steps, since neither page stated them.
Method: documentation only; no commands were run.
