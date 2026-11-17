---
id: creative-arts.animation.editing.rough-cut-assembly-and-story-reels
name: rough-cut-assembly-and-story-reels
category: creative-arts
field: animation
product: editing
tags: [rough-cut, story-reel, selects, radio-cut, editorial, premiere, avid, resolve, bins, alternates, pitch-reel, dailies, story-before-picture]
level: practitioner
status: draft
description: "Pick the best takes/boards per beat into a loose story reel to prove the story works before locking any timing."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rough Cut Assembly and Story Reels

**Goal: find out whether the story works before anyone spends a frame of final timing
on it.** This is the editorial pass that happens *before* `creative-arts.animation.
editing.animatic-assembly` locks per-shot durations — it is loose, disposable, and its
output is a decision ("this sequence works" / "cut these three beats") rather than a
timed deliverable. Confusing the two wastes real production time: teams that skip the
rough cut and go straight to timed animatic end up re-timing the same sequence three
times because the story problem wasn't caught until boards were already paced.

## The method

1. **Log before you cut.** For every beat/shot, list every take/board/angle you have
   (alternate line reads, alternate staging, alternate gags) in a bin/selects reel, one
   clip per alternate, named `<shot_id>_<alt>` (e.g. `SH040_wide`, `SH040_cu`,
   `SH040_altline`). Do this even for 2D boards — a "take" can just be two different
   drawings of the same beat.
2. **Cut dialogue-first ("radio cut").** Assemble the VO/dialogue track alone, trimmed
   only for pace and overlap, with no picture decision made yet. This is the spine the
   picture gets hung on; cutting picture before the dialogue read is locked means every
   picture decision gets re-litigated when the read changes.
3. **Assemble loosely, in order, picking one alternate per beat.** Use whatever is
   fastest to drag-and-drop (Premiere/Resolve storyboard view, Avid bins set to frame
   view) — do not trim to scripted duration yet. Durations here are "long enough to
   read," not "final." Overlapping cuts and held-too-long holds are fine; the only
   question this pass answers is "does the sequence track."
4. **Watch it straight through, cold.** Problems a rough cut exists to catch: beats
   that don't need to exist, a joke that doesn't land without the missing setup shot,
   geography that doesn't track shot-to-shot, a take that reads funnier/sadder than the
   one the storyboard artist expected. Note timecodes, don't fix in the moment.
5. **Iterate on selection, not on timing.** Swap alternates, reorder, cut whole beats.
   Re-watch. Repeat until the note is "this works" rather than "something's off" — only
   then does the sequence graduate to timed assembly (duration-per-shot locking belongs
   to the animatic-assembly stage, not here).
6. **Hand off a decision, not just a file.** The deliverable is the selects reel *plus*
   a short note per beat: which alternate won and why, which beats got cut, which still
   need a missing shot. Downstream editors re-timing the sequence need the reasoning,
   not just the winning clip, or they'll re-ask the same story question.

## Gotchas

- **Don't trim-to-length in a rough cut.** The moment you start matching durations to a
  script timing column, you've switched tasks to animatic-assembly and will burn time
  re-deciding story after a take changes.
- **Keep every alternate in the bin even after picking one.** A later note ("try the
  wide again") is common; re-digitizing or re-rendering a dropped take costs real time.
- **A story reel for pitching is not a rough cut.** A pitch/sizzle reel is cut *after*
  the story is proven, selectively, for persuasion; a rough cut is cut for the whole
  team to find problems and is allowed to be ugly and too long.
- **Silence is a beat too.** Don't fill gaps with slates or black here (that's the
  animatic's job) — a rough cut can jump-cut straight from one alternate to the next;
  continuity of runtime doesn't matter yet.

## Verify

- [ ] Every alternate take/board for every beat is logged in the bin before assembly
      starts, not discovered mid-cut.
- [ ] Dialogue/VO track was cut and reviewed on its own before any picture was chosen.
- [ ] The rough cut was watched start-to-finish at least once without pausing to fix,
      with notes taken on a second pass.
- [ ] Each beat has one explicit written reason for its winning alternate.
- [ ] No shot in the rough cut has been trimmed to a scripted `dur_s` — if it has, the
      sequence has silently moved into the animatic-assembly stage.

Status: draft — method is standard editorial practice (dailies/selects/radio-cut
workflow used across live-action and animation editorial); not yet cross-checked
against a specific in-house pipeline script the way `animatic-assembly` was. If you
have a concrete tool/shortcut set (Resolve storyboard timeline, Avid ScriptSync) that
should be folded in, note it here rather than opening a competing skill.
