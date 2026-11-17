---
id: creative-arts.animation.encode-delivery.imsc1-ttml-for-professional-delivery
name: imsc1-ttml-for-professional-delivery
category: creative-arts
field: animation
product: encode-delivery
tags: [imsc, imsc1, ttml, timed-text, subtitles, w3c, netflix-timed-text, delivery]
level: advanced
status: draft
description: "Prepare IMSC1 (TTML) subtitle files for professional delivery: text versus image profiles, document skeleton, timing basis, styling and regions, validation."
sources:
  - https://www.w3.org/
  - https://backlothelp.netflix.com/hc/en-us/articles/360053755033-Netflix-IMSC-1-1-Text-Profile
  - https://backlothelp.netflix.com/hc/en-us/articles/215758617
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IMSC1/TTML for professional delivery

**TTML** (Timed Text Markup Language) is a W3C XML standard for timed text. **IMSC1** (Internet Media Subtitles and Captions 1) is a W3C profile of TTML for subtitles and captions, with a **Text Profile** (text as characters) and an **Image Profile** (bitmap subtitles). It is used in IMF packages and by streaming services. Netflix publishes a fixed **IMSC 1.1 Netflix Text** profile (designator `nst1`, identifier `https://www.netflix.com/ns/imsc1.1/text/1`, listing each W3C feature as permitted, "should not be used" or prohibited, where prohibited features get the delivery rejected), but per Netflix's own page IMSC1.1 is currently a valid delivery format **only for Japanese-language** timed text; other languages use TTML1 under Netflix's general timed text rules (checked 2026-10-18 on backlothelp.netflix.com). Check each platform's current spec for the exact profile, naming and rules.

## Skeleton (illustrative)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<tt xmlns="http://www.w3.org/ns/ttml"
    xmlns:tts="http://www.w3.org/ns/ttml#styling"
    xmlns:ttp="http://www.w3.org/ns/ttml#parameter"
    xml:lang="en" ttp:timeBase="media" ttp:frameRate="24">
  <head>
    <styling><style xml:id="s1" tts:fontFamily="proportionalSansSerif"
      tts:fontSize="100%" tts:color="white" tts:textAlign="center"/></styling>
    <layout><region xml:id="bottom" tts:origin="10% 80%" tts:extent="80% 15%"
      tts:displayAlign="after"/></layout>
  </head>
  <body><div>
    <p begin="00:00:01:00" end="00:00:03:12" region="bottom" style="s1">Hello there.</p>
  </div></body>
</tt>
```
Whether times use frames (`hh:mm:ss:ff`) or clock time (`hh:mm:ss.mmm`) depends on the delivery spec, and frame times require the right `ttp:frameRate` (and `ttp:frameRateMultiplier` for 23.976/29.97 rates).

## Points that matter
- **Time base and frame rate** must match the video; a mismatch drifts or offsets cues.
- **Language** via `xml:lang`; one file per language.
- **Regions and styles** place and style text; use the profile's allowed features and keep it simple (many players ignore exotic styling).
- **Line length and reading speed** rules come from the style guide (`subtitles-captions.md`), not from TTML.
- Encode as **UTF-8** and escape `&`, `<`.

## Validation
Run a TTML/IMSC validator (W3C-provided tools exist) and any platform's own checker before delivery; open in a player to see the timing.

## Verify
- [ ] Profile and version match the spec.
- [ ] Frame rate and time format match the picture.
- [ ] Validator passes and sample cues render in the right place.
