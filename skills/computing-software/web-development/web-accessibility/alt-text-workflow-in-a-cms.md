---
id: computing-software.web-development.web-accessibility.alt-text-workflow-in-a-cms
name: alt-text-workflow-in-a-cms
category: computing-software
field: web-development
product: web-accessibility
tags: [alt-text-workflow, alt-text, cms-accessibility, ai-generated-alt-text, content-authoring]
level: practitioner
status: docs-checked
description: "Running an alt text workflow in a CMS: making alt contextual per usage, required-field and decorative toggles, reviewing AI-generated alt text, and auditing image libraries."
sources:
  - https://www.w3.org/WAI/tutorials/images/decision-tree/
  - https://www.w3.org/WAI/tutorials/images/tips/
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html
  - https://github.com/dequelabs/axe-core/blob/HEAD/doc/rule-descriptions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alt text workflow in a CMS

Alt text is editorial content, not metadata. The same photo needs different alt text in different articles, so the workflow matters more than the field.

## 1. Data model
- Store a **default** alt on the media asset, but allow (and encourage) an override per placement (block/embed).
- Provide an explicit **"decorative"** checkbox that outputs `alt=""`; never leave alt empty by omission, and never output the filename.
- Separate fields for alt (what the image conveys) and caption (visible, for everyone); don't duplicate the caption into alt.

## 2. Authoring UI
- Show guidance inline: "Describe what this image conveys in this context. If the text around it already says it, mark decorative."
- Block publish (or warn) when an image has neither alt nor the decorative flag. Report missing alt in the editorial dashboard.
- Hint that alt is a short phrase or sentence; longer descriptions (charts, diagrams) go in body text or a linked description.
- Images that are links need alt describing the destination.

## 3. AI-generated alt text
Vision models produce plausible but generic or wrong descriptions ("a person smiling") and miss the reason the image is there.
- Treat as a **draft** prefilled for a human to edit; record whether the alt was reviewed.
- Never auto-publish generated alt for informative images (charts, product details, screenshots with text).
- Strip "image of", subjective guesses about identity, gender or emotion unless editorially verified.

## 4. Auditing an existing library
1. Export images with alt values and the pages that use them (your CMS's media export, or a database query).
2. Flag empty, filename-like (`IMG_1234`, `.jpg`), duplicate-of-title and very long alts.
3. Prioritise high-traffic pages and informative images; sample by template.
4. Automated checks (axe `image-alt`) catch missing alt, not bad alt; human review is required.

## Verify
- [ ] Editors cannot publish an image without alt or the decorative flag; per-placement overrides render; sample review confirms alt matches context.

## Checked

- Date: 2026-10-26. Documentation: W3C WAI Images tutorials, WCAG 2.2, axe-core rule descriptions (4.14).
- Confirmed: decorative images take an empty `alt`; alt should be the most concise description of purpose; linked images describe the destination; the axe `image-alt` rule exists and checks presence only.
- Removed (no documentation found): the 125-150 character hint, the WordPress block-versus-library statement and the WP-CLI recipe; the WordPress handbook link was dropped.
Method: documentation only; no commands were run.