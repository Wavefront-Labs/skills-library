---
id: computing-software.cybersecurity-defensive.pomerium.session-recording-limits-and-tuning
name: session-recording-limits-and-tuning
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [recording-limitations, session-recording-concurrency, pipe-max-size, querier-cache, asciicast]
level: advanced
status: docs-checked
description: "Know what Pomerium SSH recordings capture and omit, memory limits, upload concurrency and pipe tuning, metadata cache, and how to disable recording."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/session-recording.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Contents and limits**
- Recordings hold raw PTY data from upstream to client plus terminal resize events.
- Client keystrokes are not recorded; input the server does not echo (passwords) is missing.
- Only interactive shells are recorded, not direct commands or file transfers.
- No compression. Pomerium does not encrypt recordings; use the object store's encryption.

**Memory**: data is buffered in memory only, never on disk, up to roughly 10-12 MB per active recording. At the limit the connection may pause; if the buffer stays full for a few seconds the session is force-closed (only that session).

**Upload tuning**
- `session_recording_concurrency`: Envoy worker pool, default 2, silently lowered to the worker thread count.
- Upload pipes are resized to 4 MiB if the kernel allows, otherwise to `fs.pipe-max-size` (usually 1 MiB). Processes with `CAP_SYS_RESOURCE` get 4 MiB. Raise `fs.pipe-max-size` for large recordings.

**Access tuning**: enable the metadata cache with `--enable-session-recording-querier-cache=true --cache-dir=/path/to/cache` (or `enable_session_recording_querier_cache: true` and `cache_dir`). Without `cache_dir` it is memory only. For very large volumes rotate buckets.

**Playback**: files are `<recording-id>.asciicast.json`, playable with `asciinema play`.

**Disable**: set `session_recording.enabled = false` or remove the block; existing recordings stay. To remove the extension, disable on all routes, remove the mount, then remove the `envoy_dynamic_extensions` path.

## Checked

2026-11-04. Read the SSH Session Recording page: recording contents and limitations, 10-12 MB buffer and pause behaviour, session_recording_concurrency default, pipe sizing, querier cache flags, asciicast download format, and disable and removal steps all confirmed. Nothing removed.

Method: documentation only; no commands were run.
