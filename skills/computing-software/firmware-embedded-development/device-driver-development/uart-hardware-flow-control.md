---
id: computing-software.firmware-embedded-development.device-driver-development.uart-hardware-flow-control
name: uart-hardware-flow-control
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [hardware-flow-control, rts-cts, uart-driver, overrun-prevention, crtscts, fifo-threshold, xon-xoff, bluetooth-hci-uart, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use RTS/CTS hardware flow control on UART links: signal direction and polarity, hardware vs software RTS thresholds, skid bytes, Linux crtscts, and when XON/XOFF is acceptable."
sources:
  - https://docs.kernel.org/devicetree/bindings/serial/serial.html
  - https://man7.org/linux/man-pages/man3/termios.3.html
  - https://github.com/coreutils/coreutils/blob/master/src/stty.c
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_uart/include/driver/uart.h
  - https://github.com/STMicroelectronics/cmsis_device_l4/blob/master/Include/stm32l476xx.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardware flow control (RTS/CTS)

**Goal:** a fast UART link (Bluetooth/Wi-Fi modules, modems, MCU-to-SoC) where the slower side
can pause the sender instead of losing bytes.

## Signals and wiring
- **RTS** (output): "I can receive"; deasserting it asks the peer to stop sending to me.
- **CTS** (input): the peer's RTS; when it is deasserted my transmitter pauses. Check each device's
  datasheet for the electrical polarity.
- Cross them: my RTS -> peer CTS, my CTS <- peer RTS. Naming on modules is from the module's
  point of view; mismatched labels are the #1 bring-up problem - verify with a scope.

## Hardware vs software RTS
- **Hardware RTS** (STM32 `USART_CR3.RTSE`, ESP32 `UART_HW_FLOWCTRL_CTS_RTS` with
  `rx_flow_ctrl_thresh`): the peripheral drives RTS from its receive state; read your part's
  reference manual for exactly when it deasserts, and test with interrupt latency in mind.
- **Software RTS** (GPIO driven from the ring buffer level): deassert at a high-water mark
  leaving room for **skid bytes** - the peer may send several more bytes after RTS drops (its
  TX FIFO or DMA in flight; measure the peer's worst case). High-water = size − worst-case skid; re-assert at a low-water mark (hysteresis).
- **Hardware CTS** is almost always used: TX halts at a byte boundary without CPU involvement.

## Linux side
```sh
stty -F /dev/ttyS1 921600 crtscts raw -echo
```
Devicetree (serial binding): `uart-has-rtscts;` marks dedicated RTS/CTS lines, or give GPIOs with
`rts-gpios`/`cts-gpios`. In C, set `CRTSCTS` (not in POSIX) in `termios.c_cflag`; `stty crtscts` sets
it from the shell. USB-serial adapters support it if the RTS/CTS pins are wired.

## When not to / alternatives
- XON/XOFF (software flow control, termios `IXON`/`IXOFF`) uses the in-band bytes 0x11 and 0x13,
  so binary data may contain them and latency is worse. Avoid for firmware updates or HCI.
- If a peer ignores CTS (some bridge chips in a mode, or misconfigured), flow control gives
  false confidence; test overrun deliberately.
- Low baud with large buffers and DMA may not need flow control at all; compute
  worst-case consumer stall × byte rate first.

## Gotchas
- At boot, before your firmware configures the UART, RTS floats: add a pull-up so the peer
  does not send into an uninitialised receiver (or a pull-down if you want it to send).
- Bluetooth HCI UART links generally rely on flow control at high baud rates; check the controller's
  documentation.

## Verify
- [ ] Stall the receiver task for 1 s during a bulk transfer: RTS deasserts, no overrun or
      dropped bytes, transfer CRC passes.
- [ ] Scope shows TX pausing within a few bytes of CTS going high.

## Checked

TinyUSB master sources (hathach/tinyusb), Microsoft driver documentation (MicrosoftDocs/windows-driver-docs, staging), STM32 CMSIS device headers and Linux kernel Documentation, read 2026-10-27.
Confirmed: devicetree `uart-has-rtscts`, `rts-gpios` and `cts-gpios` (Linux serial.yaml); `CRTSCTS` described as RTS/CTS hardware flow control and not in POSIX, and `IXON`/`IXOFF` as XON/XOFF (termios man page); `crtscts` accepted by stty (coreutils source); ESP-IDF `uart_config_t.rx_flow_ctrl_thresh` ("UART HW RTS threshold") and `UART_HW_FLOWCTRL_CTS_RTS`; STM32 `USART_CR3_RTSE` and `USART_CR3_CTSE` in the CMSIS header; 0x11/0x13 are the ASCII DC1/DC3 control codes.
Removed as unconfirmed: active-low polarity, the NXP RXRTSE name, the 1-byte data register behaviour, the 16-64 byte skid figure, and the H4 1-3 Mbaud rule.

Method: documentation only; no commands were run.
