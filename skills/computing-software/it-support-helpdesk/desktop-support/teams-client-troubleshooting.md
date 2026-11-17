---
id: computing-software.it-support-helpdesk.desktop-support.teams-client-troubleshooting
name: teams-client-troubleshooting
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, microsoft-365, m365-support, teams-troubleshooting, microsoft-teams, teams-cache, teams-audio-video, teams-sign-in, teams-presence, new-teams, call-quality-dashboard]
level: practitioner
status: draft
description: "Fix new Teams client problems: sign-in loops, clearing the cache, audio/camera device issues, presence stuck, meetings add-in missing in Outlook, and reading Call Quality data."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/microsoftteams/teams-administration/clear-teams-cache"
  - "https://learn.microsoft.com/en-us/microsoftteams/troubleshoot/teams-welcome"
  - "https://learn.microsoft.com/en-us/microsoftteams/quality-of-experience-review-guide"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# teams-client-troubleshooting

Goal: a working Teams client in one visit, and a call-quality answer based
on data rather than the user's memory of "it was choppy".

## Quick isolation
Does Teams on the web (teams.microsoft.com) or mobile work for the same user?
Yes → local client issue. No → account/licence/policy/service — check
Microsoft 365 Service health first.

## Clear the cache (new Teams)
Quit Teams fully (tray → Quit), then:
- Settings → Apps → Microsoft Teams → Advanced options → **Reset**, or
- delete `%LOCALAPPDATA%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams`.
Classic Teams (retired) used `%APPDATA%\Microsoft\Teams`.
Fixes: blank window, stale channels, wrong presence, sign-in loop.

## Sign-in problems
- Error codes like `caa20002`, `caa70004`: token/WAM issues — sign out of
  Windows "Work or school accounts" duplicates, clear cache, ensure time is
  correct.
- Conditional access block: sign-in logs in Entra (user → Sign-in logs →
  failure reason) give the actual policy.

## Audio and video
- Teams Settings → Devices: correct speaker/mic/camera; **make a test call**.
- Camera "in use by another app": close other conferencing apps; check
  Windows Privacy → Camera → allow desktop apps.
- Headset buttons/dock audio: update dock firmware and headset firmware;
  certified devices behave better.
- Echo: someone without headset in the meeting, not the reporter.

## Call quality evidence
Teams admin centre → Users → user → Meetings & calls → pick the call →
Advanced: network (jitter, packet loss, round-trip), device, Wi-Fi vs wired.
Patterns: packet loss > 1 % or jitter > 30 ms on Wi-Fi → Wi-Fi/home network;
VPN in path → split-tunnel Teams media (Microsoft 365 "Optimize" endpoints).
Call Quality Dashboard (CQD) for building-wide trends.

## Outlook meeting add-in missing
Teams Meeting Add-in in Outlook COM add-ins; re-register by restarting new
Teams (it installs the add-in), check it isn't in Disabled Items (Outlook →
Options → Add-ins → Manage Disabled Items).

## Gotchas
- Two Teams clients installed (classic + new) confuse protocol handlers and
  add-ins; remove classic via the Teams admin uninstall tooling.
- Presence stuck "Away" while active: Outlook calendar state or idle timer
  → cache reset usually clears it.

## Verify
Test call plays back clean audio, camera preview works, user can join a
scheduled meeting from Outlook, presence changes within a minute.
