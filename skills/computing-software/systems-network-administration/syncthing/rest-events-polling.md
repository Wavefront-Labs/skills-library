---
id: computing-software.systems-network-administration.syncthing.rest-events-polling
name: rest-events-polling
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, rest-events, event-api, long-polling]
level: advanced
status: docs-checked
description: "Poll Syncthing events through GET /rest/events with since, limit, timeout and events filters without missing items."
sources: ["https://docs.syncthing.net/rest/events-get.html", "https://docs.syncthing.net/events/itemfinished.html", "https://docs.syncthing.net/events/statechanged.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Polling /rest/events

## Request
`GET /rest/events` returns a JSON array of event objects starting at the event just after the last seen ID given in `since` (default 0, which returns all events).

Parameters:
- `events=EventTypeA,EventTypeB` filters to chosen types. Without a filter, all events except `LocalChangeDetected` and `RemoteChangeDetected` are included.
- `limit=<n>` returns only the last n events. `/rest/events?since=0&limit=1` catches up with the latest event ID after a disconnection.
- `timeout=<seconds>` customizes the wait. By default the call times out after 60 seconds, returning an empty array.

`GET /rest/events/disk` is the same stream pre-filtered to only `LocalChangeDetected` and `RemoteChangeDetected`; the `events` parameter is not used.

## Blocking behaviour
If no new events have been produced since the last seen ID, the call blocks and waits for new events before returning. If the ID is a future ID, it blocks until that ID is reached or it times out.

## Loop pattern
```sh
last=0
while true; do
  out=$(curl -s -H "X-API-Key: <key>" "http://127.0.0.1:8384/rest/events?since=$last&events=ItemFinished,StateChanged")
  # parse out, set last to the highest id seen
done
```

## Lost events
The number of buffered events is limited, so if events arrive at a high rate or the time between polls is long, some may be missed. This can be detected as a discontinuity in the event IDs.

## Useful events
`StateChanged` is emitted when a folder changes state (`idle`, `scanning`, `syncing`, `error`); `duration` is the number of seconds spent in the `from` state. `ItemFinished` is generated when Syncthing ends synchronizing a file to a newer version; its data has `item`, `folder`, `error`, `type` and `action`.

## Checked
2026-11-04. Read GET /rest/events, ItemFinished and StateChanged: parameters and defaults, the default filter, blocking and timeout behaviour, the disk endpoint, buffer limits and the event fields. Removed the `StartupComplete` claim and the advice to catch up from the db endpoints, which the pages do not state. The shell loop is an illustration only.
Method: documentation only; no commands were run.
