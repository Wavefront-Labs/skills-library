---
id: creative-arts.photography-fine-art.art-photography.milky-way-and-star-point-exposure
name: milky-way-and-star-point-exposure
category: creative-arts
field: photography-fine-art
product: art-photography
tags: [art-photography, night-photography, npf-rule, 500-rule, milky-way, astro-landscape, star-focus, light-pollution, sequator]
level: practitioner
status: draft
description: "Photograph the Milky Way with pinpoint stars: NPF rule exposure limits, high-ISO settings, focusing on stars, dark-sky planning and stacking for noise."
sources: ["https://www.photopills.com/articles/milky-way-photography-guide", "https://www.lightpollutionmap.info/", "https://sites.google.com/view/sequator/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Milky Way and star-point exposure

## Exposure limits
- **500 rule** (500 / focal length FF) is too lax for modern sensors.
- **NPF rule** (Frederic Michaud) accounts for aperture and pixel pitch:
  t = (35 x N + 30 x p) / f   (N f-number, p pixel pitch um, f focal length mm). PhotoPills computes it.
- e.g. 20 mm f/1.8 on 24 MP FF (p about 6): about 10.5 s for pinpoint stars.

## Settings starting point
Fast wide lens (14-24 mm, f/1.4-2.8), ISO 3200-6400, NPF time, raw, WB ~3800-4200 K, long-exposure NR
off (use dark frames instead), lens stabilisation off.

## Procedure
1. Plan: new-moon window, dark site (Bortle 1-3 from lightpollutionmap.info), Milky Way core
   position (season dependent; northern hemisphere core visible roughly Feb-Oct).
2. Focus: live view, magnify on a bright star or planet, adjust manual focus until smallest; tape the ring.
3. Compose with a foreground; shoot sky frames and a separate foreground frame (longer, lower ISO,
   or during blue hour).
4. Noise: shoot 10-20 sky frames, stack in Sequator (Windows) / Starry Landscape Stacker (Mac).

## Gotchas
- Dew on the lens: use a heater strip.
- Coma at f/1.4 corners: stop down 1/3-2/3.

## Verify
- [ ] Stars round at 100% in the corners; noise acceptable after stack.
