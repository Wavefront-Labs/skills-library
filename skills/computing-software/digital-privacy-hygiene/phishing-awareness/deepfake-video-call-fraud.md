---
id: computing-software.digital-privacy-hygiene.phishing-awareness.deepfake-video-call-fraud
name: deepfake-video-call-fraud
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, deepfake-video-call, business-email-compromise, family-safe-word]
level: practitioner
status: draft
description: "Defend against payment fraud on deepfaked video and voice calls: verification callbacks, code words, dual approval, and live challenge limits."
sources:
  - "https://www.ic3.gov/PSA/2024/PSA241203"
  - "https://www.cisa.gov/topics/election-security/foreign-influence-operations"
  - "https://consumer.ftc.gov/consumer-alerts/2023/03/scammers-use-ai-enhance-their-family-emergency-schemes"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Deepfake video call fraud

**Goal:** a convincing face and voice on a call can't authorise a payment or a credential change.

## What's happening
Criminals use real-time face and voice synthesis to impersonate executives, colleagues or relatives on video calls.
In a widely reported 2024 Hong Kong case, an employee transferred about US$25 million after a video meeting where
every other participant was deepfaked. The FBI has warned about generative AI in fraud (IC3 PSA, Dec 2024).

## Controls that work
- **Process, not perception:** payments and bank-detail changes need a second approver and a callback to a number
  from your records, regardless of who asked on a call.
- **Code words:** a family safe word; for small teams, a pre-agreed verification phrase for urgent requests.
- **Out-of-band confirmation:** message the person on a known channel ("did you just ask me to...?").
- **Slow down:** urgency plus secrecy plus money = verify.

## Live checks (weak but useful)
Ask the person to turn their head fully sideways, pass a hand across their face, or answer something only the real
person knows. Real-time deepfakes improve constantly; failing a check is informative, passing isn't proof.

## Reduce source material
Executives and public figures have abundant video; assume they can be cloned. Personal accounts: limit public video
and voice where practical.

## Gotchas
- Deepfake calls often follow a phishing email that "sets up" the meeting.
- Report attempts to your bank and IC3 even if no money moved.
