---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-for-scanning-patterns
name: designing-for-scanning-patterns
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [f-pattern, scanning-patterns, layer-cake-pattern, eye-tracking, visual-hierarchy, content-layout, ui-layout]
level: practitioner
status: draft
description: "Lay out pages for how people scan: F-pattern and layer-cake behaviour, front-loading, headings, focal points, and what to place where."
sources:
  - "Nielsen Norman Group - F-Shaped Pattern For Reading Web Content (nngroup.com/articles/f-shaped-pattern-reading-web-content)"
  - "Nielsen Norman Group - Text Scanning Patterns: Eyetracking Evidence (nngroup.com/articles/text-scanning-patterns-eyetracking)"
  - "Nielsen Norman Group - Page Layouts and eye tracking (nngroup.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scanning patterns

**Goal:** put the most important content where people actually look, and make pages scannable.

## Patterns from NN/g eye tracking
- **F-pattern:** on text-heavy pages without structure, people read the first lines fully, then scan a shorter horizontal line, then run down the left edge. Cause: poor formatting, not a law to design for.
- **Layer-cake pattern:** on pages with clear headings and subheads, people scan the headings and read selected parts: the best-case scanning behaviour.
- **Spotted pattern:** skipping to find specific items (links, numbers, bolded words).
- **Commitment pattern:** when users are engaged, they read most of the text.
- Z-pattern and gaze order depend on layout and imagery; do not treat them as rules for complex screens.

## Design implications
1. **Front-load:** the first two words of headings, bullets and paragraphs carry meaning.
2. **Strong left edge:** key labels, first words of list items, and navigation start on the left (in LTR languages).
3. **Descriptive headings and subheads** at a regular interval; bullets and short paragraphs; bold key phrases sparingly.
4. **Place the key content above and around the first screen,** but people do scroll when content signals more (partial cut-off rows, clear structure).
5. **One focal point per view:** size, contrast and whitespace direct the eye to the primary action.
6. **Use images that carry information** (faces looking toward content, annotated screenshots) rather than decorative stock; users skip banner-like elements (banner blindness).

## Verify
- [ ] Headings alone communicate the page's story.
- [ ] Each paragraph and list item starts with its key word.
- [ ] The primary action is visually dominant and sits on the strong left or top region.
