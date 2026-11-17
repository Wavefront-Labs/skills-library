---
id: computing-software.firmware-embedded-development.bare-metal-programming.spurious-interrupt-reentry
name: spurious-interrupt-reentry
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [spurious-interrupt, nvic, interrupt-flag-clear, write-buffer, dsb, firmware-embedded-development]
level: advanced
status: draft
description: "Fix ISRs that run twice per event on Cortex-M: clearing the peripheral flag at the end of the handler races the write buffer, so the NVIC re-pends the IRQ."
sources:
  - https://developer.arm.com/documentation/ka003795/latest/
  - https://developer.arm.com/documentation/dui0553/latest/
  - https://www.st.com/resource/en/errata_sheet/es0206-stm32f427437-and-stm32f429439-line-limitations-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spurious re-entry from late flag clearing

**Symptom:** each event's ISR executes twice; the second time no status flag is set. Counters
double, "unknown interrupt" branches hit, or a DMA half-transfer callback fires an extra time.

## Cause
The flag-clear write travels through the CPU write buffer and a bus bridge (AHB to APB, often
at a slower clock). If it is the **last instruction** before exception return, the core leaves
the handler before the peripheral has de-asserted its IRQ line. The NVIC samples the line as
still active and re-pends the interrupt, which tail-chains straight back in.

## Fix
Clear the flag **first** in the handler, then do the work:
```c
void TIM2_IRQHandler(void) {
    uint32_t sr = TIM2->SR;
    TIM2->SR = ~sr;               /* rc_w0 flags: write 0 to clear the ones we saw */
    if (sr & TIM_SR_UIF) { tick(); }
}
```
If the clear must be last (e.g. you need to read data before clearing), force completion:
```c
    USARTx->ICR = USART_ICR_ORECF;
    (void)USARTx->ICR;            /* read-back from the same peripheral stalls until the write lands */
    __DSB();                      /* DSB alone completes the write on the bus matrix, not always at the APB peripheral */
```
The read-back is the reliable one on slow APB buses; ST errata for several families recommend it.

## Related traps
- **Clearing with read-modify-write** of a W1C/rc_w0 register (`SR &= ~FLAG`) clears flags that
  arrived between the read and write: other events are lost. Write a constant mask instead.
- **Level-triggered sources** (UART RXNE, I2C) stay asserted until the data register is read;
  "clearing the flag" means reading DR.
- **EXTI pending bits** are W1C in `EXTI->PR` (or `RPR1/FPR1` on newer parts); clear the specific
  line only.
- **Shared IRQ lines** (EXTI9_5, DMA2_Stream groups): check and clear each source's flag.

## Verify
- [ ] Count ISR entries vs events with a scope (GPIO toggle per entry): counts match.
- [ ] Single-step at the handler exit: `NVIC_GetPendingIRQ(IRQn)` is 0 after the clear completes.
