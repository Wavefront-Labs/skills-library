---
id: creative-arts.graphic-design.adobe-indesign.cc-libraries-for-brand-assets
name: cc-libraries-for-brand-assets
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, cc-libraries, creative-cloud-libraries, brand-colours, shared-library, indesign-snippets, character-styles, paragraph-styles, brand-assets]
level: practitioner
status: draft
description: "Share brand colours, styles, logos and snippets across InDesign, Illustrator and Photoshop with Creative Cloud Libraries: add, link, update and permission a team library."
sources:
  - https://helpx.adobe.com/indesign/using/creative-cloud-libraries-sync-share-assets.html
  - https://helpx.adobe.com/creative-cloud/help/libraries.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CC Libraries for shared brand colour and assets

**Goal:** one source of brand colours, type styles, logos and layout snippets used by every designer
and app, so updates reach everyone.

## Build the library
- Window > **CC Libraries**, Create New Library (name it by brand and version, e.g. `Acme Brand 2026`).
- Add from InDesign: select objects or text and click **+** to add colours (fill and stroke), paragraph and
  character styles, graphics and text (as snippets). From Illustrator: colours, colour themes, character
  styles, graphics. From Photoshop: layer styles, colours, graphics.
- Organise with **Groups** (Logos, Colours, Type, Templates) and give assets clear names.

## Use
- Colour: click to apply; right-click > **Add to Swatches** to make it a document swatch.
- Styles: click to apply; it is added to the document's style list.
- Graphics: drag to place. Placed library graphics are **linked** (cloud link shown in the Links panel);
  when the library asset changes, the link shows as modified and updates.
- Alt/Option-drag places an unlinked copy.

## Share
- Panel menu > **Share** (invite collaborators with edit or view permissions) or share a public link
  (view-only). Brand teams keep edit rights; agencies get view or follow.
- Libraries can be followed (read-only) so central brand updates reach partners.

## Gotchas
- Library colours carry their colour mode; a brand RGB colour added from Photoshop is RGB in InDesign.
  Store CMYK and spot versions explicitly and name them (`Acme Red PMS 485`, `Acme Red CMYK`).
- Libraries need Creative Cloud sign-in and sync; offline or outside-agency workflows still need
  packaged files.
- Deleting a library asset breaks links in documents (they keep their last cached version).

## Verify
- [ ] A second designer can apply the same colours and styles from the shared library.
- [ ] Editing a library logo marks placed instances as modified in the Links panel.
