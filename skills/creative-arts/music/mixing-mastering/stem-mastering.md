---
id: creative-arts.music.mixing-mastering.stem-mastering
name: stem-mastering
category: creative-arts
field: music
product: mixing-mastering
tags: [mastering, mixing-mastering, stem-mastering, stems, stem-delivery, summing, vocal-stem, drum-stem, bus-processing, mastering-chain, stem-alignment, null-test]
level: advanced
status: draft
description: "Master from stems instead of a stereo mix: what stems to request, alignment and null checks, processing per stem vs on the sum, and the limits of fixing a mix at mastering."
sources: ["Bob Katz, Mastering Audio (3rd ed.), stem mastering", "https://www.soundonsound.com/", "https://www.izotope.com/en/learn"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stem mastering

**Goal:** more control at mastering (e.g. vocal level, low end) without turning mastering into
a remix.

## 1. When it helps
- The mix is good but one element needs adjustment (vocal 1 dB up, kick and bass balance, harsh guitars).
- Electronic producers mixing in less-than-ideal rooms who want an engineer's ears on the balance.
- Not a fix for a bad mix: send it back to mix if many changes are needed.

## 2. What to request
- 4-8 stereo stems: e.g. **Drums, Bass, Music (instruments), Lead vocal, BVs, FX**.
- Same length, same start point (bar 1), same sample rate and bit depth (24-bit or 32-bit float), no master-bus processing (or exactly as agreed).
- Also the stereo mix printed from the same session for reference.

## 3. Checks before processing
- Import at zero; **null test**: sum the stems and polarity-invert the stereo mix; the result should be near silence. If not, master-bus processing or missing stems differ (ask the mix engineer).
- Check alignment and that stem buses didn't double-count sends (reverb returns should be in an FX stem or included once).

## 4. Processing approach
- Minimal per-stem moves (level, a little EQ or compression) to fix balance.
- Then a normal mastering chain on the **sum** (bus EQ, compression, limiting) so everything reacts together.
- Keep a version mastered from the stereo mix for comparison; the stem version must be better, not just different.

## Gotchas
- Stems printed with each bus's compressor reacting differently from the full mix: summing doesn't null (stems printed with master processing on each).
- Scope creep: clients asking for remix-level changes at mastering prices.

## Verify
- Null test passes before work starts.
- Final master compared level-matched against the stereo-mix master; documented changes approved by the client.
