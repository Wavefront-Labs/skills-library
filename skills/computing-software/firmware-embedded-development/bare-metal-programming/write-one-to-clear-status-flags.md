---
id: computing-software.firmware-embedded-development.bare-metal-programming.write-one-to-clear-status-flags
name: write-one-to-clear-status-flags
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [write-one-to-clear, mmio, rc-w1, rc-w0, clear-on-read, status-register, firmware-embedded-development]
level: practitioner
status: draft
description: "Clear peripheral status flags correctly by access type (rc_w1, rc_w0, rc_r, read sequences) without losing other flags to read-modify-write."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/ddi0403/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Write-1-to-clear and read-to-clear status flags

Reference manuals annotate each bit with its access type. Get it wrong and flags either never
clear (ISR storm) or unrelated flags get cleared (lost events).

| Notation (ST style) | Meaning | Correct clear |
|---|---|---|
| `rc_w1` | read, clear by writing 1 | `REG = FLAG;` |
| `rc_w0` | read, clear by writing 0 (writing 1 has no effect) | `REG = ~FLAG;` |
| `rc_r` | cleared by reading the register | read it once (and only once) |
| `r` + sequence | cleared by a read sequence (e.g. read SR then DR) | follow the sequence exactly |
| `w1c` / `W1C` (other vendors) | same as rc_w1 | `REG = FLAG;` |

## The read-modify-write bug
```c
EXTI->PR |= EXTI_PR_PR5;      /* WRONG: reads all pending bits (say PR3 also set) and writes them back as 1 */
EXTI->PR  = EXTI_PR_PR5;      /* right: writes 1 only to bit 5; zeros are ignored for rc_w1 */

TIM2->SR &= ~TIM_SR_UIF;      /* WRONG for rc_w0: a CC1IF arriving between read and write is cleared */
TIM2->SR  = ~TIM_SR_UIF;      /* right: writes 0 to UIF, 1 (no effect) everywhere else */
```
HAL macros do this right (`__HAL_TIM_CLEAR_FLAG` writes `~flag`); hand-written code is where
it breaks.

## Dedicated clear registers
Newer peripherals separate status and clear: STM32 USART `ISR` + `ICR`, DMA `ISR` + `IFCR`,
nRF `EVENTS_x = 0`. Write the clear register with the bit mask; never write the status register.

## Read-sequence clears
STM32F1/F4 USART: overrun `ORE` clears by reading `SR` then `DR`. I2C v1 `ADDR`: read `SR1` then
`SR2`. A debugger memory view that refreshes SR can clear flags behind your back; close peripheral
views when chasing these bugs.

## Clear-on-read data
FIFO data registers and some capture registers pop or clear on read. Read once into a local; do
not test a register in an `if` and read it again.

## Verify
- [ ] Every flag clear in the driver uses `=` (not `|=`/`&=`) on status/clear registers, matching the access type.
- [ ] A test that generates two events close together (two EXTI lines, UIF + CC1IF) handles both.
