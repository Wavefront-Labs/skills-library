---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-device-flow-polling
name: oauth-device-flow-polling
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-device-flow-polling, oauth-device-grant, authorization_pending, slow_down, expired_token, access_denied, polling, interval, identity-protocols]
level: practitioner
status: docs-checked
description: "Handle device grant token errors: authorization_pending, slow_down adds 5 seconds, access_denied, expired_token, and server-side rate limits."
sources:
  - https://www.rfc-editor.org/rfc/rfc8628
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Device flow polling errors and slow_down

Goal: poll politely and finish cleanly.

Rules:
- Wait `interval` seconds between requests (5 if absent).
- `authorization_pending`: keep polling at the same interval.
- `slow_down`: increase the interval by 5 seconds permanently, then continue.
- `access_denied`: user declined; stop.
- `expired_token`: the `device_code` expired and the session ended; the client may start a new request but should wait for user interaction first.
- Success returns the standard token response.

Server side: return `authorization_pending` until the user finishes and `slow_down` when the client should poll less often; any other error ends polling.

Gotchas:
- On a connection timeout the client MUST reduce its polling frequency; exponential backoff (for example doubling the interval) is RECOMMENDED.
- Any error other than `authorization_pending` and `slow_down` means stop polling.

Verify: run the flow and check that polling waits at least `interval` seconds and that the interval grows by 5 seconds after `slow_down`.

## Checked

2026-11-02. Confirmed against RFC 8628 section 3.5 (5 second default, `authorization_pending`, `slow_down` adds 5 seconds to all later requests, `access_denied`, `expired_token`, stop on other errors, timeout backoff). Removed: server-side binding, 10-15 minute expiry and single-use statements, the jitter advice and the UI timer advice (not in the RFC).
Method: documentation only; no commands were run.
