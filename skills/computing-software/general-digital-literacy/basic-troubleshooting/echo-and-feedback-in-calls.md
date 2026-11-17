---
id: computing-software.general-digital-literacy.basic-troubleshooting.echo-and-feedback-in-calls
name: echo-and-feedback-in-calls
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-audio-video, echo-in-calls, audio-feedback, noise-suppression]
level: intro
status: draft
description: "Stop echo, howling feedback and others hearing themselves in Teams, Zoom and Meet calls with headphones, the right mic, echo cancellation and room fixes."
sources:
  - https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0059865
  - https://support.microsoft.com/en-us/office/manage-audio-settings-in-microsoft-teams-meetings
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Echo and feedback in calls

## Who has the problem?
If **you hear yourself**, the echo is coming from **someone else's** setup (their speakers feed your voice into their mic). If others hear themselves, it is yours. Mute participants one at a time to find the source.

## Fixes (in order)
1. **Headphones or earbuds**: the near-universal cure; speakers + mic is the cause.
2. **Two devices in the same room** both in the call (laptop + phone, two colleagues side by side): mute and disconnect audio on all but one; join extra devices with *Don't use audio* / *Companion mode*.
3. Lower speaker volume; move the laptop away from walls and hard surfaces.
4. **Choose the right mic**: Teams/Zoom settings › Audio › pick the headset mic, not the laptop/webcam mic far away.
5. App settings: Zoom › Audio › *Suppress background noise* Auto; keep *Original sound* **off** unless you are a musician with headphones. Teams › Settings › Devices › *Noise suppression* Auto.
6. Windows: Settings › Sound › input device › turn off *Listen to this device* (Control Panel › Sound › Recording › Properties › Listen). It plays your mic back to you.
7. Bluetooth headsets switch to low-quality "hands-free" mode; a wired or USB headset sounds better.

## Meeting rooms
- One room system per room; laptops in the room join with audio off. Speakerphones (Jabra, Poly) have proper echo cancellation.

## Verify
- [ ] In a test call (Teams Make a test call, Zoom zoom.us/test) playback sounds clear with no repeat.
