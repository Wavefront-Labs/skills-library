---
id: creative-arts.photography-fine-art.adobe-lightroom.generative-remove
name: generative-remove
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, generative-remove, lightroom-transform, firefly, content-credentials, lightroom-classic]
level: practitioner
status: draft
description: "Remove large distractions in Lightroom Classic with Firefly-powered Generative Remove: painting, variations, detection, credits, disclosure and when to avoid it."
sources: ["https://helpx.adobe.com/lightroom-classic/help/remove-tool.html", "https://helpx.adobe.com/lightroom/web/edit-photos/manage-ai-edits.html", "https://contentauthenticity.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generative Remove

Generative Remove (Remove tool `Q` > tick **Use Generative AI**) sends the painted area and surrounding context to Adobe Firefly, which generates a fill. It handles large objects (people, cars, signs) where content-aware Remove smears.

## Steps
1. Remove tool, tick Use Generative AI. Optional: **Detect objects** to have Lightroom find the object you brush loosely.
2. Paint generously over the object **and its shadow/reflection**.
3. Lightroom returns three variations; cycle with the arrows and pick one. Click Refresh for new variations.
4. Requires an internet connection and uses Firefly generative credits per generation.

## Craft and ethics
- Fine-art and documentary contexts differ: competitions, journalism and many open calls forbid generative content. The edit is recorded; smart collection rule Develop > Has AI finds them.
- Exports may carry Content Credentials (C2PA) noting AI use when enabled.
- Keep a virtual copy without generative fills for submissions that require it.

## Quality checks
- Generated texture can look soft or have a different grain: add matching Grain locally or match noise with Effects.
- Check repeated or nonsensical structures (fake windows, text-like shapes) at 100%.
- Resolution: fills are generated at a limited resolution and upsampled; very large prints may show softness in the fill.

## Gotchas
- Generative fills are stored with the edit; syncing them to other photos is not possible.
- Applying Denoise after Generative Remove may require redoing it; Denoise first.

## Verify
- [ ] At print size (or 100%), the filled area matches surrounding grain and detail; disclosure noted in the file's record if required.
