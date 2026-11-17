---
id: computing-software.messaging-and-integration.prosody.mod-tombstones
name: mod-tombstones
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, tombstones, account-deletion, security]
level: practitioner
status: docs-checked
description: "mod_tombstones in Prosody: keep a record of deleted accounts so contacts are aware and left-over privileges cannot be abused; user_tombstone_expiry defaults to forever."
sources:
  - https://prosody.im/doc/modules/mod_tombstones
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_tombstones

Keeps a record of accounts that have been removed, to ensure former contacts are aware and to prevent any left-over privileges from being abused.

Enable with `"tombstones";` in `modules_enabled`.

Configuration: `user_tombstone_expiry` is how long to keep tombstones around. It defaults to forever. The page gives no value format, so check the format before using a number.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_tombstones (purpose and user_tombstone_expiry default). Removed the claim that re-registering a name is refused and the `prosodyctl deluser` verify line, which the page does not state.
Method: documentation only; no commands were run.
