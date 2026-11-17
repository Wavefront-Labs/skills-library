---
id: computing-software.general-digital-literacy.digital-communication.messaging-and-video-calls
name: messaging-and-video-calls
category: computing-software
field: general-digital-literacy
product: digital-communication
tags: [digital-communication, messaging, instant-messaging, chat, whatsapp, signal, imessage, sms, rcs, slack, microsoft-teams, teams, zoom, google-meet, facetime, video-calls, video-conferencing, mute-shortcut, screen-sharing, netiquette, online-etiquette, async-communication, end-to-end-encryption, sharing-links, file-sharing, do-not-disturb, headset, echo]
level: intro
status: docs-checked
description: "Pick the right channel, write chat messages people can act on, run video calls on Zoom/Teams/Meet without audio or sharing mishaps, and share content safely."
sources:
  - https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0067050
  - https://support.microsoft.com/en-us/accessibility/teams/keyboard-shortcuts-for-microsoft-teams
  - https://support.google.com/meet/answer/9298571
  - https://support.apple.com/en-us/109510
  - https://telegram.org/faq
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Messaging and video calls - clear, courteous, and no "you're on mute"

**Goal:** choose the right channel for the message, write messages that don't need a follow-up, join calls ready to talk, and share files without leaking them.

## 1. Choose the channel
| Need | Channel |
|---|---|
| Quick question, low stakes | Chat (Teams, Slack, WhatsApp) |
| Decision, record, external party | Email |
| Nuance, conflict, many back-and-forths | Call or video call |
| Urgent and time-critical | Phone call, then a written follow-up |
Rule of thumb: if a chat thread passes ~5 exchanges without resolution, switch to a call and post the outcome in writing afterwards.

## 2. Writing messages
- **Don't send "Hi" and wait.** Put greeting, context and question in one message: "Hi Sam - could you send the October rota by 3pm? I need it for payroll."
- Reply **in the thread** (Slack/Teams) so conversations stay together; @-mention only people who must act.
- Tone is easy to misread in text: no ALL CAPS, add a little warmth, use a reaction to acknowledge instead of a separate "ok".
- Respect time zones and off-hours: use scheduled send where available, and don't expect instant replies.
- Assume anything you send can be screenshotted and forwarded. "Delete for everyone" isn't guaranteed.

## 3. Privacy of the channel
- Encryption differs by app and mode. Telegram says only its *Secret Chats* use end-to-end encryption (ordinary Telegram chats are cloud chats). Read each app's own help for what is encrypted before you rely on it.
- End-to-end encrypted RCS between iPhone and Android was announced in beta in May 2026 and depends on iOS version, carrier and Google Messages version. Apple lists supported carriers on its RCS carrier page; check there before assuming a chat is encrypted.
- Work chat (Teams, Slack) is readable and retained by your employer. Keep personal matters out and follow company policy for confidential data.

## 4. Video calls that go smoothly
**Before:** test camera, mic and speakers: Zoom's test meeting (zoom.us/test), Teams Settings > Devices > Make a test call (desktop, work or school account), Google Meet's preview screen before joining. Use a **headset or earbuds** to stop echo; join 2-3 minutes early.

**Mute/camera shortcuts:**
| App | Mute | Camera |
|---|---|---|
| Zoom | `Alt+A` (Mac `Cmd+Shift+A`); on Mac hold `Space` to talk while muted | `Alt+V` (Mac `Cmd+Shift+V`) |
| Teams | `Ctrl+Shift+M` (Mac `Cmd+Shift+M`) | `Ctrl+Shift+O` (Mac `Cmd+Shift+O`) |
| Google Meet | `Ctrl+D` (Mac `Cmd+D`) | `Ctrl+E` (Mac `Cmd+E`) |
Stay muted when not speaking in calls over ~4 people.

**Picture and connection:** face a window or lamp (light in front, not behind); camera at eye level. If video stutters, turn off your camera first, close other uploads, and move closer to the router or plug in a cable.

**Screen sharing:** share **a single window**, not the whole screen, so notifications and other tabs stay private; turn on Do Not Disturb or Focus first. Stop sharing as soon as you're done.

**Recording:** announce it and get agreement before recording; consent rules vary by country and organisation, so check yours.

## 5. Sharing content
- Share a **link with explicit permission** (view / comment / edit) instead of attaching copies. Prefer "specific people" over "anyone with the link" for anything private; set an expiry where the service supports it.
- Don't forward other people's messages, photos or documents beyond the original audience without asking.
- Check what a shared photo reveals (addresses, documents in the background, location metadata) before posting publicly.

## Verify
- [ ] The channel matched the message (chat vs email vs call).
- [ ] Your messages carry the full question; no bare "Hi".
- [ ] You can mute and unmute by keyboard in your main call app.
- [ ] Screen shares show one window with notifications silenced.
- [ ] Shared links are restricted to the people who need them.

## Checked
Date: 2026-10-27. Documentation: Zoom Support KB0067050 (fetched), Microsoft Support Teams keyboard shortcuts, Google Meet keyboard shortcuts (via search results), Apple Support RCS carrier page, Telegram FAQ. Confirmed: all three shortcut rows (Zoom push-to-talk listed for Mac only), Teams test-call path (Microsoft Q&A), Telegram Secret Chats statement, RCS end-to-end encryption still beta on listed carriers. Removed unconfirmed claims (default encryption of Signal, WhatsApp, iMessage, SMS; Meet "Join now" wording).
Method: documentation only; no commands were run.
