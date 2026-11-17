---
id: creative-arts.animation.color.false-color-exposure-checks
name: false-color-exposure-checks
category: creative-arts
field: animation
product: color
tags: [false-color, exposure, video-scopes, clipping, hdr, nits, resolve, ffmpeg, lighting-qc]
level: practitioner
status: draft
description: "Use false colour overlays to check exposure, clipping and HDR highlight levels on renders and grades, with Resolve, monitor LUTs or an ffmpeg pseudocolor pass."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://ffmpeg.org/ffmpeg-filters.html#pseudocolor
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# False colour and exposure checks

**Goal:** see exposure zones directly on the image: each luminance band shown as a distinct colour, so clipped
or crushed areas and inconsistent faces jump out.

## Common scale (SDR, approximate IRE)

| Colour | Zone |
|---|---|
| purple/blue | near black, crushed (0-5%) |
| grey/green | mid-grey around 40-45%, often the "correct key" marker |
| pink | skin key (around 55-65%) |
| yellow | bright highlight (around 90-97%) |
| red | clipping (above 97-100%) |

Scales differ by tool (ARRI, RED, monitor makers). Learn the one you use and keep it the same across the show.

## Where to get it

- **Resolve:** recent Studio versions list a *False Color* effect under ResolveFX (check Effects > ResolveFX
  Color in your version); apply it on a disabled-for-render node or a timeline node you bypass before delivery.
  Third-party OFX plug-ins provide calibrated scales too. Unconfirmed per version: verify the effect exists.
- **Monitoring:** many reference monitors and Blackmagic/Atomos devices have built-in false colour on the input.
- **ffmpeg:** `ffmpeg -i shot.mov -vf "pseudocolor=p=range1" -frames:v 1 fc.png` (presets include `range1`,
  `range2`, `preferred`, `total`, `heat`).

## HDR

For PQ masters, map nit levels: diffuse white around 100-203 nits (ITU-R BT.2408 suggests 203 nits for graphics
white), specular highlights up to the mastering display peak (1000 nits typical). A false-colour scale in nits
shows whether a whole sequence's highlights stay below the planned MaxCLL (see
`creative-arts.animation.color.hdr-pq-hlg`).

## Animation uses

- Lighting QC: compare character key levels across a sequence; the same character in the same light should show
  the same false-colour zone.
- FX flashes and glows that clip to red across large areas need re-grading or will band on delivery.

## Verify

Every shot in a sequence shows the hero face/key area in the same zone, and red (clip) appears only on intended
speculars.
