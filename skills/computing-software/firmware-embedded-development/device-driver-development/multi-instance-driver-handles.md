---
id: computing-software.firmware-embedded-development.device-driver-development.multi-instance-driver-handles
name: multi-instance-driver-handles
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [driver-instance, interrupt-driven, device-handle, const-config, isr-dispatch, firmware-embedded-development]
level: advanced
status: draft
description: "Design drivers that support several instances (UART1..UART5, two identical sensors): const config plus RAM state structs, ISR-to-instance dispatch, and static allocation."
sources:
  - https://docs.zephyrproject.org/latest/kernel/drivers/index.html
  - https://www.state-machine.com/doc/AN_OOP_in_C.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-instance driver handles

Global variables and hard-coded `USART2` in a driver mean copy-pasting the driver for the second
UART. Separate the code from per-instance data.

## Pattern: const config + mutable state
```c
typedef struct {                 /* in flash: board/instance description */
    USART_TypeDef *regs;
    IRQn_Type irq;
    uint32_t baud;
    void (*clk_enable)(void);
} uart_cfg_t;

typedef struct {                 /* in RAM: runtime state */
    const uart_cfg_t *cfg;
    ringbuf_t rx;
    uint8_t rx_mem[256];
    volatile uint32_t errors;
} uart_t;

int uart_init(uart_t *u, const uart_cfg_t *cfg);
int uart_write(uart_t *u, const void *p, size_t n);
```
Board code defines instances statically:
```c
static const uart_cfg_t k_console_cfg = { USART2, USART2_IRQn, 115200, rcc_usart2_on };
uart_t g_console;
static const uart_cfg_t k_gps_cfg = { USART3, USART3_IRQn, 9600, rcc_usart3_on };
uart_t g_gps;
```

## ISR dispatch
Vector table entries are fixed functions; map them to instances:
```c
static uart_t *s_by_irq[UART_MAX];               /* filled in uart_init */
void USART2_IRQHandler(void) { uart_isr(s_by_irq[1]); }
void USART3_IRQHandler(void) { uart_isr(s_by_irq[2]); }
```
or a small table indexed by `IRQn`. Callbacks carry a `void *arg` (or the handle) so upper layers
are also instance-agnostic.

## Rules
- No `static` mutable variables inside driver functions; everything lives in the handle.
- Handles are statically allocated by the user (no `malloc`), sized at compile time.
- Config is `const` (flash); state is RAM. Zephyr's `DEVICE_DT_INST_DEFINE` with `config` and
  `data` pointers is exactly this pattern, generated from devicetree.
- An "opaque handle" (incomplete struct type in the header) hides internals but forces dynamic
  or pool allocation; exposing the struct with a "private" comment is the usual compromise in C.
- External chips: the handle holds the bus pointer and address/CS, so two BME280s on different
  buses are two handles of one driver.

## Verify
- [ ] Two instances run concurrently (e.g. loopback UART2 <-> UART3) with independent state.
- [ ] `nm` shows no driver-private `.bss` symbols besides the instance tables.
