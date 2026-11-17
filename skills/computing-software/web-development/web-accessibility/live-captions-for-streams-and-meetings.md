---
id: computing-software.web-development.web-accessibility.live-captions-for-streams-and-meetings
name: live-captions-for-streams-and-meetings
category: computing-software
field: web-development
product: web-accessibility
tags: [live-captions, real-time-captioning, cart-captioning, wcag-1-2-4]
level: practitioner
status: docs-checked
description: "Live captions for streams and webinars: WCAG 1.2.4 scope, CART vs automatic captions, caption content, and cleaning up captions for the recording."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/captions-live.html
  - https://www.w3.org/WAI/media/av/captions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live captions for streams and meetings

## 1. What WCAG requires
- SC 1.2.4 Captions (Live), Level AA: captions are provided for all live audio content in synchronized media.
- Intent: let people who are deaf or hard of hearing follow real-time presentations. Captions include dialogue, identify who is speaking and note sound effects and other significant audio.
- Scope: intended for broadcast of synchronized media. It is not intended to require captions on two-way multimedia calls between individuals through web apps regardless of user needs; responsibility falls to the content providers (the callers) or the host caller, not the application.
- No captions needed when the video has no audio information needed to understand it (for example only background music).
- Examples from W3C: a live captioned web cast; an orchestra providing CART captioning of each real-time web performance, covering lyrics and dialogue and identifying non-vocal music by title, movement and composer.

## 2. Human vs automatic
- Live captions are usually done by professional real-time captioners or CART (Communication Access Realtime Translation) providers, in person or remotely over a phone or Internet audio connection.
- W3C: automatically generated captions do not meet user needs or accessibility requirements unless confirmed fully accurate; they usually need significant editing, and a single missing word such as "not" can contradict the audio. W3C says they can serve as a starting point for accurate captions.
- WCAG 1.2.4 Understanding note: captions may be generated using a real-time text translation service.

## 3. Techniques listed as sufficient
- G9: creating captions for live synchronized media, together with either G93 (open, always-visible captions) or G87 (closed captions) using a readily available media format whose video player supports closed captioning (or SMIL synchronized text streams SM11/SM12).
- Closed captions can be turned on and off; open captions cannot be turned off. Captions should not obscure or obstruct relevant information in the video.

## 4. After the event
If you post a recording of live captioned content you will probably need to do minor editing for accuracy. WebVTT is the most common caption format on the web. Prerecorded captions are required at Level A (1.2.2).

## Verify
- [ ] Captions appear in the player during a test stream; spot-check accuracy against the audio; recording republished with corrected captions.

## Checked
Method: docs-only read on 2026-11-09 of W3C Understanding SC 1.2.4 in full and the W3C WAI Captions/Subtitles page (introduction, live captions, requirements and automatic-caption sections; first 70 lines of extracted text). Dropped sources: Apple HLS authoring specification (excluded domain) and the FCC guide (not read). Removed as unstated: accuracy and latency figures, cost, CEA-608/708 and HLS delivery details, meeting platform setup, player requirements beyond the stated note, 1.2.9 claim, and the live-streaming tag.
