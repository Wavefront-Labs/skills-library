---
id: computing-software.firmware-embedded-development.stm32.hal-i2c-sequential-transfers
name: hal-i2c-sequential-transfers
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-hal-comms, hal-i2c-seq, i2c-repeated-start, xferoptions, i2c-first-frame, stm32, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Build custom I2C transactions (repeated start, combined write-read, chunked transfers) with STM32 HAL Seq_Transmit/Seq_Receive and XferOptions, including slave-side listen mode."
sources:
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
  - https://github.com/STMicroelectronics/STM32CubeL4/tree/master/Projects/NUCLEO-L476RG/Examples/I2C
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HAL I2C sequential transfers

`HAL_I2C_Mem_Read` covers register-addressed devices. For anything else (two-byte commands with
restart, reading a length byte then the payload, SMBus block reads) use the sequential API with
explicit framing options.

## XferOptions
| Option | Meaning |
|---|---|
| `I2C_FIRST_FRAME` | START + address, no STOP at end |
| `I2C_NEXT_FRAME` | continue, same direction (no restart) |
| `I2C_LAST_FRAME` | ... then STOP |
| `I2C_FIRST_AND_LAST_FRAME` | single complete transfer |
| `I2C_FIRST_AND_NEXT_FRAME` | START, no STOP, allows direction change after (repeated start) |
| `I2C_LAST_FRAME_NO_STOP` | end without STOP (keep bus for later restart) |

## Write command then read with repeated start
```c
uint8_t cmd[2] = { 0xE0, 0x00 };
HAL_I2C_Master_Seq_Transmit_IT(&hi2c1, ADDR << 1, cmd, 2, I2C_FIRST_FRAME);
/* in HAL_I2C_MasterTxCpltCallback: */
HAL_I2C_Master_Seq_Receive_IT(&hi2c1, ADDR << 1, rx, 6, I2C_LAST_FRAME);   /* restart + read + STOP */
```
Direction change between frames generates a repeated START automatically.

## Length-prefixed read (SMBus block read style)
```c
HAL_I2C_Master_Seq_Transmit_IT(h, a, &reg, 1, I2C_FIRST_FRAME);
/* TxCplt: */ HAL_I2C_Master_Seq_Receive_IT(h, a, &len, 1, I2C_NEXT_FRAME);
/* RxCplt (first): */ HAL_I2C_Master_Seq_Receive_IT(h, a, data, len, I2C_LAST_FRAME);
```
`NEXT_FRAME` in the same direction continues reading without a restart.

## Slave with listen mode
```c
HAL_I2C_EnableListen_IT(&hi2c2);
void HAL_I2C_AddrCallback(I2C_HandleTypeDef *h, uint8_t dir, uint16_t addr) {
    if (dir == I2C_DIRECTION_TRANSMIT) HAL_I2C_Slave_Seq_Receive_IT(h, &reg, 1, I2C_FIRST_FRAME);
    else HAL_I2C_Slave_Seq_Transmit_IT(h, &regs[reg], sizeof regs - reg, I2C_LAST_FRAME);
}
void HAL_I2C_ListenCpltCallback(I2C_HandleTypeDef *h) { HAL_I2C_EnableListen_IT(h); }
```
Always re-enable listen after each transaction and handle `HAL_I2C_ErrorCallback` with AF
(NACK at end of master read is normal for slaves).

## Pitfalls
- Address is 7-bit shifted left by one in HAL calls.
- DMA variants exist (`_Seq_Transmit_DMA`); F1/F4 I2C v1 peripheral has errata with DMA and
  1-2 byte reads; the v2 peripheral (L4, G4, F7, H7) is robust.
- Never start the next frame from outside the callback while the previous is running.

## Verify
- [ ] Logic analyser shows Sr (repeated start) without STOP between write and read.
- [ ] Slave handles 10k transactions with random lengths without hanging (listen re-enabled).

## Checked

2026-10-31: Confirmed the sequential-transfer HAL API and the `I2C_FIRST_FRAME`/`I2C_NEXT_FRAME`/`I2C_LAST_FRAME` (and combined) option macros with their RELOAD/soft-end encodings from stm32l4xx_hal_i2c.h; `LL_USART_DMA_GetRegAddr` usage is per the LL headers.

Method: documentation only; no commands were run.
