---
id: creative-arts.animation.storyboarding.storyboard-revisions-and-director-notes
name: storyboard-revisions-and-director-notes
category: creative-arts
field: animation
product: storyboarding
tags: [animation, storyboarding, director-notes, notes-session, revisions, note-triage, dailies, feedback, version-control-for-art, approval-workflow, story-artist, spotting-session]
level: practitioner
status: draft
description: "Run a director notes pass without losing reasoning: capture, triage, version, and close out notes on a board."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SKILL: Storyboard revisions and director notes

This skill is about the **notes session itself** — how to run it, capture it, triage
it, and prove it got addressed. `creative-arts.animation.storyboarding.storyboarding`
already states the baseline rule ("version sequences, carry the note on the panel");
this skill is the deeper mechanics of the note-taking meeting, the ambiguous-note
problem, and the close-out loop, which is its own skill because a badly run notes
session loses more board time than bad drawing does. A board artist can draw well and
still burn days by mishearing, misfiling, or silently dropping notes.

## Running the session
- **One person drives the capture, even if the director is talking fast.** Either the
  artist takes notes live while the director watches the board/boardomatic play, or a
  second person (an assistant, coordinator, or the artist themselves pausing playback)
  writes verbatim-as-possible notes. Do not rely on memory after the session — notes
  get rewritten in your head to match what you *wanted* to hear.
- **Play the boardomatic, not static panels, for a revisions pass once one exists.**
  Notes given against a static board and notes given against the timed reel are
  different notes; a panel that reads fine held for 4 seconds can read wrong at the
  reel's real 1-second hold. Re-confirm notes taken on panels once the reel exists.
- **Repeat the note back in your own words before the director moves on.** This is the
  single highest-leverage habit in this skill: "so you want her to notice the door
  *before* she speaks, not after" costs five seconds and catches the majority of
  misreadings before they cost a redraw.

## Triage: not every note is the same kind of note
Sort notes as they land, because they get fixed differently:
- **Staging/geography notes** ("crossed the line," "can't tell who's talking") — fix at
  thumbnail, never patch in clean art. If several clean panels are affected, drop back
  to the thumbnail pass for that stretch (see
  `creative-arts.animation.storyboarding.thumbnail-to-storyboard-workflow`).
- **Acting notes** ("too happy," "she should hesitate here") — usually a single-panel
  redraw; rarely cascades.
- **Timing notes** ("this holds too long," "cut in sooner") — these are boardomatic
  notes, not panel notes. Don't redraw a panel to fix a timing note; retime the reel
  first and only redraw if the retimed hold exposes a genuinely bad drawing.
- **Taste/preference notes** ("I just don't like this shot") — the dangerous kind.
  Ask one follow-up question ("is it the angle, the size, or the acting?") before
  guessing, because a vague note redrawn on a guess often comes back with the same
  complaint, now against a second wasted version.

## The ambiguous-note problem
Directors talk in intent, not panel language ("make it feel more desperate," "this
needs more oomph"). The artist's job is to translate that into a concrete staging
change, and the translation is where notes sessions go wrong:
- **Don't silently interpret a vague note into a big change.** Float your read back:
  "desperate — I'm thinking tighter on her face and losing the wide, that work?" A
  wrong guess costs a full redraw; a thirty-second check doesn't.
- **Watch for notes that contradict an earlier note.** If a new note undoes a decision
  from two sessions ago, say so out loud rather than quietly re-reversing it — it may be
  intentional (the scene changed) or it may be the director forgetting the earlier
  call, and only asking resolves which.
- **A note given on panel 4 sometimes means panel 2 is the actual problem** (an earlier
  staging choice is why panel 4 doesn't work). Notice when a note's real fix is
  upstream of where it was given, and say so rather than patching the named panel only.

## Logging and closing out notes
- **One note log per session, dated, one line per note**, each tagged to a shot/panel
  number and a status (open / addressed / deferred / rejected-with-reason). This is
  the artifact that proves a note was handled — "didn't we already fix this?" is
  answered by the log, not by memory.
- **Carry unresolved notes forward explicitly.** A note deferred ("fix in the next
  pass, not blocking today's lock") must still appear in the next session's log as
  open, or it quietly disappears.
- **Close the loop by showing the fix, not just claiming it.** Re-present the specific
  panel or boardomatic cut that addresses each note at the top of the next review,
  before moving to new material — this is also how a director catches a
  misinterpreted note early instead of three sessions later.

## Gotchas
- **Rejecting a note without saying why, out loud, in the room.** If a note genuinely
  breaks continuity or the budget, say so in the session; a silently-ignored note
  resurfaces as "I told you about this already" with no record to check.
- **Too many open alternates at once.** If a beat has survived three note passes still
  undecided, that's a sign the beat itself (or the script underneath it) is the
  problem, not the drawing — escalate rather than keep iterating panels.
- **Mixing note types in one redraw pass.** Fixing a staging note and a taste note on
  the same panel in the same pass makes it hard to tell which change actually answered
  which note if the director has a follow-up.

**Unconfirmed**: specific note-logging tools (spreadsheet vs. frame.io-style
timestamped comments vs. a production-tracking board) vary by studio and aren't
verified here as a single standard — use whatever the show's pipeline already runs
for dailies, and keep the one-line-per-note discipline regardless of the tool.

## Verify
- [ ] Every note from the session is in the log, dated, tagged to a shot/panel, with a
      status.
- [ ] Every staging/geography note went back through the thumbnail pass, not a direct
      clean-art patch.
- [ ] Every ambiguous/taste note was checked back with the director before a redraw
      was attempted.
- [ ] The next session opens by showing the specific fix for each prior open note.
- [ ] No note sits "open" for more than one session without an explicit reason logged
      (deferred, rejected, or blocked on something upstream).
- [ ] The sequence version number advanced (`seq_vNN` → `seq_vNN+1`) and the note log
      references which version addressed which note.
