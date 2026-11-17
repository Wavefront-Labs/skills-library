---
id: sports-recreation.coaching-officiating-and-sports-administration.performance-analysis.video-code-window-tagging-and-kpi-feedback
name: video-code-window-tagging-and-kpi-feedback
category: sports-recreation
field: coaching-officiating-and-sports-administration
product: performance-analysis
tags: [performance-analysis, video-analysis, notational-analysis, code-window, tagging, coding, sportscode, hudl, nacsport, longomatch, dartfish, catapult, kpi, key-performance-indicators, operational-definitions, inter-rater-reliability, live-coding, post-match-analysis, opposition-analysis, scouting-report, clips, playlist, feedback-session, data-visualisation, analyst, match-analysis]
level: practitioner
status: draft
description: "Building a video-analysis code window around a few coach-agreed KPIs, tagging matches live or post-event in tools like Sportscode or Nacsport, and presenting short clip-based feedback."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Video code window, tagging and KPI feedback

**Goal:** turn match video into a few reliable numbers and the right clips, delivered
to coaches and players fast enough and briefly enough to change the next session.

> Draft: workflow common to most analysis tools (Hudl Sportscode, Nacsport,
> LongoMatch, Dartfish and similar). Menus and terms differ by product; the method
> doesn't.

## 1. Agree the KPIs with the coach first
- Start from the **game model / coaching objectives**: what does the coach want more
  or less of? E.g. "regains within 5 s of losing the ball", "entries into the 22",
  "shots from inside the box".
- Keep it to **3–6 KPIs** per phase. Fifty stats nobody uses is the classic failure.
- Write **operational definitions**: exactly what counts. "Regain = our team gains
  controlled possession (two consecutive touches or a pass) within 5 s of losing it."

## 2. Build the code window
- **Event buttons** (instances with lead/lag time: e.g. 5 s before, 3 s after) for
  each KPI event: *Turnover*, *Regain*, *Shot*, *Entry*.
- **Labels/descriptors** for detail: zone, player, outcome (success/fail), phase.
- Use **exclusive** buttons for things that can't overlap (possession team A/B) and
  linking/activation rules so a label applies to the right instance.
- Keep the layout matching the **pitch** (zones arranged spatially) — faster and
  fewer errors when coding live.
- Test the window on a past match before match day.

## 3. Tagging
- **Live**: code the essentials only (possession, key events) — enough for half-time
  clips. Synchronise with the camera feed.
- **Post-match**: add detail labels; review uncertain tags.
- **Reliability**: periodically have two analysts code the same segment and compare
  (inter-rater reliability). Disagreements mean the definition needs tightening.

## 4. Outputs
- **Matrix/table** of KPIs per half and per match, vs targets and vs season average.
- **Playlists**: 6–10 clips per topic, good and bad examples, trimmed tight, annotated
  (arrows/spotlights) only where it adds clarity.
- **Opposition report**: patterns in their build-up, set-pieces, key players — 1–2
  pages and a short video, not a dossier.

## 5. Feedback sessions
- Team meeting: **≤10–15 minutes**, 2–3 themes, coach-led with the analyst driving.
- Individual: player-specific playlists sent to their phone/app with a question
  ("What were your options here?").
- Close the loop: coaches pick training themes from the KPIs; analysts measure whether
  they change over the next matches.

## Gotchas
- Camera angle: a high, wide, tactical view is far more useful than broadcast close-ups.
- Small samples: a KPI swing over one match is often noise; look at trends.
- Data without context (score state, opponent quality, red cards) misleads.
- Consent and storage: player video and data are personal data — follow club policy
  and local law.

## Verify
- [ ] KPI list signed off by the coach with written definitions.
- [ ] Code window tested; live code produces half-time clips within minutes.
- [ ] Reliability check done this season; definitions updated if needed.
- [ ] Feedback session under 15 min with ≤3 themes, and the KPIs tracked over time.
