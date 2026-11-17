---
id: computing-software.firmware-embedded-development.device-driver-development.rs-485-direction-control
name: rs-485-direction-control
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [rs-485, half-duplex, driver-enable, de-re-pin, transmission-complete, modbus-rtu, termination, failsafe-bias, uart-driver, firmware-embedded-development]
level: practitioner
status: gated
description: "Drive a half-duplex RS-485 transceiver correctly: DE/RE timing, releasing the bus on transmission-complete not TX-empty, hardware DE pins, Linux RS485 ioctl, termination and bias."
sources:
  - https://docs.kernel.org/driver-api/serial/serial-rs485.html
  - https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/serial/rs485.yaml
  - https://github.com/STMicroelectronics/stm32l4xx_hal_driver
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/uart.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RS-485 direction control

**Goal:** a half-duplex RS-485 node that never truncates its own last byte and never collides
with the reply.

## The rule
Assert DE (driver enable) before the first start bit, keep it asserted until the **stop bit of
the last byte has left the shift register**, then release immediately so the other node can
answer; a late release makes you clip the reply.

## Software control
```c
void rs485_send(const uint8_t *p, size_t n) {
    gpio_set(DE_PIN);                        /* DE and /RE often tied: also disables receiver */
    delay_us(DE_SETUP_US);                   /* transceiver enable time: see its datasheet */
    uart_start_tx(p, n);                     /* IRQ or DMA */
}
void USART_IRQHandler(void) {
    ...
    if (USART->ISR & USART_ISR_TC) {         /* transmission complete, NOT TXE */
        USART->ICR = USART_ICR_TCCF;
        gpio_clear(DE_PIN);
    }
}
```
- **TXE / DMA-complete fire while the last byte is still shifting out.** Releasing DE there
  chops the final byte (classic CRC-error-on-last-byte bug). Use TC.
- With DE and /RE tied, you do not hear your own echo; tie /RE low separately if you want to
  read back for collision detection (then discard echo bytes).

## Hardware DE
Many UARTs drive DE themselves with programmable assertion/deassertion times:
STM32 `USART_CR3_DEM` with assertion/deassertion times DEAT/DEDT (`HAL_RS485Ex_Init`) and ESP32
`UART_MODE_RS485_HALF_DUPLEX`; other families have similar modes (see the reference manual). Prefer
this: exact timing with zero CPU latency.

## Linux
```c
struct serial_rs485 rs = { .flags = SER_RS485_ENABLED | SER_RS485_RTS_ON_SEND,
                           .delay_rts_before_send = 0, .delay_rts_after_send = 0 };
ioctl(fd, TIOCSRS485, &rs);
```
or devicetree `linux,rs485-enabled-at-boot-time;` and `rs485-rts-delay = <0 0>;` (before-send and
after-send delays; `rs485-rts-active-low` inverts the RTS level). RTS is used as DE.

## Physical layer checklist
- Terminate both **ends** of the trunk only (typically 120 ohm, matching the cable impedance (gated: unconfirmed, source is paywalled or blocked)); stubs short.
- Failsafe biasing (pull-up on A, pull-down on B, value from the transceiver datasheet) or transceivers
  with built-in failsafe so an idle bus reads as mark (1) instead of noise.
- Common ground/reference wire; isolated transceivers for long runs between buildings.
- Node count is set by unit loads: 32 unit loads standard, and 1/8-unit-load transceivers allow 256 nodes (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Scope DE and the A-B differential: DE falls just after the last stop bit, not during it.
- [ ] Modbus master sees no CRC errors over 10k transactions at max baud.

## Checked

2026-10-27, Linux kernel documentation (mainline v7.3), STM32L4 HAL and CMSIS header (master), ESP-IDF uart docs (master).
Confirmed in serial-rs485.rst: TIOCSRS485, struct serial_rs485, SER_RS485_ENABLED, SER_RS485_RTS_ON_SEND, delay_rts_before_send and delay_rts_after_send. Confirmed in the rs485.yaml binding: linux,rs485-enabled-at-boot-time, rs485-rts-delay (two values), rs485-rts-active-low. Confirmed in the STM32L4 HAL and header: HAL_RS485Ex_Init with DEAT/DEDT, USART_CR3_DEM, USART_ISR_TC, USART_ICR_TCCF. Confirmed in the ESP-IDF UART documentation: UART_MODE_RS485_HALF_DUPLEX. The termination value and unit-load numbers are marked gated because TIA-485 is paywalled and the TI note could not be read. Removed the Modbus 1.75 ms reply claim, the NXP LPUART and SAMD mode names, the 680 ohm bias value, the rts-gpios property and the transceiver enable-time figure.

Method: documentation only; no commands were run.
