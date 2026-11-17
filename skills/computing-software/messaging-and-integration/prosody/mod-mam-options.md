---
id: computing-software.messaging-and-integration.prosody.mod-mam-options
name: mod-mam-options
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, mam, xep-0313, archive, retention, modules]
level: practitioner
status: docs-checked
description: "mod_mam message archive options in Prosody: archive_expires_after 1w, default_archive_policy, cleanup interval, query page size, and which namespaces are skipped."
sources:
  - https://prosody.im/doc/modules/mod_mam
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_mam options

Stores per-user archives (XEP-0313) so clients can sync history for offline periods. Enable with `"mam"` in `modules_enabled`.

| Option | Default |
|---|---|
| `archive_expires_after` | `"1w"` |
| `default_archive_policy` | `true` (all); `false` none; `"roster"` contacts only |
| `archive_cleanup_interval` | `4*60*60` seconds |
| `max_archive_query_results` | `50` |
| `dont_archive_namespaces` | chatstates namespace |
| `mam_smart_enable` | `false` (archive only after user queries or sets preferences) |

Expiry accepts seconds, suffixed strings (`"1d"`, `"1w"`, `"2mon"`, `"1y"`) or `"never"`.

```lua
archive_expires_after = "1w"
max_archive_query_results = 20
```

Large page sizes are discouraged because Prosody blocks while processing a request. Online sync between clients is mod_carbons, not mod_mam.

Verify: a client's MAM query returns at most `max_archive_query_results` items per page and messages older than the expiry disappear after a cleanup run.

## Checked

2026-11-04. Read the mod_mam page: archive_expires_after "1w" with seconds, d, w, mon, y suffixes and "never", default_archive_policy true, false and "roster", archive_cleanup_interval 4*60*60, max_archive_query_results 50, dont_archive_namespaces with the chatstates namespace, mam_smart_enable false, the warning about large page sizes, and mod_carbons for online sync all match. Nothing removed.

Method: documentation only; no commands were run.
