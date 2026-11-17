---
id: computing-software.networking-hardware-and-wireless.asterisk.answer-playback-hangup-and-early-media
name: answer-playback-hangup-and-early-media
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, dialplan, answer, playback, hangup, progress, early-media, wait]
level: intro
status: docs-checked
description: "Use Answer, Playback, Hangup and Progress correctly: when to answer, silence padding before prompts, the noanswer option, and early media before the call is answered."
sources:
  - https://docs.asterisk.org/Configuration/Applications/Answer-Playback-and-Hangup-Applications/
  - https://docs.asterisk.org/Configuration/Applications/Early-Media-and-the-Progress-Application/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# answer, playback, hangup and early media
- `Answer(500)`: the parameter is a delay in milliseconds so the far end can begin processing audio. Do not answer before `Dial()` hands the call to another device; do answer before playing prompts or gathering input.
- `Playback(file)`: file name without extension; ignores DTMF. To avoid clipping the start of a prompt, play `silence/1` first, e.g. `Playback(silence/1&hello-world)`.
- `Hangup()`: recommended as the last priority of an extension even though fallthrough ends the call.
- Early media: audio before answer. `Progress()` signals progress so audio can be played without answering. Use `Playback(file,noanswer)` after it:
```
exten => 500,1,Progress()
exten => 500,n,Wait(1)
exten => 500,n,Playback(WeAreClosedGoAway,noanswer)
exten => 500,n,Hangup()
```
Asterisk sends RTP to a caller regardless, but doing so without a progress message is called improper and can behave differently per phone. `Queue()` does not answer automatically, so `Progress()` before `Queue(queuename)` is an option; if unsure, just answer.

For Dial usage see the Dial application page and the per-channel-driver dialing page.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Answer-Playback-and-Hangup-Applications, Early-Media-and-the-Progress-Application) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
