---
id: computing-software.general-digital-literacy.office-suites.photo-album-presentations
name: photo-album-presentations
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, pres-content, photo-album, slideshow, powerpoint]
level: intro
status: docs-checked
description: "Build a photo album slideshow in PowerPoint or Impress with captions and layouts, compress the pictures, and add background music and timings that loop."
sources:
  - https://support.microsoft.com/en-us/powerpoint/create-and-share-a-photo-album
  - https://support.microsoft.com/en-gb/office/play-music-across-multiple-slides-in-your-slide-show-in-powerpoint-b01ded6a-28c8-473a-971a-6dfa92cc9367
  - https://support.microsoft.com/en-us/office/add-or-delete-audio-in-your-powerpoint-presentation-c3b2a9fd-2547-41d9-9182-3dfaa58f1316
  - https://support.microsoft.com/en-us/powerpoint/training/record-a-slide-show-with-narration-and-slide-timings
  - https://support.microsoft.com/en-us/powerpoint/set-up-slide-show
  - https://support.microsoft.com/en-us/office/graphics-visuals/reduce-the-file-size-of-a-picture-in-microsoft-office
  - https://support.microsoft.com/en-us/powerpoint/turn-your-presentation-into-a-video
  - https://support.microsoft.com/en-us/powerpoint/create-professional-slide-layouts-with-designer
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/photo_album.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Photo album presentations

## PowerPoint (Windows: Microsoft 365, 2016-2024)
1. **Insert > Photo Album > New Photo Album**.
2. Under *Insert picture from*, **File/Disk...**: pick the pictures. Reorder with the arrow buttons; rotate,
   change brightness or contrast per picture; tick *ALL pictures black and white* if wanted.
3. **Album Layout**: *Picture layout*, *Frame shape* and *Theme* (Browse).
4. Tick **Captions below ALL pictures** (needs a picture layout chosen first; uses file names as
   placeholder text, so edit them afterwards).
5. **Create**. Change it later: Insert > Photo Album > *Edit Photo Album* › Update.
- Microsoft documents the Photo Album command for PowerPoint for Windows. Elsewhere, insert the pictures and
  use **Design > Design Suggestions** (Designer, Microsoft 365) to lay them out.

## LibreOffice Impress
**Insert › Media › Photo Album** › Add pictures › choose images per slide in *Slide layout*, tick *Add
caption to each slide*, *Keep aspect ratio* or *Fill screen* › **Insert Slides**. *Link images* links
instead of embedding. Undo does not remove an album; delete its slides.

## Music and auto-play (PowerPoint)
- **Insert > Audio > Audio on My PC**, then Playback tab › **Play in Background** (starts automatically
  and plays across slides). *Loop until Stopped* repeats the track.
- **Transitions > Advance Slide > After**, enter the seconds per slide.
- **Slide Show > Set Up Slide Show > Loop continuously until 'Esc'** for events.

## Keep the file small
- Select a picture, **Picture Format > Compress Pictures**, clear *Apply only to this picture* so it applies to
  all, choose a lower resolution (the Microsoft 365 default is 220 ppi), and tick *Delete cropped areas of
  pictures*.
- Make a video to share: **File > Export > Create a Video** (for example Full HD 1080p) using the timings.

## Gotchas
- Use music files you have the rights to and that are saved on your computer; web music must be
  downloaded first.

## Verify
- [ ] Play from start: music continues, slides advance, the show loops.

## Checked
2026-10-27, against Microsoft Support (Create and share a photo album, applies to PowerPoint for Microsoft 365 and 2016-2024; play music across slides; add or delete audio; slide timings; Set Up Slide Show; compress pictures; turn a presentation into a video; Designer) and the LibreOffice help master branch (Impress Photo Album). Confirmed: Photo Album dialog options, captions behaviour, Edit Photo Album, Play in Background and Loop until Stopped, Advance Slide After, Loop continuously until 'Esc', Compress Pictures options and the 220 ppi default, video export, Designer now labelled Design Suggestions, and the Impress Photo Album dialog. Removed unconfirmed ppi presets, HEIC and portrait-photo claims, and the claim that Play in Background loops.
Method: documentation only; no commands were run.
