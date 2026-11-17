---
id: computing-software.rpa-and-low-code.uipath.uipath-json-http-request
name: uipath-json-http-request
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-json-http-request]
level: practitioner
status: draft
description: "Use HTTP Request and Deserialize JSON."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Call APIs and parse JSON
**Goal:** Use HTTP Request and Deserialize JSON.

- HTTP Request activity (method, headers, auth, body) then `Deserialize JSON` to JObject or typed object; access via `jobject("key").ToString`.
- Handle non-2xx status codes explicitly.
- Retry with exponential backoff.

## Gotchas
- Never log tokens or secrets.

## Self-check
Response parsed into variables with no null errors.
