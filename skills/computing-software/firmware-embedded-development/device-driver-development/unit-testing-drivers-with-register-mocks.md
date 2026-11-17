---
id: computing-software.firmware-embedded-development.device-driver-development.unit-testing-drivers-with-register-mocks
name: unit-testing-drivers-with-register-mocks
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [register-mocking, interrupt-driven, fake-registers, host-testing, driver-tests, firmware-embedded-development]
level: advanced
status: draft
description: "Unit test register-level drivers on the host by pointing peripheral macros at fake RAM structs, simulating status flags and interrupts, and asserting the register write sequence."
sources:
  - https://www.throwtheswitch.org/unity
  - https://interrupt.memfault.com/blog/unit-testing-basics
  - https://github.com/meekrosoft/fff
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unit testing drivers with register mocks

## Redirect the peripheral to RAM
```c
/* driver code uses USART2->... via the CMSIS macro */
#ifdef UNIT_TEST
#  include "fake_regs.h"          /* extern USART_TypeDef fake_usart2; */
#  undef  USART2
#  define USART2 (&fake_usart2)
#endif
```
Better: make the driver take the register block pointer as a parameter (`uart_init(USART_TypeDef *regs, ...)`):
no macro tricks, multi-instance for free, and tests pass `&fake`.

## Simple state tests
```c
void test_init_sets_baud_and_enables(void) {
    memset(&fake, 0, sizeof fake);
    uart_init(&fake, 80000000, 115200);
    TEST_ASSERT_EQUAL_HEX32(694, fake.BRR);               /* 80 MHz / 115200 rounded */
    TEST_ASSERT_BITS_HIGH(USART_CR1_UE | USART_CR1_TE | USART_CR1_RE, fake.CR1);
}
```

## Simulating hardware behaviour
Status flags that the hardware sets (TXE, RXNE, BSY) won't change by themselves in RAM, so a busy
wait loops forever. Options:
1. **Preset flags** before calling: `fake.ISR = USART_ISR_TXE;` for code that waits for TXE.
2. **Access hooks**: compile register accesses through inline accessors (`reg_read(&r)`,
   `reg_write(&r, v)`) that call test callbacks in `UNIT_TEST` builds; the callback can emulate
   behaviour (writing TDR clears TXE, then sets it again) and record a write log.
3. **Inject interrupts** by calling the ISR function directly after setting flags:
   `fake.ISR = USART_ISR_RXNE; fake.RDR = 'A'; USART2_IRQHandler();`.

## Asserting sequences
Order matters (disable peripheral, configure, enable). Record writes in a log via accessors and
compare with an expected list:
```c
static const reg_op_t expected[] = { {&fake.CR1, 0}, {&fake.BRR, 694}, {&fake.CR1, UE|TE|RE} };
TEST_ASSERT_EQUAL_MEMORY(expected, log, sizeof expected);
```
fff or CMock can mock the accessor functions if you prefer framework support.

## Limits
These tests verify your understanding of the reference manual, not the silicon. Pair them with
on-target tests (HIL) for timing, DMA and real flag behaviour, and with the errata.

## Verify
- [ ] Driver builds and tests run on the host with no vendor startup code.
- [ ] Tests cover error flags (ORE, NACK) and the recovery path, which are hard to trigger on hardware.
