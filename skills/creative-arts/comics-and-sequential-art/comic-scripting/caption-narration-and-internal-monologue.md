---
id: creative-arts.comics-and-sequential-art.comic-scripting.caption-narration-and-internal-monologue
name: caption-narration-and-internal-monologue
category: creative-arts
field: comics-and-sequential-art
product: comic-scripting
tags: [comic-scripting, comic-dialogue, comic-captions-writing, caption-narration, internal-monologue, first-person-captions, omniscient-narrator, thought-captions]
level: practitioner
status: draft
description: "Choose and write comic narration: omniscient vs first-person captions, internal monologue instead of thought balloons, counterpoint to the art, and consistent narrator coding."
sources:
  - https://scottmccloud.com/2-print/1-uc/index.html
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Writing+Comics
  - https://blambot.com/pages/comic-book-grammar-tradition
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Caption narration and internal monologue

**Goal:** captions that add what the picture can't (time, interiority, irony), with a
clear, consistent narrator.

## Pick the narration mode per book
| Mode | Use | Script tag |
|---|---|---|
| None | most action/ensemble books | - |
| Omniscient third person | mythic or literary tone, time jumps | `CAPTION:` |
| First-person (one lead) | noir, character studies | `CAPTION (MARA):` |
| Multiple first-person | ensemble; needs visual coding per narrator | `CAPTION (TEO):` |
| Diary/document | epistolary, flashbacks | `CAPTION (JOURNAL):` |

Modern comics mostly replace thought balloons with first-person captions; thought
balloons survive in comedic or retro styles.

## Writing rules
1. **Don't describe the picture.** "Mara walked into the bar" over a panel of Mara
   walking into the bar wastes space.
2. **Counterpoint**: the caption says one thing, the image another ("I was fine." over
   her shaking hands). This is where captions earn their keep.
3. **Short units**: one or two sentences per caption box; several boxes in a column
   read better than one big block.
4. **Tense**: present for immediacy, past for retrospective narration. Pick one.
5. **Don't let captions and dialogue compete** in the same panel; trim one.

## Coding narrators
Tell the letterer in a note: "Mara's captions: off-white boxes; Teo's: pale blue."
Keep a list in the series bible; colourists and letterers need it.

## Gotchas
- Captions that summarise what happened between panels usually mean a missing panel.
- First-person narrators can't know what happens off-screen; break the rule only
  deliberately.

## Verify
- [ ] One narration mode per sequence; narrator coding listed.
- [ ] No caption only restates the visible image.
- [ ] Caption boxes short and sequential.
