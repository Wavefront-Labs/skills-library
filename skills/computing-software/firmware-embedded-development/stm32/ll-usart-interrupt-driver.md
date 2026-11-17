---
id: computing-software.firmware-embedded-development.stm32.ll-usart-interrupt-driver
name: ll-usart-interrupt-driver
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-ll, ll-usart, usart-ring-buffer, rxne-isr, txe-interrupt, stm32, firmware-embedded-development]
level: practitioner
status: draft
description: "Write an interrupt-driven STM32 USART driver with LL: RXNE/TXE/TC handling, ring buffers, overrun and noise error clearing, and idle detection for packet framing."
sources:
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
  - https://github.com/STMicroelectronics/STM32CubeL4/tree/master/Projects/NUCLEO-L476RG/Examples_LL/USART
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LL USART interrupt driver

HAL's UART IT API arms one fixed-length receive at a time. A ring buffer with LL keeps receiving
continuously with minimal overhead.

## Init (after GPIO AF and clock setup)
```c
LL_USART_SetBaudRate(USART2, 80000000, LL_USART_PRESCALER_DIV1, LL_USART_OVERSAMPLING_16, 115200);
LL_USART_ConfigCharacter(USART2, LL_USART_DATAWIDTH_8B, LL_USART_PARITY_NONE, LL_USART_STOPBITS_1);
LL_USART_SetTransferDirection(USART2, LL_USART_DIRECTION_TX_RX);
LL_USART_Enable(USART2);
LL_USART_EnableIT_RXNE(USART2);
LL_USART_EnableIT_ERROR(USART2);      /* frame/noise/overrun interrupts (with DMA or EIE) */
NVIC_SetPriority(USART2_IRQn, 5); NVIC_EnableIRQ(USART2_IRQn);
```
(F4-style parts have no `PRESCALER` argument: `LL_USART_SetBaudRate(USART2, pclk, LL_USART_OVERSAMPLING_16, 115200)`.)

## ISR with ring buffers
```c
#define RB 256                                   /* power of two */
static volatile uint8_t rx[RB], tx[RB];
static volatile uint16_t rx_h, rx_t, tx_h, tx_t;

void USART2_IRQHandler(void) {
    if (LL_USART_IsActiveFlag_ORE(USART2)) { LL_USART_ClearFlag_ORE(USART2); overruns++; }
    if (LL_USART_IsActiveFlag_NE(USART2))  { LL_USART_ClearFlag_NE(USART2); }
    if (LL_USART_IsActiveFlag_FE(USART2))  { LL_USART_ClearFlag_FE(USART2); }
    if (LL_USART_IsActiveFlag_RXNE(USART2)) {
        uint8_t b = LL_USART_ReceiveData8(USART2);       /* read clears RXNE */
        uint16_t n = (rx_h + 1) & (RB - 1);
        if (n != rx_t) { rx[rx_h] = b; rx_h = n; } else rx_drops++;
    }
    if (LL_USART_IsEnabledIT_TXE(USART2) && LL_USART_IsActiveFlag_TXE(USART2)) {
        if (tx_t != tx_h) { LL_USART_TransmitData8(USART2, tx[tx_t]); tx_t = (tx_t + 1) & (RB - 1); }
        else LL_USART_DisableIT_TXE(USART2);            /* nothing left: stop TXE storm */
    }
}
int uart_put(uint8_t b) {
    uint16_t n = (tx_h + 1) & (RB - 1);
    if (n == tx_t) return -1;                            /* full */
    tx[tx_h] = b; tx_h = n;
    LL_USART_EnableIT_TXE(USART2);
    return 0;
}
```
Flag/clear names: on F1/F4 the ORE flag is cleared by reading SR then DR (`LL_USART_ClearFlag_ORE`
does this sequence); on L4/G4/F7 by writing ICR. An uncleared ORE on L4 keeps the interrupt
firing forever and blocks the main loop: always handle it.

## Packet framing with idle line
`LL_USART_EnableIT_IDLE(USART2)`, then in the ISR `if (LL_USART_IsActiveFlag_IDLE) { LL_USART_ClearFlag_IDLE; frame_end(); }`.
Newer parts also have receiver timeout (RTOF) for Modbus-style 3.5-char gaps.

## Before sleep or RS485 turnaround
Wait for TC (transmission complete), not TXE, before switching DE low or entering Stop.

## Verify
- [ ] 1 h echo test at max baud with zero drops; overrun counter stays 0.
- [ ] Line noise injection: error flags counted, driver keeps running.
