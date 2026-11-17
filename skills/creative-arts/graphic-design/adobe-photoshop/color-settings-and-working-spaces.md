---
id: creative-arts.graphic-design.adobe-photoshop.color-settings-and-working-spaces
name: color-settings-and-working-spaces
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-color-management, color-modes, color-settings, working-space, icc-profile, srgb, adobe-rgb, fogra39, gracol, creative-cloud-synchronise, colour-management]
level: practitioner
status: draft
description: "Configure Photoshop Color Settings (RGB/CMYK working spaces, colour management policies, mismatch warnings) and synchronise them across Creative Cloud apps for consistent colour."
sources:
  - https://helpx.adobe.com/photoshop/using/color-settings.html
  - https://helpx.adobe.com/photoshop/using/working-with-color-profiles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Color Settings and working spaces

**Goal:** every file opens and converts the same way on every machine and in every Adobe app.

## Edit > Color Settings (Shift+Ctrl/Cmd+K)
**Working Spaces**
- **RGB:** sRGB IEC61966-2.1 for screen-first studios; Adobe RGB (1998) for print-first
  photography. Pick one studio-wide.
- **CMYK:** the profile matching your main press condition. Europe coated:
  **Coated FOGRA39** (ISO 12647-2:2004) or PSO Coated v3 (FOGRA51, 2013 standard). US
  sheetfed coated: **GRACoL2013** (CRPC6) or U.S. Web Coated (SWOP) v2 for web offset.
  Ask the printer; their profile beats any default.
- **Gray:** Dot Gain 15-20% or Gray Gamma 2.2 for screen.

**Color Management Policies:** set RGB, CMYK and Gray to **Preserve Embedded Profiles**.
Tick **Ask When Opening** for profile mismatches and missing profiles - you want to know.

**Conversion Options:** Engine Adobe (ACE), Intent **Relative Colorimetric** with
**Black Point Compensation** on (safe default for photos and graphics; Perceptual for
heavily out-of-gamut images - compare in soft proof).

Save the settings as a `.csf` and share it with the team.

## Synchronise across apps
Adobe Bridge > Edit > Color Settings, choose your saved setting, **Apply**. The "Unsynchronized"
warning in Photoshop/InDesign/Illustrator Color Settings disappears when all apps match.

## Mismatch dialogs on open
- **Embedded profile mismatch:** usually choose "Use the embedded profile" - the file
  knows what it is. Converting to the working space is fine for RGB-to-RGB if you want a
  uniform studio space.
- **Missing profile:** the file is untagged. Assume sRGB for web/phone images; assign
  and check visually.

## Gotchas
- Monitor calibration matters more than any setting: calibrate with a hardware device
  (target ~D65, 120 cd/m2 for print work, gamma 2.2).
- Changing the CMYK working space does not alter existing CMYK files - it changes how
  new conversions and untagged CMYK are interpreted.
- Web browsers that ignore profiles show untagged Adobe RGB images dull. Export screen
  images converted to sRGB with the profile embedded.

## Verify
- [ ] All CC apps show the same synchronised colour setting.
- [ ] Status bar (Document Profile) shows the expected profile on open.
- [ ] CMYK working space matches the printer's stated profile.
