---
id: computing-software.digital-privacy-hygiene.privacy-configuration.managing-ai-meeting-assistants
name: managing-ai-meeting-assistants
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, ai-meeting-assistant, ai-tools, zoom, microsoft-teams, transcription, recording-consent, otter]
level: practitioner
status: draft
description: "Control AI notetakers in meetings (Zoom AI Companion, Teams Copilot, Gemini, Otter bots): host settings, removing uninvited bots, consent and transcript retention."
sources:
  - "https://support.zoom.com/"
  - "https://learn.microsoft.com/en-us/microsoftteams/"
  - "https://ssd.eff.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Managing AI meeting assistants

**Goal:** sensitive conversations should not be recorded, transcribed and summarised to third-party servers
without everyone knowing and agreeing.

## The risks
- Bots (Otter, Fireflies, Read.ai) join automatically from an attendee's calendar and email summaries to all
  attendees, including external ones.
- Recording-consent laws: many US states and countries require all-party consent; a silent notetaker can breach them.
- Transcripts may be retained indefinitely or used for model improvement depending on the vendor plan.

## As host
- **Zoom**: Settings > AI Companion: turn off meeting summary/questions by default, or require host approval;
  enable Waiting Room and "Only authenticated users can join" so bots cannot walk in; remove bot participants
  (Participants > More > Remove) and lock the meeting.
- **Microsoft Teams**: Meeting options > Copilot and recording: "Only during the meeting" (no retained transcript)
  or off; disable automatic recording; control who can record.
- **Google Meet**: Gemini "Take notes for me" and transcripts are host-controlled; turn off in meeting settings,
  admins can disable org-wide.
- Say at the start: "This meeting is not to be recorded or transcribed."

## As participant
- Ask when you see "recording/transcribing" banners or a bot name; you can object or leave.
- Check your own integrations: Otter/Fireflies settings > auto-join off; revoke their calendar access in Google
  (myaccount.google.com/connections) or Microsoft account app permissions if you never meant to grant it.

## Retention
- Delete transcripts and summaries after use; set org retention policies for recordings.
- Never feed transcripts with personal or client data into consumer AI chat tools.

## Verify
- [ ] Default host settings require approval for AI features; your calendar has no unwanted notetaker integration.
