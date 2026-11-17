---
id: computing-software.digital-privacy-hygiene.privacy-configuration.siri-and-dictation-privacy
name: siri-and-dictation-privacy
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, siri-privacy, apple-privacy, voice-recording-review]
level: practitioner
status: docs-checked
description: "Reduce what Siri and dictation keep: opt out of Improve Siri recordings, turn off Search improvement, limit location and per-app learning, and clear on-device history."
sources:
  - "https://www.apple.com/legal/privacy/data/en/ask-siri-dictation/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Siri and dictation privacy

**Goal:** Siri works for you without storing more voice data than necessary. Source: Apple's "Siri, Dictation &
Privacy" page (dated 2026-10-26). Menu names follow that page and vary by iOS version.

## What Apple says it keeps
- Default: audio is not stored by Apple unless you opt in to Improve Siri & Dictation (or Improve Siri & Apple
  Intelligence). Opting in lets Apple collect, store and review audio and text of what you say, tied to a random
  device-generated identifier that rotates multiple times per hour, not your Apple Account.
- Request data (category of request, success, device configuration, performance statistics, and approximate
  location if Location Services is on for Siri) is kept with that identifier for up to two years.
- Search requests via Siri are stored and used to improve Search, Siri and related features.
- Contextual data such as contact names, device names and app names may be sent to help Siri understand you.
- A history of Siri and Dictation interactions is stored on your device to personalise Siri.

## Settings Apple lists
- **Opt out of recording review**: Settings > Privacy & Security > Analytics & Improvements > turn off Improve Siri &
  Dictation (or Improve Siri & Apple Intelligence).
- **Search improvement**: Settings > Search > turn off Help Apple Improve Search.
- **Siri location**: Settings > Privacy & Security > Location Services > Siri > Never. Suggestions location:
  Location Services > System Services > turn off Suggestions & Search.
- **Per-app learning**: Settings > Siri > Excluded Apps to stop Siri using information from an app; Settings > Siri >
  Suggestions > [app name] to control suggestions per app; Settings > Siri > App Clips > turn off Learn from App
  Clips.
- **Siri sync**: Settings > [your name] > iCloud > Saved to iCloud > See All > turn off Siri (stops personalisation
  syncing across devices; sync is end-to-end encrypted).
- **Speech recognition**: Settings > Privacy & Security > Speech Recognition controls which apps may use it; audio
  to be transcribed may be sent to Apple.
- **Delete on-device transcripts**: turning off Siri (Settings > Siri > Turn Off Siri) deletes the stored Siri and
  Dictation transcripts on your device; if you also turn off Dictation (Settings > General > Keyboard > Enable
  Dictation), the transcripts used for personalisation are deleted.
- **Restrict entirely**: Settings > Screen Time > Content & Privacy Restrictions > Other Features > Siri or
  Dictation.

## On-device processing
Siri and Keyboard settings indicate whether what you say is processed on device; otherwise it is sent to and
processed by Apple. If you enable Siri AI, requests may be processed on device or in Private Cloud Compute, which
Apple says does not retain your data. Third-party apps and services that Siri uses have their own privacy policies.

## Gotchas
- Opting out of Improve Siri does not stop requests being processed; the page says audio is sent to Apple unless the
  setting shows on-device processing.
- Other voice assistants (Alexa, Google) have their own recording settings; see the smart-speaker skills.

## Checked
Checked 2026-11-08 against the full text of Apple's "Siri, Dictation & Privacy" page. The Apple Support article
102390 (certificate trust profiles) is unrelated and the iPhone guide link redirected to a generic welcome page, so
both were dropped from sources. Removed what the page does not state: the lock-screen Face ID & Passcode toggle,
Listen for Siri, the "Delete Siri & Dictation History" button, and the Shortcuts note.
Method: documentation only; no commands were run.
