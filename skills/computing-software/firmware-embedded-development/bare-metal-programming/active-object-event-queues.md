---
id: computing-software.firmware-embedded-development.bare-metal-programming.active-object-event-queues
name: active-object-event-queues
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [active-object, actor-model, event-queue, publish-subscribe, event-pool, qp-framework, run-to-completion, event-driven, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Structure firmware as active objects: private state machine plus event queue, direct post vs publish-subscribe, queue sizing, and no shared-state locking."
sources:
  - https://www.state-machine.com/active-object
  - https://github.com/QuantumLeaps/qpc/blob/master/include/qp.h
  - https://www.state-machine.com/doc/Samek0607.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active objects and event queues

**Goal:** components that own their data, communicate only by asynchronous events, and
therefore need no mutexes - the actor model applied to microcontrollers.

## The pattern
Per the Quantum Leaps active object page, an active object (AO) keeps its data private and
isolated, communicates with the rest of the system only through asynchronous events, and has
its own event queue. It handles events one at a time, to completion. Because its attributes
are private and only its own thread touches them, they need no mutex.
- Others never call its functions or touch its data; they post events.
- Never block inside an event handler.
- A shared resource can be given to a dedicated AO that acts as a broker for it, so callers
  send it requests instead of locking.

```c
/* producer (an ISR or another AO), QP/C macros from qp.h */
TempEvt *e = Q_NEW(TempEvt, TEMP_SIG);   /* event allocated by the framework */
e->celsius = adc_to_c(raw);
QACTIVE_POST(AO_Heater, &e->super, me);  /* (me_, e_, sender_) */
```

## Posting vs publishing
The `qp.h` header provides:
- **Direct post**: `QACTIVE_POST(me_, e_, sender_)` - producer knows the receiver.
- **LIFO post**: `QACTIVE_POST_LIFO(me_, e_)` - places the event at the front of the queue.
- **Publish-subscribe**: AOs call `QActive_subscribe`, and a producer calls
  `QACTIVE_PUBLISH(e_, sender_)` to multicast the event to all subscribers. Samek describes
  publish-subscribe as the Observer pattern, and states QP supports it.
- `QActive_getQueueMin` reports the queue's low-water mark, usable to check sizing.
- Dynamic events carry a pool number (the `poolNum_` field of `QEvt`).

## Queue sizing
Samek (Samek0607, reader-comment reply): event queues cost memory in the way stacks do, and in
real-time applications "overflowing a queue is as big a crime as overflowing a stack", so size
each queue adequately for worst-case bursts.

## Rules of thumb
- One AO per independent concern (comms, control loop, UI, storage).
- Split long work into steps driven by posted events.

## Verify
- [ ] No global variable is written by more than one AO.
- [ ] Queue low-water marks (`QActive_getQueueMin`) show headroom under stress test.
- [ ] Host test drives an AO by posting events and asserting on emitted events.

## Checked
Method: docs-checked 2026-11-09 against the Quantum Leaps active object page (state-machine.com/active-object), the QP/C `qp.h` header on GitHub (macro and function names above), and Samek0607.pdf (queue sizing reply, publish-subscribe reply).
Removed as unconfirmed: the claim that pool sizing follows burst size, reference-count recycling details, "const static signal-only events", assert-on-overflow advice, `QF_PUBLISH` (the header macro is `QACTIVE_PUBLISH`), the minimal ring-buffer framework design, the QP-nano lineage claim, and the Zephyr `k_msgq` suggestion. The QP/C landing page was not used.
