---
id: computing-software.cybersecurity-defensive.zeek.event-tracing
name: event-tracing
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, event-trace, replay, pcap-anonymisation, base-time]
level: advanced
status: docs-checked
description: "Record Zeek events to a replayable script with --event-trace or -E, edit it to anonymise a sensitive pcap, and know what the trace cannot capture."
sources: ["https://docs.zeek.org/en/current/reference/zeekscript/event-semantics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# event tracing

Record the events of a run (live or pcap) and replay them later without the traffic source.

```
zeek --event-trace=mytrace.zeek <traffic-option> <other-options> <scripts...>
zeek -E mytrace.zeek -r in.pcap
zeek <other-options> <scripts...> mytrace.zeek
```

Use `-i` or `-r` for the traffic source. A main use is turning a sensitive pcap into an editable, shareable reflection of the same activity: change addresses and strings in the generated script. It ends with a summary of constants that might be sensitive, and a global `__base_time` lets you shift most times while keeping relative offsets.

Limits stated on the page:

- Values of type opaque, file or any cannot be recreated. They appear as variables such as `__UNSUPPORTED21`, designed to cause syntax errors so you find them.
- Only events from traffic processing (after `network_time` is set) are traced; `zeek_init` and script-generated events are not.
- The trace is written on a clean exit. A crash gives no trace; ctrl-c exits cleanly.
- Changes scripts made to values in the original run are baked in on replay. Delete lines marked `# from script` if the replay scripts must react afresh.
- Some timers may behave differently on replay.

## Checked

2026-11-08. Read the Event Semantics page in full; every claim confirmed.

Method: documentation only; no commands were run.
