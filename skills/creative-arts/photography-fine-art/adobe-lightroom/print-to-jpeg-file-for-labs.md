---
id: creative-arts.photography-fine-art.adobe-lightroom.print-to-jpeg-file-for-labs
name: print-to-jpeg-file-for-labs
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, print-to-file, lightroom-print-module, lab-printing, jpeg-file, lightroom-classic]
level: practitioner
status: draft
description: "Use Lightroom Classic Print to JPEG File to send labs exact-size files with borders, custom file dimensions, resolution, sharpening and ICC profile conversion."
sources: ["https://helpx.adobe.com/lightroom-classic/help/print-module-basics.html", "https://helpx.adobe.com/lightroom-classic/desktop/help/printing-photos-basic-workflow.html", "https://helpx.adobe.com/lightroom-classic/user-guide.html (Print to JPEG)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Print to JPEG file for labs

Print Job panel > Print To: **JPEG File**. The page layout becomes a JPEG with the exact page dimensions, including borders, keylines, text and multiple images.

## Settings
- **File Resolution**: what the lab requests (usually 300 ppi; Fujifilm Frontier/Noritsu labs often 300; some large-format labs 200-240).
- **Print Sharpening**: Standard, Glossy (C-type is a glossy/lustre medium) unless the lab sharpens.
- **JPEG Quality**: 100 for lab files.
- **Custom File Dimensions**: set to the paper size (e.g. 12 x 18 in) so the page equals the paper the lab prints on; margins in Layout panel become printed white borders.
- **Color Management > Profile**: sRGB by default, or choose the lab's paper/printer ICC profile (Other... to load it) and Rendering Intent Perceptual/Relative. Soft proof with the same profile first.

## Steps
1. Get the lab's specs: paper sizes, profile, whether they convert or expect sRGB, whether to turn off their auto-correction ("no colour correction").
2. Set Page via Custom File Dimensions; lay out cell; template it as `Lab - 12x18 - lustre`.
3. Print to File..., name per lab convention.

## Gotchas
- Lab files with embedded custom profiles get converted to sRGB by labs that ignore profiles; ask.
- Borders made in Lightroom avoid lab cropping surprises (labs often crop 2-3 mm on borderless prints).

## Verify
- [ ] Opened JPEG shows the exact page px (inches x ppi) and correct profile; lab test print matches the soft proof.
