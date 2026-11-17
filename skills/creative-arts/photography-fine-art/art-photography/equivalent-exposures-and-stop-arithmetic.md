---
id: creative-arts.photography-fine-art.art-photography.equivalent-exposures-and-stop-arithmetic
name: equivalent-exposures-and-stop-arithmetic
category: creative-arts
field: photography-fine-art
product: art-photography
tags: [art-photography, exposure-control, equivalent-exposure, stops, f-stop, exposure-value, reciprocity-law, sunny-16, filter-factor]
level: practitioner
status: draft
description: "Calculate equivalent exposures across aperture, shutter and ISO in full and third stops, and convert ND and filter factors into exposure time."
sources: ["Ansel Adams, The Camera (exposure)", "https://en.wikipedia.org/wiki/Exposure_value", "https://en.wikipedia.org/wiki/Sunny_16_rule"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Equivalent exposures and stop arithmetic

One **stop** doubles or halves the light. Any combination giving the same total light is
an **equivalent exposure** (reciprocity law; breaks down for film at long times - see
reciprocity failure).

## The scales (full stops)
- Aperture: f/1.4, 2, 2.8, 4, 5.6, 8, 11, 16, 22, 32, 45, 64 (each x1.41)
- Shutter: 1/1000, 1/500, 1/250, 1/125, 1/60, 1/30, 1/15, 1/8, 1/4, 1/2, 1 s, 2, 4, 8...
- ISO: 100, 200, 400, 800, 1600, 3200
- Third stops: f/4, 4.5, 5, 5.6; 1/125, 1/100, 1/80, 1/60; ISO 100, 125, 160, 200.

## Worked example
Meter: f/8, 1/125, ISO 100. You want f/2.8 for shallow focus -> 3 stops more light at the
aperture, so 3 stops less time: 1/125 -> 1/250 -> 1/500 -> 1/1000. Result f/2.8, 1/1000.

## EV
EV = log2(N^2 / t) at ISO 100. f/16 at 1/125 = EV 15 (sunny day). Each EV is one stop.

## Filter factors
- Factor 2 = 1 stop, 4 = 2, 8 = 3, 1000 (ND 3.0) = 10 stops.
- ND density: 0.3 = 1 stop. ND 1.8 = 6 stops; 64x.
- 10-stop ND from 1/60 s: 1/60 x 1024 = about 17 s.

## Sunny 16 sanity check
Bright sun, distinct shadows: f/16 at 1/ISO. Slight overcast f/11, overcast f/8,
heavy overcast f/5.6, open shade f/4.

## Gotchas
- Lens markings round off; 1/125 is really 1/128. Doesn't matter until you chain many stops.
- Camera displays cap at 30 s; use Bulb and a timer beyond that.

## Verify
- [ ] You can reach an equivalent exposure in your head and confirm with the meter.
