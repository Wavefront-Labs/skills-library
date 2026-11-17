---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.capturing-user-reproductions
name: capturing-user-reproductions
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, evidence-gathering, repro-capture, screen-recording, snipping-tool-recording, steps-recorder, problem-steps-recorder, har-file, timestamps, reproduce-issue]
level: intro
status: draft
description: "Get evidence of intermittent problems from users: screen recordings (Snipping Tool, macOS, phones), HAR files for web apps, timestamps, and Steps Recorder alternatives."
sources:
  - "https://support.microsoft.com/en-us/windows"
  - "https://learn.microsoft.com/en-us/azure/azure-portal/capture-browser-trace"
  - "https://support.apple.com/guide/mac-help/welcome/mac"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# capturing-user-reproductions

Goal: see exactly what the user sees when the problem happens — especially
when it never happens while you're watching.

## Ask for a recording
- **Windows 11 Snipping Tool**: Win+Shift+S → Record (or Snipping Tool →
  Record), select area, Start; saves MP4. Include the clock in the area for
  timestamps.
- **Steps Recorder (psr.exe)** is deprecated and being removed from Windows
  11 — use screen recordings instead; on older builds `psr` still produces a
  zip of screenshots with clicks.
- **macOS**: Cmd+Shift+5 → Record selected portion.
- **Phones**: built-in screen recording (iOS Control Centre, Android quick
  settings).
- **Teams**: user shares screen during a call and you record (with consent,
  per policy).

## Web app failures: HAR file
Browser DevTools (F12) → Network → tick "Preserve log" → reproduce →
right-click → **Save all as HAR**. Contains request/response details,
status codes, timing — vendors ask for it.
**HAR files include cookies and tokens** — tell users to send via the
ticket, not email; sanitise or use the browser's "export HAR (sanitized)"
option where available.

## Intermittent problems
- Ask the user to note **exact time** (and screenshot including the clock)
  each time it happens — then correlate with Event Viewer, sign-in logs,
  network monitoring.
- Leave a lightweight capture running if needed (Reliability Monitor
  already records crashes; Performance Monitor data collector for
  resource spikes).
- Teams/Office: Ctrl+Alt+Shift+1 (Teams) / app diagnostic logs at the
  moment of failure.

## Guidance to users
"Start recording, do what you normally do until the problem happens, stop,
attach to the ticket." Ask them to avoid showing confidential content, or
blur it.

## Gotchas
- Recordings and HARs may contain personal/confidential data — store in the
  ticket with restricted access, delete when done.
- Large video files exceed email limits — upload via portal/OneDrive link.

## Verify
Ticket has a recording or HAR with timestamps that correlates to log
entries, and the issue can now be reproduced or explained.
