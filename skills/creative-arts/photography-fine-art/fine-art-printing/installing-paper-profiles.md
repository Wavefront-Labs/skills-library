---
id: creative-arts.photography-fine-art.fine-art-printing.installing-paper-profiles
name: installing-paper-profiles
category: creative-arts
field: photography-fine-art
product: fine-art-printing
tags: [fine-art-printing, custom-printer-profile, paper-profile-install, icc-profile-install, media-settings, colorsync]
level: practitioner
status: draft
description: "Install and use manufacturer ICC paper profiles on Windows and macOS, match the profile's driver media settings, and choose the right black ink."
sources: ["https://www.canson-infinity.com/en/icc-profiles", "https://support.apple.com/guide/colorsync-utility/welcome/mac"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing paper profiles

## Download
From the paper manufacturer's site, choose printer model **and** ink set. Download the ICC/ICM file and
the **PDF with recommended driver settings** (media type, quality, black ink, platen gap, drying time).

## Install
- **Windows**: right-click the .icc file > Install Profile (copies it to the system colour directory,
  System32\spool\drivers\color).
- **macOS**: copy into the user ColorSync Profiles folder (Library > ColorSync > Profiles in your home folder),
  or the system Library equivalent for all users.
- Restart Lightroom/Photoshop to see it. In Lightroom Print module: Profile > Other... and tick the profile.

## Use
1. Application manages colour: choose the paper profile, rendering intent, BPC.
2. Driver: media type exactly as the PDF says (the profile was made with that ink-laydown setting), colour
   management **off**.
3. Print quality setting as specified (e.g. "Quality" / level 4-5, high speed off).

## Gotchas
- Using a profile with a different media type setting gives wrong ink amounts (bleeding or weak blacks).
- Profiles from manufacturers are generic; printer-to-printer variation can call for a custom profile.
- Delete obsolete profiles to keep menus manageable.

## Verify
- [ ] Profile appears in application; first print matches soft proof with the PDF's settings.
