---
id: computing-software.networking-hardware-and-wireless.asterisk.queue-log-events
name: queue-log-events
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, queues, queue-log, queue-log-events, reporting, abandon, connect, ringnoanswer]
level: practitioner
status: docs-checked
description: "Read the Asterisk queue_log file: pipe-delimited fields, key event types (ENTERQUEUE, CONNECT, COMPLETEAGENT, ABANDON, RINGNOANSWER, transfers) and queues.conf logging options."
sources:
  - https://docs.asterisk.org/Operation/Logging/Queue-Logs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# queue log events
Queue logs record call setup and teardown in more detail than CDRs. Lines in `queue_log` are pipe-delimited: UNIX timestamp, a unique ID of the caller channel (or `REALTIME` or `NONE`), queue name, member channel, event type, then event parameters. Example shape: `1366720340|1366720340.303267|MYQUEUE|SIP/8007|RINGNOANSWER|1000`.

Selected events (parameters in order):
- `ENTERQUEUE(url|callerid|origposition[|calleridname])`; `CONNECT(holdtime|bridgedchanneluniqueid|ringtime)`.
- `COMPLETEAGENT` and `COMPLETECALLER (holdtime|calltime|origposition)`: who ended the call.
- `ABANDON(position|origposition|waittime)`; `EXITEMPTY`; `EXITWITHKEY(key|...)`; `EXITWITHTIMEOUT`.
- `RINGNOANSWER(ringtime)` (ms before the attempt ended); `RINGCANCELED`.
- `BLINDTRANSFER(extension|context|holdtime|calltime|origposition)`, `ATTENDEDTRANSFER(method|method-data|...)` (added in 12), `TRANSFER`.
- Membership: `ADDMEMBER`, `REMOVEMEMBER`, `AGENTLOGIN`, `AGENTLOGOFF(channel|logintime)`, callback-agent variants.
- Housekeeping: `CONFIGRELOAD`, `QUEUESTART`, `SYSCOMPAT`, `AGENTDUMP`.

Logging options such as `log_membername_as_agent` are in `queues.conf`; see the sample file.

## Checked
2026-11-09: read the cited Queue Logs page in full and confirmed the field order, the example line, the event names and their parameters, the added-in-12 notes and the queues.conf option pointer. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
