---
id: computing-software.firmware-embedded-development.freertos.queue-registry-for-debuggers
name: queue-registry-for-debuggers
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [queue-registry, vqueueaddtoregistry, configqueue-registry-size, kernel-aware-debugging, named-queues, freertos, firmware-embedded-development]
level: practitioner
status: draft
description: "Name FreeRTOS queues, semaphores and mutexes in the queue registry so kernel-aware debuggers and trace tools show which object each blocked task waits on."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/17-vQueueAddToRegistry
  - https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Queue registry for debuggers

**Goal:** in the debugger's RTOS view, see `uart_rx (3/16)` and "task `net` blocked on
`tx_mutex`" instead of anonymous addresses.

## Enable and register
```c
/* FreeRTOSConfig.h */
#define configQUEUE_REGISTRY_SIZE  16      /* 0 = registry compiled out */

QueueHandle_t q = xQueueCreate(16, sizeof(msg_t));
vQueueAddToRegistry(q, "uart_rx");

SemaphoreHandle_t m = xSemaphoreCreateMutex();
vQueueAddToRegistry((QueueHandle_t)m, "tx_mutex");   /* semaphores are queues */
```
- The registry stores the **pointer** to the name, not a copy. Pass a string literal or
  static buffer, never a stack array.
- When full, further adds are silently ignored. Size it for every object you want to see.
- Call `vQueueUnregisterQueue(q)` before `vQueueDelete(q)`. Deleting first leaves a dangling
  entry that debuggers will dereference.
- `pcQueueGetName(q)` reads the name back, useful in your own logs and asserts.

## Who uses it
- IDE RTOS views: STM32CubeIDE, MCUXpresso, Segger Ozone, Cortex-Debug (VS Code), IAR and
  Keil RTOS plugins. They walk `xQueueRegistry[]`; unregistered queues are invisible or
  shown by address.
- Tracealyzer and SystemView label kernel objects with registry names (they also have their
  own naming calls such as `vTraceSetQueueName`; registry names work with both).
- OpenOCD `-rtos FreeRTOS` shows threads only, not queues.

## Production builds
Cost per entry is one pointer plus one handle (8 bytes on 32-bit) and a linear search on
add/remove. Most teams leave it on. To strip it, set `configQUEUE_REGISTRY_SIZE 0`; the calls
compile to nothing, so no `#ifdef`s are needed at call sites.

## Convention
Register right after creation, inside the module that owns the object, with a short
`module_object` name. A helper keeps it to one line:
```c
#define Q_NAMED(len, sz, name) ({ QueueHandle_t _q = xQueueCreate(len, sz); \
                                  configASSERT(_q); vQueueAddToRegistry(_q, name); _q; })
```
(GNU statement expression; write a function if you need portable C.)

## Verify
- [ ] Halt the target: the RTOS view lists every queue, semaphore and mutex by name with fill level.
- [ ] Names survive after the creating function returns (literals only).
- [ ] Delete paths unregister first.
