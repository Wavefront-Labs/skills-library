---
id: computing-software.cybersecurity-defensive.zeek.functions-hooks-events
name: functions-hooks-events
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, callables, event-handler, hook, schedule]
level: practitioner
status: docs-checked
description: "Compare Zeek functions, hooks and events: immediate versus queued calls, priorities, multiple bodies, scheduling, defaults, return values."
sources: ["https://docs.zeek.org/en/current/reference/zeekscript/statements.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# functions, hooks and events

Comparison from the statements page:

- **Anonymous (lambda)**: functions yes; hooks and events no.
- **Multiple bodies and priorities**: hooks and events yes; functions no.
- **Immediate invocation**: functions and hooks yes. Events are pushed onto the event queue and handled as time passes.
- **Scheduling**: events only. Scheduling a function or hook gives the syntax error "function invoked as an event".
- **Default arguments**: all three.
- **Alternate prototype declarations** (overloading with different argument sets): hooks and events yes, functions no.

Mutation: container arguments (records, tables) are passed by reference, atomic types by value, so changes inside persist. Asynchronous functions are the exception: `when` statements call them with copies, so changes are lost.

Return values: functions must return a value, and with no explicit return type they implicitly return void (not a valid Zeek type). A hook may return a `bool` or void, and may return before it breaks. Events cannot return a value because no caller waits.

Handler order uses `&priority` (default 0):

```
event zeek_init() &priority=10
    {
    print "high priority";
    }
```

Statements outside callables must follow all global declarations and end with a semicolon, with a few exceptions.

## Checked

2026-11-08. Read the Declarations and Statements page in full; removed the higher-first ordering claim, which that page does not state.

Method: documentation only; no commands were run.
