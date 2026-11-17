---
id: humanities.heritage-interpretation.digital-and-audio-interpretation.scripting-audio-guides-and-heritage-apps
name: scripting-audio-guides-and-heritage-apps
category: humanities
field: heritage-interpretation
product: digital-and-audio-interpretation
tags: [digital-and-audio-interpretation, heritage-interpretation, audio-guide, audio-tour, audio-script, writing-for-the-ear, heritage-app, museum-app, mobile-guide, gps-trail, geofencing, qr-codes, bluetooth-beacons, ar-reconstruction, augmented-reality, virtual-tour, 360-tour, photogrammetry, digital-reconstruction, london-charter, seville-principles, wcag, transcripts, audio-description, offline-mode]
level: practitioner
status: draft
description: "Script and specify audio guides, heritage apps, AR reconstructions and virtual tours: write for the ear, pace stops, keep reconstructions honest, and plan access, offline use and upkeep."
sources:
  - "The London Charter for the Computer-based Visualisation of Cultural Heritage (2.1, 2009)"
  - "Principles of Seville: International Principles of Virtual Archaeology (2011)"
  - "W3C Web Content Accessibility Guidelines (WCAG) 2.2"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scripting audio guides and heritage apps

**Goal:** deliver heritage interpretation through a device — audio guide, app, AR overlay or
virtual tour — that people actually finish, that is honest about what's known, and that
still works in a stone building with no signal.

## 1. Decide whether a device is the right medium
Digital is good for **layers** (depth on demand), **languages**, **reconstruction** (what's
gone), **sound** (voices, music, ambience) and **off-site** access. It's poor when visitors
should look at each other or the place, when signal/battery fail, or when nobody will
maintain it. Tie it to the site interpretation plan
(`humanities.heritage-interpretation.interpretive-planning.writing-a-site-interpretation-plan`).

## 2. Writing for the ear (audio guides)
- **Stop length**: commonly 1–2 minutes per stop; ~130–150 spoken words per minute.
  Offer optional "more" tracks for depth.
- **Tell people where to look first**: "Stand by the window and look at the left-hand
  corner of the fireplace." Then the story.
- **Short sentences, one idea each**; repeat key names; avoid lists of dates.
- **Voices**: a narrator plus real voices (curator, community member, oral-history clip,
  actor reading a letter) gives variety. Clear permissions for every clip.
- **Sound design**: subtle ambience is effective; don't drown speech; test on cheap
  earphones and phone speakers.
- **Read the script aloud on site** with a stopwatch before recording.
- Number stops to match **physical markers**; include orientation and directions between
  stops.

## 3. Apps and triggers
- Trigger content by **stop number, QR code, GPS geofence or Bluetooth beacon**. GPS is
  unreliable indoors and between tall walls; beacons need batteries and maintenance; QR and
  numbers are robust.
- **Offline first**: let visitors download before arriving; assume poor signal in historic
  buildings and rural sites. Keep download size small.
- Provide **on-site Wi-Fi or loan devices** if the guide is core to the visit.
- Budget for **OS updates**: apps break as phone platforms change. A mobile website can
  outlive a native app.

## 4. AR and virtual reconstructions — keep them honest
The **London Charter** and **Seville Principles** ask that visualisations document their
sources and distinguish evidence from conjecture.
- Keep a **paradata** record: for each element, the evidence (excavation, drawings,
  analogies) and level of certainty.
- Show uncertainty visibly (e.g. greyed or simplified forms for conjectural parts,
  alternatives, "what we know / what we think" toggle).
- Get specialist review before release; reconstructions are treated as fact by visitors.
- Virtual tours (360° photography, photogrammetry) need good capture in even light;
  plan for accessibility (keyboard navigation, text alternatives).

## 5. Accessibility
- **Transcripts** for every audio track; **captions** for video; **audio description** for
  visual content; adjustable text size; compatibility with screen readers. Use **WCAG 2.2
  AA** as the baseline for apps and web.
- Physical access to triggers (QR codes at reachable heights).
- Languages: translate and record natively, don't machine-translate without review.

## 6. Maintenance plan
Decide before launch: who updates content, how often hardware (loan devices, beacons) is
checked, how bugs are reported, how analytics (stops played, completion rate) feed
revisions, and when the product will be retired.

## Gotchas
- **Talking heads at length**; interviews must be edited hard.
- **Directions that no longer match the route** after a room closes.
- **Rights**: music, images and archive audio need licences that cover the app's life and
  territory.
- Visitors with headphones don't talk to each other — offer shared-listening options for groups.

## Verify
- [ ] Each audio stop starts with where to look and runs ~1–2 minutes when read aloud.
- [ ] The guide works offline and indoors; triggers were tested on site.
- [ ] AR/virtual reconstructions have paradata and visibly mark conjecture.
- [ ] Transcripts, captions and WCAG 2.2 AA checks are done.
- [ ] Rights are cleared for every asset; a maintenance owner and budget exist.
