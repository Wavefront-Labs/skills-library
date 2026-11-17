---
id: computing-software.general-digital-literacy.office-suites.video-and-audio-on-slides
name: video-and-audio-on-slides
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slide-content, slide-video, slide-audio, embed-video, youtube-in-slides, trim-video, play-automatically]
level: intro
status: docs-checked
description: "Insert video and audio into slides (file or YouTube), trim clips, set play automatically or on click, and make sure media plays on the presenting computer."
sources:
  - https://support.microsoft.com/en-us/powerpoint/insert-and-play-a-video-file-from-your-computer
  - https://support.microsoft.com/en-us/office/insert-a-video-from-youtube-or-another-site-8340ec69-4cee-4fe1-ab96-4849154bc6db
  - https://support.microsoft.com/en-us/office/add-or-delete-audio-in-your-powerpoint-presentation-c3b2a9fd-2547-41d9-9182-3dfaa58f1316
  - https://support.microsoft.com/en-us/powerpoint/video-and-audio-file-formats-supported-in-powerpoint
  - https://support.microsoft.com/en-us/powerpoint/compress-your-media-files
  - https://support.microsoft.com/en-us/powerpoint/add-closed-captions-or-subtitles-to-media-in-powerpoint
  - https://support.google.com/docs/answer/97447
  - https://github.com/LibreOffice/help/blob/master/source/text/shared/00/00000404.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Video and audio on slides

**Goal:** media that plays when you click, on whatever computer you present from.

## Insert
- **PowerPoint:** Insert › Video › **This Device** (embedded by default; *Link to File* from the Insert button's
  arrow), Stock Videos, or **Online Video** (paste a YouTube or Vimeo link; needs internet when presenting, and
  Trim, Fade and bookmarks don't apply). Insert › Audio › **Audio on My PC** / **Record Audio**.
- **Google Slides:** Insert › Video › Search YouTube / By URL / Google Drive (put your own video files in Drive
  first). Audio: Insert › Audio picks .mp3 or .wav files from Drive.
- **Impress:** Insert › Media › **Audio or Video**.

## Playback options
- PowerPoint Playback tab › Start: *In Click Sequence* (default) / *Automatically* / *When Clicked On*.
- Trim and Fade for embedded clips; for audio, *Play Across Slides*, *Loop until Stopped* or **Play in
  Background** (starts automatically and plays across slides).
- Google Slides: select the video › Format options › Video playback › *Play (on click)* (default),
  *Play (automatically)* or *Play (manual)*.

## Make it work on the day
- Embedded files travel inside the .pptx; online videos need a working connection at the venue. If you link to
  a file, Microsoft suggests copying the video into the same folder as the presentation first.
- Use **MP4 (H.264 video, AAC audio)**, Microsoft's recommended format; .mov and .webm are also supported.
  In PowerPoint version 2505 and later, support for WMV, MPEG-2, AVI, AIFF and 3GPP is limited and deprecated
  (files are converted to MP4), and MIDI audio is no longer supported.
- PowerPoint for Windows: File › Info › **Compress Media** (Full HD, HD or Standard) shrinks the file but drops
  embedded subtitles and alternate audio tracks.
- Test on the presenting laptop with its speakers or the room's HDMI audio.

## Gotchas
- Only use video you have rights to.
- Add captions for speech: Playback › **Insert Captions** with a WebVTT (.vtt) file, or UTF-8 SRT in newer
  versions (Windows 2411+, Mac 16.91+). Not available for online videos.

## Verify
- [ ] Full rehearsal on the actual presenting machine plays every clip with sound.

## Checked
2026-10-27, against Microsoft Support (Insert and play a video file; Insert a video from YouTube or another site; Add or delete audio; Video and audio file formats; Compress your media files; Add closed captions; PowerPoint for Microsoft 365 and 2016-2024), Google Docs Editors Help (Insert images and videos) and the LibreOffice help master branch (Insert menu). Confirmed: video and audio insert paths, embed vs link, online-video limits, Start options, audio playback options, Google video sources, playback modes and audio formats, Impress Insert › Media › Audio or Video, recommended and deprecated formats (version 2505), Compress Media options and what it drops, and caption formats. Removed an unconfirmed "Optimise Media Compatibility" command and an Impress linking claim.
Method: documentation only; no commands were run.
