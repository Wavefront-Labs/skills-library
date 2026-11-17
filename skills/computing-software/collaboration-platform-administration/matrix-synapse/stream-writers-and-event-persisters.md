---
id: computing-software.collaboration-platform-administration.matrix-synapse.stream-writers-and-event-persisters
name: stream-writers-and-event-persisters
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, workers, stream-writers, event-persister, event-creator, typing, receipts, presence, device-lists]
level: sme
status: docs-checked
description: "Move Synapse stream writing off the main process with stream_writers: requirements, event persisters sharded by room, and endpoints per stream."
sources:
  - https://element-hq.github.io/synapse/latest/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Writing of specific streams, such as events, can be moved from the main process to a named worker. That worker needs an HTTP `replication` listener, a `worker_name` listed in `instance_map`, and the main process must also be in `instance_map`. One worker may handle several streams, but unless documented otherwise each stream has a single writer.

```yaml
instance_map:
    main:
        host: localhost
        port: 8030
    event_persister1:
        host: localhost
        port: 8034

stream_writers:
    events: event_persister1
```

**events.** This stream experimentally supports multiple writers, sharded by room ID, each called an event persister. A persister receives new events, links them into the room DAG, persists them and updates the stream. Because of the sharding you must restart all worker instances when adding or removing persisters. Multiple writers are given as a list (`event_persister1`, `event_persister2`). Do not confuse a persister with an `event_creator`, which takes client requests to create events and passes them over HTTP replication to persisters (or the main process); both are plain `synapse.app.generic_worker`.

Endpoints to route straight to the stream's writer, per the docs:

- `typing`: `^/_matrix/client/(api/v1|r0|v3|unstable)/rooms/.*/typing`
- `to_device`: `.../sendToDevice/`
- `account_data`: `.../.*/tags` and `.../.*/account_data`
- `receipts` (multiple writers allowed): `.../rooms/.*/receipt` and `.../read_markers`
- `presence`: `.../presence/`
- `push_rules`: `.../pushrules/`
- `device_lists` (multiple writers allowed): `delete_devices`, `devices`, `keys/upload`, `keys/device_signing/upload`, `keys/signatures/upload`
- `quarantined_media_changes` (multiple writers allowed): the media quarantine admin endpoints under `/_synapse/admin/v1/`. The writer must also be able to run the media repository, since those endpoints exist only on media-capable workers.

## Checked

Method: docs-checked 2026-11-09 against docs/workers.md (Synapse develop branch, raw markdown, read in full).
