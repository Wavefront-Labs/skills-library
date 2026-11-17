---
id: computing-software.firmware-embedded-development.stm32.multi-task-watchdog-supervision
name: multi-task-watchdog-supervision
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [iwdg, watchdog-task-monitor, task-checkin, rtos-watchdog, iwdg-timeout-calculation, stm32, firmware-embedded-development]
level: advanced
status: draft
description: "Supervise every RTOS task with one STM32 IWDG: task check-ins, a supervisor that refreshes only when all are alive, handling blocking tasks, recording the culprit, and LSI-tolerant timeouts."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.freertos.org/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-task watchdog supervision

Refreshing the IWDG from one task (or the idle hook) only proves that task runs. Other tasks
can be deadlocked while the board looks healthy. The fix: each task checks in, and a single
supervisor refreshes the hardware watchdog only when **all** monitored tasks have checked in
within their deadlines.

## IWDG timing
```c
/* LSI ~32 kHz on L4 (datasheet range e.g. 29.5-34 kHz): timeout = 4 * 2^PR * (RLR + 1) / f_LSI */
IWDG_HandleTypeDef hiwdg = { .Instance = IWDG,
    .Init = { .Prescaler = IWDG_PRESCALER_64, .Reload = 999, .Window = IWDG_WINDOW_DISABLE } };
/* nominal 64 * 1000 / 32000 = 2.0 s; with LSI at +6% it's ~1.88 s: design for the minimum */
HAL_IWDG_Init(&hiwdg);
```
Supervisor period must be well below the **minimum** timeout (LSI tolerance), e.g. refresh
every 500 ms for a 2 s nominal timeout.

## Check-in registry
```c
#define WDT_TASK_COUNT 4
typedef struct { const char *name; TickType_t max_gap; volatile TickType_t last; bool active; } wdt_slot_t;
static wdt_slot_t slots[WDT_TASK_COUNT];

void wdt_register(int id, const char *name, uint32_t max_gap_ms) {
    slots[id] = (wdt_slot_t){ name, pdMS_TO_TICKS(max_gap_ms), xTaskGetTickCount(), true };
}
void wdt_checkin(int id)      { slots[id].last = xTaskGetTickCount(); }
void wdt_suspend(int id)      { slots[id].active = false; }   /* before a known long block */
void wdt_resume(int id)       { slots[id].last = xTaskGetTickCount(); slots[id].active = true; }

static void wdt_supervisor(void *arg)
{
    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(500));
        TickType_t now = xTaskGetTickCount();
        int late = -1;
        for (int i = 0; i < WDT_TASK_COUNT; i++)
            if (slots[i].active && (now - slots[i].last) > slots[i].max_gap) { late = i; break; }
        if (late < 0) {
            HAL_IWDG_Refresh(&hiwdg);
        } else {
            record_watchdog_culprit(slots[late].name);   /* to .noinit / backup register */
            /* stop refreshing: IWDG resets us */
        }
    }
}
```
Run the supervisor at a **high** priority so CPU starvation of lower tasks is detected through
their missed check-ins, not hidden by the supervisor also being starved.

## Tasks that block for long
A task waiting for a rare event (button, network command) can't check in. Options:
- Block with a timeout shorter than `max_gap` and check in on timeout: `xQueueReceive(q, &m, pdMS_TO_TICKS(1000))`.
- Mark it inactive around long, legitimate waits (`wdt_suspend`/`wdt_resume`), e.g. during a
  60 s flash erase or a blocking modem command with its own timeout.
- Give each task a `max_gap` matching its real worst-case period, not one global value.

## Rules
- Never refresh from an ISR, a timer callback, or the idle hook alone: those run even when
  application tasks are deadlocked.
- Start the IWDG early (before long init) and let the supervisor take over once the scheduler runs;
  long init steps refresh explicitly.
- Record the culprit **before** the reset so the next boot can report it (see reset-cause-decoding).
- Optional pre-reset hook: use the WWDG early-wakeup interrupt or an IWDG early-wakeup interrupt
  (newer series) for last-gasp logging.

## Verify
- [ ] Deadlock injected in each task in turn: reset happens and the culprit name is reported after reboot.
- [ ] CPU-hog injected in a high-priority task: lower tasks' missed check-ins trigger the reset.
- [ ] Timeout margin computed with minimum LSI frequency.
