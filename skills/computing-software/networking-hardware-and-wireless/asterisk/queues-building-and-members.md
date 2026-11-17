---
id: computing-software.networking-hardware-and-wireless.asterisk.queues-building-and-members
name: queues-building-and-members
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, queues, app-queue, queues-conf, addqueuemember, removequeuemember, strategy, hints, penalty]
level: practitioner
status: docs-checked
description: "Build ACD call queues: queues.conf templates and options, hints for device state, queue add member and state_interface, Queue(), and AddQueueMember/RemoveQueueMember login logic."
sources:
  - https://docs.asterisk.org/Configuration/Applications/Asterisk-Queues/Building-Queues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# queues: building and members
The page is based on Asterisk 1.6.2 with chan_sip and describes one approach, with flat-file configuration.

- Device state: queue members are only avoided while in use if their state is tracked. Add hints (`exten => <name>,hint,<technology>/<name>`), reload the dialplan, and verify with `core show hints`. For chan_sip peers the page needed `callcounter=yes`.
- `queues.conf`: keep `[general]` defaults (the page uses `persistentmembers`, `autofill`, `monitor-type`, `shared_lastcall`) and define a template with options such as `musicclass`, `strategy=rrmemory`, `joinempty`, `leavewhenempty`, `ringinuse=no`; each queue (sales, support) applies it. Reload `app_queue.so` and check `queue show`.
- CLI membership: `queue add member <channel> to <queue> [[[penalty <penalty>] as <membername>] state_interface <interface>]` and `queue remove member`. `state_interface` matters when the member channel cannot report its own state.
- Callers enter with `Queue(queuename)`.
- Login/logout from a phone: dialplan using `AddQueueMember()` and `RemoveQueueMember()` that checks whether the caller device is already a member; queue names are mapped through `[globals]` variables like `QUEUE_<exten>`.

Pausing, rules and other app_queue features appear in the full page.

## Checked

2026-11-09. Confirmed against the Asterisk Building Queues page: Asterisk 1.6.2 basis, hints and core show hints, callcounter for chan_sip, queues.conf general options and template, app_queue reload, queue add member syntax and state_interface purpose, Queue(), AddQueueMember and RemoveQueueMember login logic and QUEUE_<exten> globals. Nothing changed.
Method: documentation only; no commands were run.
