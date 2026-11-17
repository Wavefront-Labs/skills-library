---
id: computing-software.web-development.web-performance.cls-image-video-iframe-dimensions
name: cls-image-video-iframe-dimensions
category: computing-software
field: web-development
product: web-performance
tags: [cls, image-dimensions, aspect-ratio, layout-shift, core-web-vitals]
level: practitioner
status: docs-checked
description: "Preventing layout shifts from media: width and height attributes, CSS aspect-ratio, responsive images with art direction, iframes and embeds."
sources:
  - https://web.dev/articles/optimize-cls
  - https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image, video and iframe dimensions

## 1. Always set width and height
web.dev: always include `width` and `height` attributes on images and video elements, or reserve the space with CSS `aspect-ratio` or similar, so the browser can allocate space while the image loads.
```html
<img src="puppy.jpg" width="640" height="360" alt="Puppy with balloons">
```
```css
img { width: 100%; height: auto; }
```
Modern browsers calculate a default aspect ratio from the `width` and `height` attributes as the HTML is processed (Chrome shows `aspect-ratio: auto 640 / 360`). Once CSS sets a width such as `width: 100%`, that ratio gives the height, so the box is the right size before the image loads.

## 2. Responsive and art-directed images
- With `srcset`, each image should use the same aspect ratio so the `width` and `height` attributes can be set.
- With `<picture>` and different crops, set `width` and `height` on each `<source>` as well as the `<img>`; web.dev says Chrome, Firefox and Safari support this:
```html
<picture>
  <source media="(max-width: 799px)" srcset="puppy-480w-cropped.jpg" width="480" height="400" />
  <source media="(min-width: 800px)" srcset="puppy-800w.jpg" width="800" height="400" />
  <img src="puppy-800w.jpg" alt="Puppy with balloons" width="800" height="400" />
</picture>
```

## 3. Ads, embeds and iframes
Ads, embeds, iframes and other dynamically injected content can push later content down and increase CLS. Embed widgets often do not know their size before they load, and platforms do not always reserve space for them.
- Reserve space with a `min-height` rule, or for responsive content use CSS `aspect-ratio`, in the way browsers do automatically for images with dimensions.
- When the exact height is unknown (ads), a larger container or the most likely size from historical data avoids shifts at the cost of more blank space; alternatively set the initial size to the smallest size used and accept some shift for larger content. `min-height` lets the parent grow compared with the 0px default of an empty element.
- `aspect-ratio` (MDN) defines the desired width-to-height ratio of an element's box, for example `aspect-ratio: 16 / 9;`.
```css
.embed { aspect-ratio: 16 / 9; width: 100%; }
```

## 4. Late-appearing UI
Banners and forms that pop in at the top or bottom shift the page. Reserve space in advance (placeholder or skeleton UI), or overlay the content so it is outside the document flow.

## 5. Field data caveat
Shifts inside iframes cannot be measured from Web APIs but are visible to users and included in CrUX, so field data from RUM tools such as the web-vitals library may be incomplete.

## Verify
- [ ] Lighthouse's audit for images missing width and height is clean, and the Performance panel's Layout Shifts track shows no shifts from media (web.dev describes both).

## Checked
2026-11-09. Read the media, ads/embeds, late UI and diagnosis sections of web.dev "Optimize Cumulative Layout Shift" and the MDN `aspect-ratio` page (searched for the syntax; not read end to end). Removed (not on those pages): the `max-width` and `video` rule, the object-fit remark, CMS and framework image components, the `(width < 600px)` range syntax, Rendering-panel Layout Shift Regions, `largestShiftTarget` attribution, the claim that lazy loading without dimensions shifts on scroll as stated (the page only says lazy-loaded content without reserved space causes post-load shifts), and the 640 by 360 stretch history.
Method: documentation only; no commands were run.
