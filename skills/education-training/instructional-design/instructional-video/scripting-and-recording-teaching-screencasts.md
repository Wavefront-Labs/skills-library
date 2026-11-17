---
id: education-training.instructional-design.instructional-video.scripting-and-recording-teaching-screencasts
name: scripting-and-recording-teaching-screencasts
category: education-training
field: instructional-design
product: instructional-video
tags: [instructional-video, educational-video, teaching-video, screencast, screen-recording, lecture-capture, video-lectures, demonstration-video, how-to-video, two-column-script, a-v-script, scripting, storyboard, obs-studio, camtasia, loom, screenpal, panopto, kaltura, microphone, audio-quality, captions, subtitles, wcag, chunking, video-length, engagement, embedded-questions, edpuzzle, h5p-interactive-video, flipped-classroom]
level: practitioner
status: draft
description: "Plan and make teaching videos that hold attention: chunk into short segments, write a two-column A/V script, set up screen and audio, record in takes, caption, and embed questions."
sources:
  - "Guo, P., Kim, J. & Rubin, R. How video production affects student engagement (Learning@Scale 2014)"
  - "Brame, C. J. Effective educational videos. CBE—Life Sciences Education (2016)"
  - "OBS Studio documentation (obsproject.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scripting and recording teaching screencasts

**Goal:** short, clear teaching videos that learners actually finish and learn from —
produced fast enough that you'll make more than one.

## 1. Plan short segments
- One video = one objective. Split a 40-minute lecture into 4–8 segments.
- A widely cited MOOC study (Guo et al., 2014) found median engagement dropped off sharply
  beyond ~6 minutes. Treat **~3–8 minutes** as a target, *with the caveat that this was one
  platform's data and attention depends on motivation and content.*
- Start with **why** it matters (10–20 seconds), not a long title sequence or self-introduction.
- End with a quick recap and what to do next (the practice task).

## 2. Script in two columns
| Audio (what you say) | Visual (what's on screen) |
|---|---|
| "Let's find the error in this formula." | Spreadsheet zoomed on cell D4, cursor on it |
| "Notice the range stops at row 9…" | Highlight box around B2:B9 |
- Write for speaking: short sentences, "you" and "we", one idea per sentence.
- Every line points at something visible (signalling); don't read slide text aloud word-for-word.
- Full script for polished/reused content; bullet-point outline for quick, informal videos —
  informal, enthusiastic delivery often engages better than a stiff read.
- Rehearse once aloud and time it (~130–150 words/minute is a typical pace).

## 3. Set up for clean recording
- **Audio first.** Poor audio loses viewers faster than poor video. Use a USB or headset mic
  10–20 cm from your mouth, a quiet soft-furnished room, and turn off notifications.
- **Screen:** record at 1920×1080; increase app and font zoom (code at 16–20 pt+), hide bookmarks
  bar, desktop icons and personal tabs; close email and chat.
- **Software:** OBS Studio (free) for screen + webcam scenes; Camtasia or ScreenPal for
  record-and-edit; Loom for quick unedited videos; institutional lecture-capture
  (Panopto, Kaltura) where provided.
- Webcam inset optional; small, in a corner that doesn't cover content. A "talking head" can help
  connection but shouldn't sit on top of what learners need to see.

## 4. Record in takes, edit lightly
1. Record one segment at a time. When you stumble, pause 2 seconds and restart the sentence — the
   gap makes it easy to cut.
2. Clap or pause at the start to sync if recording camera and screen separately.
3. Edit: trim dead air and mistakes, add zoom/highlight on key areas, add a simple title card.
4. Export MP4 (H.264, AAC audio), 1080p.

## 5. Make it accessible and active
- **Captions:** auto-generate (YouTube, Panopto, Kaltura, Microsoft Stream all offer it), then
  **correct them** — technical terms and names are frequently wrong. Accurate captions are
  expected under WCAG 2.x AA for prerecorded video.
- Provide a transcript or the script as a download.
- Describe key visuals in narration ("the line rises steeply") for learners who can't see them.
- **Embed questions** using Edpuzzle, H5P Interactive Video, or your LMS/video platform's quiz
  feature, or pair each video with a short practice task.

## Gotchas
- **Over-production trap:** spending days on one video. Good audio + clear structure beats
  animation polish.
- **Dated content:** avoid saying dates, semester names or "last week" — it limits reuse.
- **Software version drift:** screencasts of software UIs go stale when menus change; keep the
  script so you can re-record quickly.
- **Copyright:** music, clips and images need licences; school/fair-use exceptions vary by country.
- **Privacy:** don't record student names, emails or faces without consent.

## Verify
- [ ] Each video teaches one objective in roughly 3–8 minutes and opens with why it matters.
- [ ] A two-column script (or outline) exists and each line ties to a visual.
- [ ] Audio is clear with no notification sounds; text is readable on a phone.
- [ ] Captions were corrected by a human, and a transcript is available.
- [ ] Each video has an embedded question or follow-up task.
