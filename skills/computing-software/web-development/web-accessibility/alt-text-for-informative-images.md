---
id: computing-software.web-development.web-accessibility.alt-text-for-informative-images
name: alt-text-for-informative-images
category: computing-software
field: web-development
product: web-accessibility
tags: [text-alternatives, informative-images, alt-text, wcag-1-1-1, images]
level: practitioner
status: docs-checked
description: "Writing alt text for informative images: describing purpose not appearance, context-dependent wording, length, linked images, and what not to include."
sources:
  - https://www.w3.org/WAI/tutorials/images/informative/
  - https://www.w3.org/WAI/tutorials/images/decision-tree/
  - https://www.w3.org/WAI/tutorials/images/functional/
  - https://www.w3.org/WAI/tutorials/images/tips/
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alt text for informative images

## 1. Principle
Alt text conveys the **information or function** the image provides in this context - what a sighted user gets from it - not a visual inventory.

## 2. Examples
| Image | Context | Alt |
|---|---|---|
| Photo of a red trail-running shoe | product page | `alt="Trailblazer 3 running shoe in red, side view"` |
| Same photo | blog post about running form | `alt="Runner's foot landing mid-sole on a rocky trail"` (what matters there) |
| Company logo in header linking home | link | `alt="Acme home"` |
| Logo in footer, next to text "Acme Ltd" | redundant | `alt=""` |
| Screenshot of an error dialog | tutorial | the error text verbatim |
| Photo of the CEO next to her name and bio | supporting | `alt=""` or short "Portrait of Dana Lee" |
| Image of a sign reading "Closed Mondays" | informative text | `alt="Closed Mondays"` |

## 3. Rules
- Usually leave out words like "image", "icon" or "picture": screen readers announce the image. Name the medium (photograph, painting, illustration) only when it matters.
- Be concise: give the most concise description of the image's purpose, a short phrase or sentence. Anything longer belongs in a long description (see the complex images skill).
- Linked image (only content of the link): alt describes the **destination/action**, not the picture.
- Include text that appears in the image if it conveys information.
- Don't duplicate adjacent caption/text; if the caption says it all, `alt=""` may be right, or keep alt short and complementary.
- Use normal punctuation, and add a space in the alt text where the image sits directly against adjacent text so words do not run together.

## 4. Who writes it
Alt text is content: authors/editors write it in the CMS per usage. Make the field required with an explicit "decorative" checkbox (sets `alt=""`), not a filename default. AI-generated alt text is a draft - it describes appearance and misses context.

## 5. Markup
`<img src alt>` always has an `alt` attribute. CSS background images can't have alt - don't use them for informative images. `<input type="image" alt="Search">`.

## Verify
axe `image-alt`; read the page with images off (or a screen reader) - does the text still convey everything? Spot-check CMS content for filenames and "image" alt values.

## Checked

- Date: 2026-10-26. Documentation: W3C WAI Images tutorials (informative, functional, tips, decision tree) and WCAG 2.2.
- Confirmed: alt conveys meaning or function rather than a literal description; a linked logo's alt names the destination (for example "W3C home"); a logo inside link text with the same words gets `alt=""`; `<input type="image">` takes `alt`; words like "image" or "picture" are normally unnecessary; punctuation and spacing in alt text; CSS backgrounds suit decorative images only.
- Removed (no documentation found): the 125-character figure, the claim that screen readers pause on periods, the `title` attribute remark and the `<picture>` placement sentence.
Method: documentation only; no commands were run.