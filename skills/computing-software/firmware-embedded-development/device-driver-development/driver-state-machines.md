---
id: computing-software.firmware-embedded-development.device-driver-development.driver-state-machines
name: driver-state-machines
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [driver-state-machine, interrupt-driven, non-blocking-driver, transaction-sequencing, busy-state, firmware-embedded-development]
level: advanced
status: draft
description: "Structure non-blocking drivers as explicit state machines driven by interrupts and timeouts: transaction phases, busy/idle ownership, error states, and re-entry protection."
sources:
  - https://www.state-machine.com/doc/AN_Crash_Course_in_UML_State_Machines.pdf
  - https://docs.zephyrproject.org/latest/kernel/drivers/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Driver state machines

A blocking sensor read is easy: write register, wait, read. A non-blocking one spans several
interrupts (address phase, data phase, conversion wait, readback). Without an explicit state
machine, drivers end up with tangled flags and race conditions.

## Example: sensor measurement over I2C with a conversion delay
```c
typedef enum { S_IDLE, S_TRIGGER, S_WAIT_CONV, S_READ, S_DONE, S_ERROR } st_t;

typedef struct {
    st_t st;
    uint8_t buf[6];
    void (*cb)(int err, const uint8_t *data, void *arg);
    void *arg;
} sensor_t;

int sensor_start(sensor_t *s, cb_t cb, void *arg) {
    if (s->st != S_IDLE) return -EBUSY;           /* ownership check */
    s->cb = cb; s->arg = arg;
    s->st = S_TRIGGER;
    return i2c_write_async(BUS, ADDR, cmd_trigger, 2, on_i2c_done, s);
}

static void on_i2c_done(int err, void *p) {        /* I2C ISR/callback context */
    sensor_t *s = p;
    if (err) { finish(s, err); return; }
    switch (s->st) {
    case S_TRIGGER:   s->st = S_WAIT_CONV; timer_start_oneshot(&s->tmr, 15, on_timer, s); break;
    case S_READ:      finish(s, 0); break;
    default:          finish(s, -EIO); break;     /* unexpected event in this state */
    }
}
static void on_timer(void *p) { sensor_t *s = p; s->st = S_READ; i2c_read_async(BUS, ADDR, s->buf, 6, on_i2c_done, s); }
static void finish(sensor_t *s, int err) { s->st = S_IDLE; s->cb(err, s->buf, s->arg); }
```

## Principles
- **One state variable** owns the driver's phase; every event handler switches on it and treats
  unexpected events as errors.
- **Return to IDLE before invoking the user callback**, so the callback may start the next
  operation.
- **Busy rejection** (`-EBUSY`) or a request queue: decide explicitly.
- **Timeouts are events too**: every waiting state has a timer that leads to an error path, so a
  missing interrupt never leaves the driver stuck.
- **Cancellation**: `sensor_abort()` must stop timers and the bus transfer and land in IDLE
  regardless of current state.
- **Concurrency**: state changes from ISR and thread contexts need a critical section, or funnel
  all events through one context (deferred work queue).
- Draw the state diagram in the driver's header comment; it is the spec.

## Verify
- [ ] Unit tests inject each event in each state (including unexpected ones) and check transitions.
- [ ] Fault injection (NACK, missing interrupt) always ends in IDLE with an error callback.
