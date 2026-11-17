---
id: computing-software.cybersecurity-defensive.zeek.signature-actions-and-file-magic
name: signature-actions-and-file-magic
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, signature-actions, custom-signature-event, file-magic, file-mime]
level: advanced
status: docs-checked
description: "Zeek signature actions (event, enable) with signature_match handlers, and file-magic and file-mime signatures for MIME identification."
sources: ["https://docs.zeek.org/en/current/frameworks/signatures.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# signature actions and file magic

**event action**: `event "Found root!"` raises `signature_match`:

```
event signature_match(state: signature_state, msg: string, data: string)
event signature_match(state: signature_state, msg: string, data: string, end_of_match: count)
```

`data` is the payload piece that led to the match (empty without content conditions). The `end_of_match` form is marked as added in 7.1; it is the length of matching data. If a match spans packets, `data` holds only the triggering packet's payload.

Custom event names (marked as added in 6.2): `event my_signature_match "Found root!"` raises `my_signature_match` with the same parameters. Omitting the string, `event found_root`, gives a handler without `msg`: `event found_root(state: signature_state, data: string)`. Matches for custom events do not appear in `signatures.log`.

**enable action**: `enable "http"` activates a protocol analyzer for the matching connection; used by dynamic protocol detection.

**File content signatures** identify MIME types independent of protocol, used by the files framework and the `file_magic` built-in function. Condition: `file-magic /<regex>/`, which applies to arbitrary data. Action: `file-mime <string> [, <integer>]`, a MIME type and optional signed strength; when several signatures match, the higher strength wins.

Troubleshooting: if an analyzer-specific condition never fires, check that analyzer's log for the connection. No entry there suggests the signature engine saw no application data.

## Checked

2026-11-08. Read the Signature Framework page in full; every claim confirmed.

Method: documentation only; no commands were run.
