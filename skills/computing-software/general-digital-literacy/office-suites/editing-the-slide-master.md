---
id: computing-software.general-digital-literacy.office-suites.editing-the-slide-master
name: editing-the-slide-master
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slides, slide-master, master-layouts, logo-on-every-slide, footer-slide-number, theme-editor]
level: intro
status: docs-checked
description: "Edit the slide master and its layouts to put a logo, footer, slide numbers and fonts on every slide at once in PowerPoint, Google Slides and Impress."
sources:
  - https://support.microsoft.com/en-us/powerpoint/training/customize-a-slide-master
  - https://support.microsoft.com/en-us/powerpoint/edit-and-re-apply-a-slide-layout
  - https://support.microsoft.com/en-us/powerpoint/insert-or-change-the-slide-numbers-date-or-footer-for-on-screen-slides-in-powerpoint
  - https://support.microsoft.com/en-us/powerpoint/reuse-import-slides-from-another-presentation
  - https://support.google.com/a/users/answer/9282978
  - https://support.google.com/docs/answer/1705254
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/footer.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editing the slide master

**Goal:** change something on every slide (logo, font, footer) in one place.

## Open it
- **PowerPoint (desktop):** View › **Slide Master**. The larger thumbnail at the top is the master; the
  layouts sit beneath it. Slide Master › **Close Master View** when done. PowerPoint for the web has no
  Slide Master view.
- **Google Slides:** View › **Theme builder** (theme colours: Slide › Edit theme). Click **Close** when done.
- **Impress:** View › **Master Slide**; leave with Close Master View or View › Normal.

## Common edits
- **Logo on every slide:** insert the image on the master (top thumbnail); objects on the master show on
  every slide that uses it.
- **Fonts and colours:** select the master title placeholder › change font; layouts follow
  unless they override it.
- **Footer and slide numbers:** PowerPoint Insert › Header & Footer › Slide tab › tick Slide number,
  Footer, *Don't show on title slide* › Apply to All. Move or format them on the master; on a layout,
  the **Footers** check box on the Slide Master tab shows or hides them. Impress: Insert › Header and Footer.
- **Custom layout:** Slide Master › **Insert Placeholder** › pick a type and draw it; right-click the layout ›
  **Rename Layout**. Then on normal slides use Home › Layout to re-apply the edited layout.

## Gotchas
- Items added on normal slides are not on the master; people often paste a logo on each slide and
  then can't update them. Delete those and use the master.
- Reusing slides with *Keep source formatting* brings the other deck's design along; leave it unticked
  to adopt this deck's look.

## Verify
- [ ] A new slide added after the change shows the logo/footer automatically.

## Checked
2026-10-27, against Microsoft Support (PowerPoint for Microsoft 365 and 2016-2024: Customize a slide master; Edit and re-apply a slide layout; slide numbers and footers; Reuse slides), the Google Workspace presentation tips and Slides theme help, and the LibreOffice help master branch (Impress footer guide). Confirmed: View › Slide Master and Close Master View, master-on-top layout order, no Slide Master in PowerPoint for the web, Insert Placeholder and Rename Layout, the Footers check box, the Header & Footer dialog options, Google Theme builder and Slide › Edit theme, Impress View › Master Slide and Insert › Header and Footer. Removed an unconfirmed "Hide Background Graphics" step.
Method: documentation only; no commands were run.
