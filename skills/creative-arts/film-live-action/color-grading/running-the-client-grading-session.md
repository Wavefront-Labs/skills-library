---
id: creative-arts.film-live-action.color-grading.running-the-client-grading-session
name: running-the-client-grading-session
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, colour-grading, film-live-action, colorist, colourist, client-session, grading-session, client-review, supervised-session, unsupervised-session, attended-session, remote-session, remote-grading, streambox, clearview, sohonet, frame-io, review-and-approve, grade-prep, look-book, reference-stills, gallery-stills, versions, local-versions, remote-versions, still-store, wipe, split-screen, session-notes, grade-notes, dp-session, director-session, time-management, bidding-grade-days, grading-schedule, first-pass, second-pass, calibration-check, viewing-environment, dim-surround, grading-suite, suite-calibration, viewing-conditions, session-prep, pre-grade, prep-stills, translating-notes, client-communication-grade, colour-language, remote-session-tools, streambox-use, clearview-use, grade-estimation, grade-days, grading-schedule-plan, review-rounds, grade-approval, approval-process, dp-in-suite, director-in-suite]
level: practitioner
status: draft
description: "Run a supervised grade: prep before the client arrives, structure the days (look day, first pass, review, polish), notes that become grades, versions and stills, remote sessions, sign-off."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (The Colorist Guide to DaVinci Resolve - session workflow chapters)"
  - "https://theasc.com/ (ASC articles on DP/colourist collaboration)"
  - "https://www.sohonet.com/clearview/ (ClearView remote review) and https://frame.io/ (review-and-approve)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running the client grading session

**Goal:** the client leaves every day having seen their film get better, you leave with
clear notes and no wasted hours, and the final grade is signed off on time because
the sessions were structured instead of improvised.

## 1. Before anyone arrives
- Conform checked against the offline; VFX status known; missing shots slugged.
- **Pre-grade**: balance pass on every shot (node 1), shot-matched within scenes, show
  LUT/LMT applied, scenes grouped (Resolve Groups / Baselight scene detection). Clients
  should never watch you fix exposure.
- **Reference material**: the DP's lookbook, approved dailies stills, the test-day
  frames, any references from the director - loaded in the Gallery/still store, labelled.
- Calibrate the monitor (probe) that morning; set the room to the viewing condition
  (dim surround, 5-10 nits, no coloured walls or reflections); client monitor matched
  to the reference.
- Timeline markers per scene; a **session agenda** (which reels today) sent the day before.

## 2. Structure the days
Typical feature: 8-15 days. A workable plan:
1. **Day 1 - look day**: with the DP (and director), establish the look on 5-10 hero
   shots across the film's key scenes. Decide contrast, colour palette, skin, how night
   looks, how flashbacks differ. Save stills and build the LMT/group grades.
2. **First pass**: scene by scene, play through at speed before touching; set the scene
   from the hero shot, propagate, then watch the scene again. Don't polish yet.
3. **Review reel by reel** with the director/DP: notes with timecodes; address in order
   of importance (story beats first).
4. **Polish pass**: secondaries, windows, tracking, power windows on faces, beauty.
5. **Deliverable passes**: HDR/SDR trims, DCP check, QC.
Keep 10-15% of the time unallocated: notes always come late.

## 3. In the room
- Play, don't scrub. Clients judge motion pictures; you judge stills. Watch a scene at
  speed before and after.
- Ask for **feelings, not values**: "colder? more contrast? too pretty?" -> you turn it
  into a grade. When a client says a number ("add 10% magenta") show them two versions
  and ask which they *feel*; it is usually neither.
- **Wipe/split** against the previous shot and against the reference still; use
  **versions** (Local/Remote in Resolve) to A/B two candidates quickly (`Ctrl/Cmd+Y` /
  version menu) rather than undo.
- One voice: agree at the start who signs off (usually the director with the DP's
  stewardship). When DP and director disagree, make both versions, play them in
  sequence, and let the director decide; record it.
- Producers/agency: give them the *why* in one sentence; pick battles on story shots.
- Fatigue: eyes drift warm/dark after hours. Fifteen-minute breaks every two hours;
  re-check the look against the day-1 stills before the end of each day.

## 4. Notes that become grades
Timecode | shot | what they said | what it means | done?
"Her face is lost" = lift the key window; "too video" = soften highlight roll-off,
desaturate highlights, add grain; "the greens are wrong" = Hue vs Hue on foliage,
check IDT. Read the notes back before the client leaves to confirm.

## 5. Remote and unsupervised
- **Remote supervised**: calibrated stream (Streambox, Sohonet ClearView Flex,
  Moxion/Frame.io live) to a client monitor you've verified (send a calibration clip
  and known stills first); accept that their display is the ceiling of what they can
  judge. Prefer a short in-person look day, remote for the rest.
- **Unsupervised**: grade to the brief, send review-and-approve links (Frame.io, Moxion)
  with stills per scene and 2-3 options on contested looks; collect timecoded comments;
  present a change list. Final approval on a calibrated monitor somewhere.

## 6. Sign-off
Play the whole film once, uninterrupted, on the deliverable transform; a written
approval (email) per reel/version; export approval stills; note the project version
(`v07_APPROVED`) and lock it. Changes after sign-off are a new version and a cost
conversation.

## Gotchas
- Letting the client watch the balance pass; two days gone and "nothing happened".
- Grading to the client's laptop in a bright room, not the reference.
- Undo as versioning; losing the look from before lunch.
- Thirty minutes on a 12-frame insert while the climax is untouched.
- No written sign-off; a producer "remembers it warmer" at the DCP check.

## Verify
- [ ] Pre-graded, matched, referenced and calibrated before the session.
- [ ] Day plan with look day, first pass, review, polish and buffer.
- [ ] Notes captured with timecodes and read back; versions saved for every A/B.
- [ ] Final playthrough and written sign-off per reel; approved version locked.
