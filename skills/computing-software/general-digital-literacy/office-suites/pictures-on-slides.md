---
id: computing-software.general-digital-literacy.office-suites.pictures-on-slides
name: pictures-on-slides
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slide-content, slide-images, crop-to-shape, align-objects, compress-pictures, stock-images]
level: intro
status: docs-checked
description: "Insert, crop, crop-to-shape, align and compress pictures on slides and use licensed stock images in PowerPoint, Google Slides and Impress."
sources:
  - https://support.microsoft.com/en-us/office/insert-images-icons-and-more-in-microsoft-365-c7b78cdf-2503-4993-8664-851085c30fce
  - https://support.microsoft.com/en-us/office/graphics-visuals/crop-a-picture-in-office
  - https://support.microsoft.com/en-us/office/graphics-visuals/reduce-the-file-size-of-a-picture-in-microsoft-office
  - https://support.microsoft.com/en-us/powerpoint/reduce-the-file-size-of-your-powerpoint-presentations
  - https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities
  - https://support.google.com/docs/answer/97447
  - https://support.google.com/docs/answer/4600160
  - https://support.google.com/docs/answer/1696521
  - https://github.com/LibreOffice/help/blob/master/source/text/shared/00/00000404.xhp
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/04/01020000.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pictures on slides

**Goal:** sharp, well-aligned images that don't bloat the file.

## Insert
- PowerPoint: Insert › Pictures › This Device, or **Stock Images** (royalty-free library for Microsoft 365
  subscribers: images, icons, cutout people, stickers, illustrations). Or click the picture icon in a
  content placeholder.
- Google Slides: Insert › Image › Upload from computer / Stock & web / Drive & Photos / Camera / By URL.
- Impress: Insert › Image.

## Crop and shape
- PowerPoint: Picture Format › **Crop** (drag the black crop handles); the Crop menu also crops to a shape
  (circle for headshots) or to an aspect ratio.
- Google Slides: select the image › **Crop** and drag the handles; the arrow next to Crop masks the image to
  a shape.

## Arrange
- Google Slides: **Arrange** › Align (two or more objects) / Distribute (three or more) / Center on page;
  colored snap guides appear while dragging.
- Impress: hold `Shift` while dragging to constrain movement horizontally or vertically.
- Full-bleed photo: size it to fill the slide, send it to the back, put text on a semi-transparent shape.

## Size the file
PowerPoint: Picture Format › **Compress Pictures** › clear *Apply only to this picture* to apply to all,
tick *Delete cropped areas of pictures* (cannot be undone), pick a resolution (Microsoft 365 default
220 ppi; lower for email). File › Options › Advanced › *Discard editing data* shrinks it further.

## Gotchas
- Images found by web search aren't automatically free to use; prefer stock libraries, Creative Commons
  with attribution, or your own.
- Add alt text to pictures so screen-reader users get what matters in them; the Accessibility Checker
  finds pictures without it.

## Verify
- [ ] File size is reasonable for how you will share it and images look sharp in Slide Show.

## Checked
2026-10-27, against Microsoft Support (Insert images, icons and more; Crop a picture in Office; Reduce the file size of a picture; Reduce the file size of your presentations; accessibility guide; Microsoft 365 and 2016-2024), Google Docs Editors Help (Insert images; Crop and adjust images; arrange objects) and the LibreOffice help master branch (Insert menu; Impress shortcut keys). Confirmed: Stock Images path and categories, Google image sources, Impress Insert › Image, crop handles, crop to shape/aspect ratio, Google mask-to-shape, Arrange options, Shift-drag in Impress, Compress Pictures options, the 220 ppi default and Discard editing data. Removed unconfirmed Remove Background, Online Pictures, size figures and a "double-click to crop" step.
Method: documentation only; no commands were run.
