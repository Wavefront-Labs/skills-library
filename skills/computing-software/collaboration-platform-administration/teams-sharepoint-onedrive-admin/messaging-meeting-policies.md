---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.messaging-meeting-policies
name: messaging-meeting-policies
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [messaging-meeting-policies]
level: practitioner
status: draft
description: Tune chat, delete/edit, external access and meeting recording options through policies.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Messaging and meeting policies
**Goal:** Tune chat, delete/edit, external access and meeting recording options through policies.

- TeamsMessagingPolicy: owner delete, read receipts, Giphy rating, chat translation.
- TeamsMeetingPolicy: who can bypass lobby, recording, transcription, anonymous join.
- Create a custom policy and assign it to pilot users first.
- Use `Set-CsTeamsMeetingPolicy` for scripted changes.

## Gotchas
- Meeting options set by organisers can't exceed the policy.
- Recording storage is OneDrive/SharePoint, so governance follows those.

## Self-check
Pilot user sees the changed option in a new meeting.
