---
id: computing-software.firmware-embedded-development.freertos.gatekeeper-tasks
name: gatekeeper-tasks
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [gatekeeper-task, resource-ownership, request-queue, serialised-access, mutex-free-design, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Give one FreeRTOS task sole ownership of a shared resource (UART console, I2C bus, flash) and serialise access through a request queue instead of a mutex."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch08.md
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/queue.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gatekeeper tasks

**Idea:** only the gatekeeper ever touches the resource. Everyone else sends it a request.
The Kernel Book presents this as mutual exclusion without the risk of priority inversion or
deadlock, and interrupts can submit requests with `FromISR` calls, which they can't do with a
mutex.

## Console gatekeeper (after the Mastering the FreeRTOS Kernel example)
```c
typedef struct { char text[64]; } log_msg_t;
static QueueHandle_t log_q;

static void log_gatekeeper(void *arg) {
    log_msg_t m;
    for (;;) {
        xQueueReceive(log_q, &m, portMAX_DELAY);
        uart_write_blocking(m.text, strnlen(m.text, sizeof m.text));  /* sole UART user */
    }
}
void log_init(void) {
    log_q = xQueueCreate(16, sizeof(log_msg_t));
    xTaskCreate(log_gatekeeper, "log", 512, NULL, tskIDLE_PRIORITY + 1, NULL);
}
bool log_post(const char *s) {                       /* any task */
    log_msg_t m; strlcpy(m.text, s, sizeof m.text);
    return xQueueSend(log_q, &m, 0) == pdTRUE;       /* drop rather than block callers */
}
```
A tick hook (`configUSE_TICK_HOOK 1`) or an ISR can post with `xQueueSendFromISR`.

## Request/response gatekeeper (bus with results)
For an I2C bus where callers need the result, put a reply channel in the request:
```c
typedef struct { uint8_t addr, reg; uint8_t *buf; size_t n;
                 TaskHandle_t caller; int status; } i2c_req_t;
/* caller: send &req (pointer queue), then ulTaskNotifyTake(pdTRUE, timeout) */
/* gatekeeper: do transfer, req->status = rc; xTaskNotifyGive(req->caller); */
```
Passing a pointer avoids copying buffers. The caller's request must stay valid until
notified, so keep it on the caller's stack and wait with a timeout.

## Design choices
- **Priority:** low for logging, so it only drains when there is spare CPU and the queue
  absorbs bursts. Higher than every client when latency matters (bus access), so a request is
  served as soon as it's posted.
- **Queue depth:** worst-case burst between gatekeeper runs. Decide the full-queue policy
  (drop and count, or block with timeout) per caller class.
- **Copy cost:** the queue copies items. Large payloads go by pointer to a pool buffer.
- **Ordering:** FIFO by default; `xQueueSendToFront` for urgent requests.

## When a mutex is better
Very short accesses (a few register writes) where the context switch to the gatekeeper costs
more than the access. Gatekeepers suit slow, blocking or ISR-originated work.

## Verify
- [ ] grep: resource driver functions are called only from the gatekeeper's file.
- [ ] Dropped-request counter exposed; zero under nominal load.
- [ ] Callers waiting for responses use timeouts and handle gatekeeper failure.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: Gatekeeper tasks give mutual exclusion without priority inversion or deadlock risk, and the book example posts from a tick hook (Kernel Book 8.4); xQueueSendToFront exists for urgent items (queue.h); ulTaskNotifyTake/xTaskNotifyGive pairing (task.h). 
Method: documentation only; no commands were run.
