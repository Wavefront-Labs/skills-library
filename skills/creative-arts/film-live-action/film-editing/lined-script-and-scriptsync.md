---
id: creative-arts.film-live-action.film-editing.lined-script-and-scriptsync
name: lined-script-and-scriptsync
category: creative-arts
field: film-live-action
product: film-editing
tags: [film-editing, film-live-action, scriptsync, script-based-editing, lined-script-import, lined-script, avid-script-bin, phrasefind, script-integration, take-lines]
level: practitioner
status: draft
description: "Use the script supervisor's lined script and script-based editing (Avid ScriptSync, script bins, Premiere/Resolve equivalents) so every take of every line is one click away."
sources:
  - "https://www.avid.com/media-composer (Avid Media Composer - Script Integration and ScriptSync documentation)"
  - "Pat P. Miller, Script Supervising and Film Continuity (the lined script)"
  - "Norman Hollyn, The Film Editing Room Handbook (lined scripts and script bins)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lined script and ScriptSync

**Goal:** the editor sees, for every line of the script, which set-ups covered it - and
plays any take from that line instantly.

## 1. The lined script (paper/PDF)
The script supervisor draws a **vertical line** per set-up down each script page through
the lines it covers: straight line = on camera, **squiggle** = off camera; labelled at
the top with set-up/slate (24B), takes and lens/ size. Facing pages list each take's
notes (circled, timing, issues). Delivered daily with the editor's report (often as PDF
from apps like ScriptE or Scriptation).

## 2. Avid Script Integration
1. Import the script as text into a **Script bin** (File > New Script).
2. **Link clips to the script**: select a clip, drag/link it to the line range it covers,
   creating coloured coverage lines in the bin - mirrors the lined script.
3. Mark **takes** and set the **preferred (circled) take** - shown in the script bin.
4. Click a line in a coverage line to load that clip **cued to that line**.

## 3. ScriptSync (Avid option)
ScriptSync uses phonetic analysis to **automatically sync each clip's dialogue to the
script lines** - so clicking a line plays that line in every take. Run it on new dailies
(needs the script imported and clips linked to the right scene). Check sync accuracy on
overlapping dialogue and improv; adjust manually. PhraseFind lets you search dialogue
phonetically across all media.

## 4. Other NLEs
- **Premiere Pro**: transcription (Speech to Text) and Text-Based Editing find lines by
  text; not a true script bin, but searchable dialogue.
- **Resolve**: transcription/ text-based editing in recent versions; third-party tools for
  script-based workflows.
- Some teams use spreadsheet logs of lines-to-takes generated from the script supervisor's
  data.

## 5. Assistant workflow
Assistants maintain script bins daily: import revised pages (match script revisions),
link new clips, mark circle takes per the script supervisor's report, flag improvised
material not in the script (add as notes).

## Gotchas
- Script bin built from an old draft; lines don't match revised pages.
- Improv sections not linked; editors miss great material.
- ScriptSync errors left uncorrected on overlapping dialogue.
- Circled takes not marked; editor doesn't know the director's preference.

## Verify
- [ ] Lined script and facing pages received daily.
- [ ] Script bin current with revisions; clips linked and circle takes marked.
- [ ] ScriptSync (or equivalent) run and spot-checked.
- [ ] Improv material noted and findable.
