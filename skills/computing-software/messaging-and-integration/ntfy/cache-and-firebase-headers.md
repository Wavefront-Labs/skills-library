---
id: computing-software.messaging-and-integration.ntfy.cache-and-firebase-headers
name: cache-and-firebase-headers
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, cache, firebase, x-cache, x-firebase]
level: practitioner
status: docs-checked
description: "Opt individual ntfy messages out of the server cache or Firebase forwarding with X-Cache: no and X-Firebase: no, and the delivery trade-offs."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-message cache and Firebase opt-out

## Message caching

Messages are cached on the server for 12 hours by default. Send `X-Cache: no` (alias `Cache: no`) to skip storage.

```
curl -H "Cache: no" -d "This message won't be stored server-side" ntfy.sh/mytopic
```

- Connected subscribers still receive it.
- `since=` and `poll=1` will not return it.
- Subscribers that reconnect or are briefly disconnected can miss it, because it is not re-delivered.

## Disable Firebase

`X-Firebase: no` (alias `Firebase: no`) stops forwarding to FCM. ntfy.sh forwards all messages to FCM by default.

```
curl -H "Firebase: no" -d "Not via Firebase" ntfy.sh/mytopic
```

Gotcha: without instant delivery enabled in the Android app (Google Play variant), delivery can be delayed by up to 15 minutes.

## Related

UnifiedPush senders use `X-UnifiedPush: 1`, which is mostly equivalent to `Firebase: no`.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Message caching, Disable Firebase, UnifiedPush): 12-hour default, header names and aliases, since/poll behaviour, missed-message warning, 15-minute delay warning, ntfy.sh forwarding to FCM, `X-UnifiedPush` equivalence. Removed: the `expires` claim and the Verify step.
Method: documentation only; no commands were run.
