---
id: creative-arts.graphic-design.adobe-indesign.threading-and-autoflow
name: threading-and-autoflow
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-text-frames, text-threading, autoflow, smart-text-reflow, overset-text, primary-text-frame, loaded-cursor, threaded-frames]
level: practitioner
status: draft
description: "Flow long text through InDesign frames and pages: manual threading, semi-autoflow, autoflow with Shift, Smart Text Reflow adding pages, and finding overset text."
sources:
  - https://helpx.adobe.com/indesign/using/threading-text.html
  - https://helpx.adobe.com/indesign/using/text-frames.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threading and autoflow

**Goal:** a 200-page manuscript placed and flowing through the right frames in a minute,
with pages added and removed automatically as the text changes.

## Place with a loaded cursor (Ctrl/Cmd+D)
After choosing the file the cursor is "loaded". Then:
| Action | Result |
|---|---|
| Click | Manual: fills one frame, stops; click the out-port to reload |
| **Alt/Option+click** | Semi-autoflow: fills a frame and stays loaded for the next |
| **Shift+click** | **Autoflow**: adds pages and frames until all text is placed |
| Shift+Alt/Option+click | Fixed-page autoflow: fills existing pages only, no new pages |
Clicking inside an existing empty frame flows into it; clicking on empty page creates a
frame within the column.

## Threading by hand
- Click the **out-port** (bottom right of a frame) then click another frame to link.
- View > Extras > Show Text Threads (Alt+Ctrl+Y / Opt+Cmd+Y) shows the links.
- Unthread: double-click an in/out port. Deleting a frame in a thread keeps the text
  (it moves to the next frame or becomes overset).

## Smart Text Reflow (Preferences > Type)
On with **Primary Text Frame** set on the parent: typing or reimporting adds or removes pages
at the end of the story/section/document. Options: Add Pages To, Limit to Primary Text
Frames, Preserve Facing-Page Spreads, Delete Empty Pages.

## Overset text
- Red **+** in the out-port = text that does not fit. Preflight panel lists every overset story.
- Edit > Edit in Story Editor (Ctrl/Cmd+Y) shows overset text below a line.
- Never ship with overset text: the printer will not see it, and neither will the reader.

## Gotchas
- Autoflow uses the parent page's margins/columns; set those first.
- Text frames with different column counts in one thread are fine, but frame-level
  baseline grid settings can differ - check Text Frame Options.
- Placing with "Show Import Options" lets you map Word styles (see Word import skill).

## Verify
- [ ] No overset text in Preflight.
- [ ] Show Text Threads confirms the intended reading order.
- [ ] Adding a paragraph near the end adds a page (if Smart Text Reflow is in use).
