---
id: computing-software.web-development.ghost.ghost-theme-content-card-css
name: ghost-theme-content-card-css
category: computing-software
field: web-development
product: ghost
tags: [ghost, theme, editor-cards, kg-image-card, kg-width-wide, css, content-helper]
level: advanced
status: docs-checked
description: "Style content produced by Ghost's editor: the kg card classes, wide and full width images and embed figure markup."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/content.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make a theme render editor cards correctly.

Themes must support the markup and classes output by the `{{content}}` helper, otherwise author-chosen options will not show.

Images and embeds are output with semantic figure and figcaption elements. Classes: `.kg-image-card` on the figure of all image cards, `.kg-image` on the img element, `.kg-embed-card` on embed card figures. Themes must also handle images and embeds that are not in figures, because Markdown and HTML cards can produce them.

Size options: images can be normal, wide or full width. Wide uses the class `kg-width-wide` and full uses `kg-width-full` on the figure; normal has no extra class. Image cards carry `width` and `height` attributes when that data is available, matching the source image.

If your theme sets a `max-width` on images, also set `height: auto` to avoid stretched or squashed images. How to make images wider than the container depends on your theme's styles; the page shows a flexbox approach and a negative-margin-and-transform approach. Images get `srcset` and `sizes` attributes where possible.

Editor card assets: Ghost outputs `cards.min.css` and `cards.min.js` through `{{ghost_head}}`. In the theme's `package.json`, `"card_assets": {"exclude": ["bookmark", "gallery"]}` excludes specific cards and `"card_assets": false` disables all (default is true). Cards listed: audio, blockquote, bookmark, button, callout, file, gallery, header, nft, product, toggle, video, signup. Class names include `.kg-audio-card`, `.kg-bookmark-card`, `.kg-button-card`, `.kg-callout-card`, `.kg-file-card`, `.kg-gallery-card`, `.kg-header-card`, `.kg-nft-card`, `.kg-product-card`, `.kg-toggle-card`, `.kg-video-card`, `.kg-signup-card`, and `blockquote` or `.kg-blockquote-alt`. Themes are validated for styles for `.kg-gallery-container`, `.kg-gallery-row` and `.kg-gallery-image`. Embed videos need CSS to keep their aspect ratio; the page's example is a `.fluid-width-video-wrapper` with `padding-top: 56.25%`.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 616 lines, no imported snippets): themes/content.mdx. The figure classes, size classes and width and height statement match. Removed as unconfirmed: the invented test plan and the Verify step. Added card_assets settings, card class names and gallery requirements from the page.
Method: documentation only; no commands were run.
