---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.teams-and-slack-desktop-client-artefacts
name: teams-and-slack-desktop-client-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [teams-forensics, user-activity-artefacts, messaging-app-forensics, dfir, leveldb]
level: advanced
status: draft
description: "Extract chat, call and file artefacts from Microsoft Teams (classic and new) and Slack desktop clients: LevelDB/IndexedDB stores, logs, cache and limits."
sources: ["https://learn.microsoft.com/en-us/microsoftteams/teams-client-system-requirements", "https://github.com/lxndrblz/forensicsim"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Teams and Slack desktop client artefacts

**Goal:** chat clients cache messages, contacts, files and call records locally. Server-side
exports (Purview, Slack Enterprise export) are authoritative, but local artefacts help when
exports are unavailable or messages were deleted.

## Microsoft Teams
| Client | Location | Storage |
|---|---|---|
| Classic (Electron, retired 2024) | `%APPDATA%\Microsoft\Teams\` | `IndexedDB\https_teams.microsoft.com_0.indexeddb.leveldb`, `Local Storage\leveldb`, `Cache`, `logs.txt` |
| New Teams (WebView2) | `%LOCALAPPDATA%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams\` | `EBWebView\WV2Profile_tfw\IndexedDB\...leveldb`, logs folder |
- Parse LevelDB with forensicsim (`ms_teams_parser.py`) or generic LevelDB tools: reconstructs
  messages (with deleted/edited versions when still in the log), contacts, call records, meeting info.
- Logs record presence changes, calls, and app events with timestamps.

## Slack
- `%APPDATA%\Slack\` (Windows), `~/Library/Application Support/Slack/` (macOS):
  `IndexedDB\https_app.slack.com_0.indexeddb.leveldb`, `Local Storage`, `Cache\Cache_Data`, `logs\`.
- `storage\root-state.json` lists workspaces and signed-in teams.
- Cached files and images in Cache; messages partly in IndexedDB.

## Approach
1. Collect the whole app data folder (raw copy; files are locked while running).
2. Parse LevelDB including `.log` and `.ldb` files; LevelDB keeps old values until compaction - deleted messages may survive.
3. Timeline the results with other user activity.

## Gotchas
- Local caches are partial: only conversations the client loaded.
- Schemas change with client updates; validate parsers against known test messages.
- Legal: chat content of other participants raises privacy issues; scope carefully.

## Verify
Recovered messages are matched to server-side exports where possible, and parser version is recorded.
