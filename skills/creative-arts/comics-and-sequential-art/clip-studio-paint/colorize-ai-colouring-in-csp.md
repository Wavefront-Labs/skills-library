---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.colorize-ai-colouring-in-csp
name: colorize-ai-colouring-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-colouring, csp-colorize, ai-colouring, hint-layer, flatting, technology-preview]
level: practitioner
status: draft
description: "Use Clip Studio Paint's Colorize feature: line art reference and hint layers, colorize all vs with hints, cleaning and flatting the result, and disclosure considerations."
sources:
  - https://tips.clip-studio.com/en-us
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Colorize (AI colouring)

**Edit > Colorize** (introduced as a technology preview) uses machine learning to colour line art
automatically.

## Modes
- **Colorize all** - colours the line art with no guidance; results are a rough base.
- **Colorize using hint image** - you paint rough colour hints on a separate layer; CSP uses them to
  colour each region.

## Workflow
1. Line art on its own layer; set it as the **reference layer** (lighthouse icon in Layer palette).
2. Create a new layer and set it as the **hint** layer (Colorize hint layer option, Layer > Layer
   settings or the layer palette depending on version). Scribble colours inside each region.
3. Edit > Colorize > Colorize using hint image. A new colour layer is created.
4. Clean up: the output is soft and bleeds over lines. Use it as a rough colour guide; re-flat with the
   Fill tool (refer other layers) and pick colours from the result.

## Where it helps
- Quick colour comps for many pages, idea testing, shadow base.
- Not a replacement for clean flats in professional pages.

## Disclosure and policy
- Some publishers and contests require disclosure of AI-assisted art or forbid it; check before using.

## Gotchas
- Processing very large canvases can take time and memory.
- Hints that touch lines cross into neighbouring regions; keep hints inside shapes.

## Verify
- [ ] Final flats are clean, closed fills; any AI use disclosed where required.
