---
id: creative-arts.animation.blender.text-boxes
name: text-boxes
category: creative-arts
field: animation
product: blender
tags: [blender, text-object, text-boxes, text-box, text-overflow, word-wrap, layout]
level: practitioner
status: docs-checked
description: "Wrap and flow Blender text with text boxes: Size X/Y, Offset X/Y, multiple frames for columns, Overflow modes (Overflow, Scale to Fit, Truncate) and Justify/Flush alignment."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/texts/properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# text-boxes

Goal: paragraphs that wrap inside a frame, flow across columns and stay inside a sign or screen.

## Properties > Data > Text Boxes

- Text boxes (frames) distribute the text among rectangular areas within one text object. Any number of frames is allowed.
- **Add Textbox** inserts a new frame just after the current one in text flow order, with the same size and position as the selected one. The remove button deletes the current frame.
- **Size X, Y**: width and height of the frame. If set to zero no word wrapping happens; if all frames have a null size the whole text box system is disabled.
- **Offset X, Y**: position of the frame.
- Text flows continuously from the lowest-numbered frame to the highest, word-wrapped inside each, and moves to the next frame when a frame cannot fit more text.

## Overflow (what happens past the last frame)

- **Overflow**: text keeps running out of the last box.
- **Scale to Fit**: scales the text to fit the available space.
- **Truncate**: hides the end of the text that does not fit. It only truncates in Object Mode; in Edit Mode the whole text stays visible.

## Alignment with frames (Paragraph panel)

- Horizontal Left, Center and Right align to the frames when frames are used; **Justify** flushes a line only when it ends at a word wrap and uses whitespace to fill; **Flush** always flushes and uses character spacing. Justify and Flush only work within frames.
- Vertical alignment (Top, Top Baseline, Middle, Bottom Baseline, Bottom) refers to the frames when they exist, otherwise to the object origin.
- Paragraph Offset X/Y applies to each frame when frames are used.

## Recipes

- Two columns: two frames side by side with the same Size, Justify alignment.
- Fixed-area sign: one frame sized to the sign, Overflow set to Scale to Fit, Center and Middle alignment.
- Driven text: set the text body from a script or driver; Scale to Fit keeps it inside the frame.

## Gotchas

- Truncate has no visible effect while editing the text.
- Text objects are limited to 50,000 characters, and large text slows interaction.

## Verify

Type extra text in Edit mode: it flows into the next frame, or scales or overflows per the chosen mode (Truncate shows its result in Object Mode).

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Text Properties: Text Boxes and Paragraph; Text introduction). Confirmed: Add Textbox behaviour, Size X/Y zero rule, Offset, flow order, the three Overflow modes and the Object-Mode-only Truncate note, Justify/Flush within frames, 50,000 character limit. Removed as unconfirmed: dashed-rectangle display, long-word wrapping behaviour, numeric recipe values, advice to use Scale to Fit/Truncate only with a single box, and text-unit coordinate claim.
Method: documentation only; no commands were run.
