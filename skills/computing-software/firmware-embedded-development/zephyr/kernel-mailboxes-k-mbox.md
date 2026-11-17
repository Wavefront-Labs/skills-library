---
id: computing-software.firmware-embedded-development.zephyr.kernel-mailboxes-k-mbox
name: kernel-mailboxes-k-mbox
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [k-mbox, k-mbox-put, k-mbox-get, synchronous-message, targeted-message, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Exchange messages with Zephyr mailboxes (k_mbox): synchronous and asynchronous send, targeting a specific receiver thread, message info/data split, and deferred data retrieval."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/data_passing/mailboxes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mailboxes (k_mbox)

A mailbox passes messages between **threads** (not ISRs) with features message queues lack:
sender/receiver targeting, variable-size data, synchronous handshake, and an info word.

```c
K_MBOX_DEFINE(cmd_mbox);
```

## Synchronous send (sender waits until received)
```c
void producer(void) {
    struct k_mbox_msg msg = {
        .info = CMD_SET_RATE,          /* 32-bit app value, exchanged both ways */
        .size = sizeof(rate),
        .tx_data = &rate,
        .tx_target_thread = K_ANY,     /* or a specific k_tid_t */
    };
    if (k_mbox_put(&cmd_mbox, &msg, K_MSEC(100)) == 0) {
        /* receiver has consumed it; msg.info now holds the receiver's reply info,
           msg.size the number of bytes it actually took */
    }
}
```

## Receive
```c
void consumer(void) {
    uint8_t buf[32];
    struct k_mbox_msg rx = {
        .size = sizeof buf,               /* max we accept */
        .rx_source_thread = K_ANY,        /* or only from a specific thread */
    };
    k_mbox_get(&cmd_mbox, &rx, buf, K_FOREVER);
    /* rx.info = sender's info, rx.size = bytes received (truncated if larger than buf) */
}
```
Passing `NULL` as the buffer defers retrieval: inspect `rx.info`/`rx.size`, then call
`k_mbox_data_get(&rx, buf)` (or `NULL` to discard). A synchronous sender stays blocked until the
data is retrieved or discarded.

## Asynchronous send
```c
static K_SEM_DEFINE(done, 0, 1);
k_mbox_async_put(&cmd_mbox, &msg, &done);   /* returns immediately; done given on consumption */
```
Requires `CONFIG_NUM_MBOX_ASYNC_MSGS` > 0 (default 10, shared by all mailboxes; 0 disables
asynchronous messages). The tx buffer must remain valid until the semaphore
is given.

## When to use
- Targeted delivery between specific threads sharing one channel.
- Request/response where the sender needs to know the request was taken (synchronous put).
- Otherwise prefer `k_msgq` (simpler, ISR-safe) or zbus for many-to-many.

## Gotchas
- Mailboxes are for threads only; ISRs cannot exchange messages.
- `k_mbox_put` returns 0, `-ENOMSG` (no wait, no receiver) or `-EAGAIN` (timeout); the mailbox
  updates `size` with the number of data bytes actually exchanged, so check it on both sides.
- A message is owned by the mailbox until it is given to a receiver, and a synchronous sender
  blocks until the message is fully processed, so its stack buffer stays valid. An asynchronous
  sender's buffer must outlive the exchange.

## Verify
- [ ] Async senders keep tx data alive until their semaphore fires.
- [ ] Receivers check `rx.size` and handle truncation.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Threads only, K_ANY targeting, info and size fields, deferred data retrieval, `k_mbox_data_get` (doc:
  kernel/services/data_passing/mailboxes; `kernel.h`).
- `CONFIG_NUM_MBOX_ASYNC_MSGS` default and meaning (`kernel/Kconfig`); `k_mbox_put` return codes.
- Removed: the truncation and "directly copied" statements the docs do not make.

Method: documentation only; no commands were run.
