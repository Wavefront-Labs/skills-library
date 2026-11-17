---
id: computing-software.firmware-embedded-development.zephyr.zbus-publish-subscribe
name: zbus-publish-subscribe
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-data-passing, zbus, zbus-chan-define, zbus-listener, zbus-subscriber, msg-subscriber, zbus-chan-pub, decoupled-modules, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Decouple Zephyr application modules with zbus channels: define channels, choose listeners vs subscribers vs message subscribers, and avoid lost or late messages."
sources:
  - https://docs.zephyrproject.org/latest/services/zbus/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zbus publish/subscribe

**Goal:** modules (sensors, UI, cloud uplink, storage) communicate through typed channels
instead of calling each other directly, so they can be added, removed and tested alone.

## Channel definition
```c
struct acc_msg { int16_t x, y, z; };

ZBUS_CHAN_DEFINE(acc_chan,              /* name */
    struct acc_msg,                     /* message type */
    NULL,                               /* validator (optional) */
    NULL,                               /* user data */
    ZBUS_OBSERVERS(logger_lis, uplink_sub),  /* static observers */
    ZBUS_MSG_INIT(.x = 0, .y = 0, .z = 0));
```
The channel holds **one** current message (the latest). Publish and read lock the channel, copy the
message to or from shared memory and unlock; with `CONFIG_ZBUS_PRIORITY_BOOST` (default on) the lock is a
Highest Locker Protocol implementation, otherwise plain semaphores are used.
`prj.conf`: `CONFIG_ZBUS=y` (+ `CONFIG_ZBUS_MSG_SUBSCRIBER=y` for message subscribers,
`CONFIG_ZBUS_ASYNC_LISTENER=y` for async listeners, `CONFIG_ZBUS_RUNTIME_OBSERVERS=y` for runtime add).

## Publishing and reading
```c
struct acc_msg m = { .x = 1, .y = 2, .z = 3 };
zbus_chan_pub(&acc_chan, &m, K_MSEC(10));   /* lock, copy in, notify observers, unlock (stack messages are fine) */
struct acc_msg cur;
zbus_chan_read(&acc_chan, &cur, K_MSEC(10));
```

## Observer types
| Type | Runs | Gets | Risk |
|---|---|---|---|
| Listener (`ZBUS_LISTENER_DEFINE`) | synchronously in the publisher's context (thread or ISR), channel locked | reads the channel directly (`zbus_chan_const_msg`) | slow callback blocks every publisher |
| Async listener (`ZBUS_ASYNC_LISTENER_DEFINE`, needs `CONFIG_ZBUS_ASYNC_LISTENER`) | in a work queue (system workqueue by default) | a copy of the message | needs buffers like message subscribers |
| Subscriber (`ZBUS_SUBSCRIBER_DEFINE(name, queue_size)`) | its own thread waits with `zbus_sub_wait` | a **channel reference**, must then read | may read a **newer** value than the one that triggered it (intermediate values lost) |
| Message subscriber (`ZBUS_MSG_SUBSCRIBER_DEFINE(name)`) | own thread, `zbus_sub_wait_msg` | a **copy** of each published message (from a net_buf pool) | memory per in-flight message; pool exhaustion |
Pick message subscribers when every sample matters (logging, uplink), plain subscribers when
"latest state" is enough (UI), listeners only for tiny, non-blocking reactions.

## Gotchas
- zbus operations work in ISRs, but only with a `K_NO_WAIT` timeout, and the docs warn that the scheduler
  will not preempt the event dispatcher while it runs in an ISR: keep ISR publications small.
- Size subscriber queues for bursts: a plain subscriber's queue holds channel references, not messages.
- Message subscribers and async listeners draw from a net_buf pool: tune
  `CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_SIZE` and `CONFIG_HEAP_MEM_POOL_ADD_SIZE_ZBUS`; the docs call them
  crucial to delivery guarantees. `CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_ISOLATION` gives a channel set its own pool.
- A channel validator rejects bad messages at publish time: use it to enforce ranges.
- Priority boost (`CONFIG_ZBUS_PRIORITY_BOOST`, default on) temporarily raises the publisher to the Highest
  Observer Priority of the channel (runtime observers are not considered); understand it before tuning thread
  priorities, or disable it to use plain semaphores as the channel lock.

## Verify
- [ ] Publish 1000 messages quickly: message subscriber receives 1000, plain subscriber may
      see fewer (expected).
- [ ] Removing one module still builds and runs the rest (decoupling achieved).

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Observer types (listener, async listener, subscriber, message subscriber), publisher-context dispatch, ISR rule
  (`K_NO_WAIT` only), priority boost default and meaning, net_buf pool options, Kconfig names `CONFIG_ZBUS`,
  `CONFIG_ZBUS_MSG_SUBSCRIBER`, `CONFIG_ZBUS_ASYNC_LISTENER`, `CONFIG_ZBUS_RUNTIME_OBSERVERS`, macro signatures
  (doc: services/zbus/index).
- Wrong in the draft: "Publishing from an ISR isn't allowed" (the docs allow zbus operations in ISRs with K_NO_WAIT);
  the "queue full: notifications dropped, publish may time out" claim was removed (not documented); async listeners were
  missing from the observer table.

Method: documentation only; no commands were run.
