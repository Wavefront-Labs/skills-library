---
id: languages-linguistics.transcription-and-captioning.realtime-captioning.preparing-and-delivering-a-cart-session
name: preparing-and-delivering-a-cart-session
category: languages-linguistics
field: transcription-and-captioning
product: realtime-captioning
tags: [realtime-captioning, cart, communication-access-realtime-translation, live-captioning, captioner, stenocaptioner, job-dictionary, prep, speaker-ids, streamtext, 1cap, zoom-captions, caption-api, latency, accuracy, on-the-fly-correction, untranslates, live-events, classroom-captioning, accessibility, deaf, hard-of-hearing, ada, remote-cart]
level: practitioner
status: draft
description: "Deliver live CART captioning: pre-event prep and job dictionaries, tech setup (StreamText, Zoom API tokens), speaker IDs, accuracy and correction strategies live, and post-session transcript."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Preparing and delivering a CART session

**Goal:** provide accurate, low-latency live captions for a Deaf or hard-of-hearing
consumer (classroom, meeting, conference), whatever input method you use (stenotype,
respeaking or high-speed typing — see those skills for technique).

> Draft. Platform details (Zoom, StreamText, Teams) change often — confirm current menus
> and API behaviour before each event. Not legal advice on accessibility obligations.

## 1. Before the session (prep is half the accuracy)
1. **Collect materials** 48+ hours before: agenda, slides, speaker list, reading lists,
   previous recordings, glossaries. Ask specifically for names and acronyms.
2. **Build a job dictionary** (stenographers) or **custom vocabulary/macros**
   (respeakers): every speaker name, organisation, product, acronym, technical term.
   Test-write each entry once.
3. **Speaker IDs:** set up quick strokes/macros for each speaker (`>>DR. PATEL:`) and a
   generic `>>SPEAKER:` / `>>AUDIENCE MEMBER:` fallback.
4. **Consumer preferences:** where they'll watch (own device, big screen, Zoom panel), font
   size, colour contrast, whether they want a transcript afterward, and confidentiality
   requirements.

## 2. Tech setup
- **Audio is everything.** Get a direct feed (mixer output, Zoom audio, a dedicated mic
  near the speaker) rather than a room mic; test with headphones.
- **Output path:**
  - Browser-based streaming (e.g. StreamText, 1CapApp) — consumer opens a link, can
    change font and colours.
  - **Zoom:** host enables captions and gives you the captioner role or copies the **API
    token** (third-party caption URL) into your software. Teams/Webex have their own
    CART integrations.
  - In-room display: second monitor or projector at readable size.
- **Backup:** second internet connection (phone hotspot), saved local file, laptop power.
- **Test 15–30 minutes early** with the consumer: can they see it, is latency acceptable?

## 3. During the session
- **Prioritise meaning and flow over perfection.** Live, accuracy commonly targeted at
  very high levels (quality benchmarks often cite 98–99%+ for professional CART), but a
  late perfect sentence is worse than a timely good one.
- **Fix what matters:** names, numbers, negations ("can" vs "can't"), key terms — correct
  these on the fly. Let trivial typos go.
- **Untranslates/misrecognitions:** if a word comes out garbled, fingerspell-style or
  type it, or use a dash and move on; add it to the dictionary at the next pause.
- **Speaker changes:** always mark them — a new line with `>>`.
- **Non-speech information** in brackets: `[APPLAUSE]`, `[LAUGHTER]`, `[INAUDIBLE]`,
  `[VIDEO PLAYING — NO CAPTIONS]`.
- **Overlapping speech:** caption the main floor; mark crosstalk.
- **Pace:** if speech outruns you, condense minimally — keep content words, drop fillers;
  never invent.
- Long sessions: CART is fatiguing; for events beyond ~1–2 hours, team with a second
  captioner and swap regularly.

## 4. After the session
- **Transcript:** if contracted, deliver an edited, cleaned transcript (not the raw feed)
  by the agreed deadline; clarify whether it's verbatim or "rough draft"-quality and
  that it's not a certified legal record.
- **Update the dictionary** with every new term from the session.
- **Confidentiality:** delete or secure files per the agreement.

## Gotchas
- Accepting a job without materials — prep is not optional for names and jargon.
- Room-mic audio with HVAC noise → poor accuracy whatever your skill.
- Zoom API token changes per meeting; using last week's token posts nowhere.
- Consumer can't resize text on a burned-in feed — offer a browser link.
- Treating the live feed as the transcript.

## Verify
- [ ] All speaker names and key terms written correctly in a pre-session test.
- [ ] Consumer confirmed visibility and latency before start.
- [ ] Every speaker change is marked in the output.
- [ ] Names, numbers and negations spot-checked in the saved file: correct.
- [ ] Dictionary updated and transcript delivered as agreed.
