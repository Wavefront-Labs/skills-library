---
id: creative-arts.music.mixing-mastering.dynamic-eq
name: dynamic-eq
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, eq, equalisation, dynamic-eq, frequency-selective-dynamics, fabfilter-pro-q, threshold, range, sidechain-eq, resonance-control, harshness, sibilance, mastering-eq]
level: practitioner
status: draft
description: "Use dynamic EQ to cut or boost a band only when it exceeds a threshold: harsh vocals, boomy notes, cymbal spikes, and sidechain-keyed unmasking, with settings and checks."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. Frequency-Selective Dynamics", "https://www.fabfilter.com/help/pro-q/using/dynamic-eq"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic EQ

**Goal:** fix frequency problems that come and go without dulling the sound all the time.

## 1. When to use it (instead of static EQ)
- A singer's harshness at 3 kHz only on loud belted notes.
- One bass note booming at 90 Hz.
- Acoustic guitar boom on certain chords; cymbal spikes in overheads.
- Mastering: taming occasional harshness or low-mid build-up.

## 2. Setting it up (Pro-Q 3/4, TDR Nova, Logic/Live EQ-with-dynamics, etc.)
1. Find the frequency with a narrow boost sweep while the problem plays.
2. Set the band to a cut with a moderate Q (1-4 for resonances; wider for general harshness).
3. Enable **dynamic** mode; set the **range** (maximum cut, e.g. -3 to -6 dB) rather than a static gain.
4. Lower the **threshold** until the band only moves on the problem moments.
5. Attack/release: fast attack (1-10 ms) for transient harshness, release 50-150 ms to avoid pumping. Many plugins auto-set these.
6. Watch the band's activity indicator: it should move only when the problem occurs.

## 3. Sidechain (external) keying
- Key the dynamic band on the guitar bus from the lead vocal: dip 2-4 kHz on guitars only when the vocal is present. Unmasks without permanently thinning the guitars.

## 4. Upward dynamic EQ
- Expand a band when it's quiet (e.g. bring up air on soft passages); use sparingly.

## Gotchas
- Using dynamic EQ for everything: static problems need static EQ.
- Too low a threshold = constant cut = static EQ with extra artefacts.
- De-essing at 6-9 kHz is a dynamic EQ job, but a dedicated de-esser's detection may be easier to set.

## Verify
- Bypass A/B at matched level: the problem moments improve and the rest sounds unchanged.
- Gain-reduction display shows activity only on the problem passages.
