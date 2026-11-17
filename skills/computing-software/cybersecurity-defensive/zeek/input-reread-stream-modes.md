---
id: computing-software.cybersecurity-defensive.zeek.input-reread-stream-modes
name: input-reread-stream-modes
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, input-reread, stream-mode, predicate-filter, force-update]
level: advanced
status: docs-checked
description: "Keep input data fresh: Input::force_update, MANUAL, REREAD and STREAM modes, change events with $ev, predicate functions that veto or alter entries, and error reporting."
sources: ["https://docs.zeek.org/en/current/frameworks/input.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# input reread and stream modes

**Manual refresh**: while a stream is open, `Input::force_update("denylist")` refreshes the whole table: changed elements updated, new ones added, absent ones removed, then `Input::end_of_data` fires.

**Automatic**: set `$mode` in `Input::add_table` to `Input::MANUAL` (default), `Input::REREAD` or `Input::STREAM`. REREAD re-reads a changed file and raises `Input::end_of_data` each time. STREAM treats the file as append-only, follows rotation by inode change, overwrites rows with the same index, and never raises `Input::end_of_data`. Change detection uses heartbeats, by default once per second (`Threading::heartbeat_interval`), and checks inode or modification time.

**Change events**: pass `$ev=entry` with signature `event entry(description: Input::TableDescription, tpe: Input::Event, left: Idx, right: Val)`. `tpe` is `Input::EVENT_NEW`, `EVENT_CHANGED` (right holds the values before the change) or `EVENT_REMOVED`.

**Predicates**: `$pred(tpe: Input::Event, left: Idx, right: Val) = { ... }` runs before a change is committed. Return T to accept, F to veto; it may modify `left` and `right`. The destination still has old values at that point.

**Errors**: problems appear in `reporter.log` and via the `$error_ev` member of `Input::TableDescription` and `Input::EventDescription`. Repeated messages for the same file are suppressed. The ASCII reader has `InputAscii::fail_on_invalid_lines` for coarse robustness control.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
