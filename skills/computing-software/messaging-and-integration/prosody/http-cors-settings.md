---
id: computing-software.messaging-and-integration.prosody.http-cors-settings
name: http-cors-settings
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, http, cors, bosh, websocket]
level: practitioner
status: docs-checked
description: "Prosody HTTP CORS options: access_control_allow_* defaults, access_control_max_age 7200, and disabling CORS per module with http_cors_override."
sources:
  - https://prosody.im/doc/http
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP CORS settings

Global-section options and defaults:

- `access_control_allow_methods`: GET, OPTIONS
- `access_control_allow_headers`: Content-Type
- `access_control_allow_credentials`: false
- `access_control_allow_origins`: all origins
- `access_control_max_age`: 7200 seconds

Override per module with `http_cors_override`, for example turning CORS off for BOSH and WebSocket:

```lua
http_cors_override = {
    bosh = { enabled = false; };
    websocket = { enabled = false; };
}
```

mod_bosh and mod_websocket allow cross-domain requests by default, so web clients on other origins work unless you restrict this.

Verify: an OPTIONS request from a disallowed origin to the module URL returns no CORS headers.

## Checked

2026-11-04. Read the Prosody HTTP server page: the five access_control_* options with defaults (GET and OPTIONS, Content-Type, false, all origins, 7200), http_cors_override with the bosh and websocket example, and CORS added automatically for BOSH, websockets and file transfer all match. Nothing removed.

Method: documentation only; no commands were run.
