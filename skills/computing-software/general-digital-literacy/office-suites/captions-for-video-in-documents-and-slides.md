---
id: computing-software.general-digital-literacy.office-suites.captions-for-video-in-documents-and-slides
name: captions-for-video-in-documents-and-slides
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, accessible-documents, video-captions, closed-captions, srt-vtt, insert-captions]
level: practitioner
status: docs-checked
description: "Add closed captions to videos and audio in PowerPoint with VTT or SRT files, caption Drive videos used in Google Slides, and supply transcripts for audio."
sources:
  - https://support.microsoft.com/en-us/powerpoint/add-closed-captions-or-subtitles-to-media-in-powerpoint
  - https://support.microsoft.com/en-us/powerpoint/compress-your-media-files
  - https://support.google.com/drive/answer/1372218
  - https://www.w3.org/WAI/media/av/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Captions for video in documents and slides

## Get a caption file
- Write one yourself or use a caption-creation tool; correct names, jargon and numbers in anything generated
  automatically.
- Formats for PowerPoint: **WebVTT (.vtt)**; newer versions also accept **SubRip (.srt)** files saved as UTF-8
  (PowerPoint for Windows version 2411+, PowerPoint for Mac 16.91+).

## PowerPoint (Microsoft 365 and 2016-2024 on Windows; Mac 16.63+ for WebVTT)
1. Insert the video (Insert › Video › This Device).
2. Select it › **Playback › Insert Captions › Insert Captions** › choose the file(s) › Insert.
3. Play the video and check the captions appear correctly.
- Remove: Playback › Insert Captions › **Remove All Captions** (removes every caption file on that video).
- Newer Windows builds also offer Insert Captions on the Accessibility ribbon (2111+) and the video's right-click
  menu (2208+); audio files can take captions from version 2303.
- Captions can't be added to online (YouTube) videos inserted into PowerPoint.

## Google Slides
Caption the video in Google Drive before inserting it: right-click the video in Drive › **File information ›
Manage caption tracks** › add a caption file (for example .srt or .sbv, under 2 MB), or generate automatic
captions there.

## Transcripts
Provide a transcript (a text version of the speech and non-speech audio) next to audio-only content such as
podcasts or voice recordings.

## Gotchas
- PowerPoint's **Compress Media** drops embedded subtitles; compress before adding captions, or re-add them after.
- Caption files apply to one Drive file version; uploading a new version removes them.

## Verify
- [ ] Play the video muted: captions appear, are in sync and identify speaker changes.

## Checked
2026-10-27, against Microsoft Support (Add closed captions or subtitles to media in PowerPoint; Compress your media files), Google Drive Help (Add caption tracks to your video files) and W3C WAI (Making audio and video media accessible). Confirmed: WebVTT support by version, SRT support from Windows 2411 and Mac 16.91, the Insert Captions and Remove All Captions paths, alternative entry points and audio captions by version, the online-video exclusion, Drive's Manage caption tracks path, formats, size limit and versioning, the WAI transcript definition, and Compress Media dropping subtitles. Corrected the claim that PowerPoint needs SRT converted to VTT; removed unconfirmed YouTube/Stream download steps and a burned-in captions claim.
Method: documentation only; no commands were run.
