---
id: computing-software.firmware-embedded-development.stm32.fdcan-with-hal
name: fdcan-with-hal
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-hal-comms, stm32-fdcan, can-fd, fdcan-filters, fdcan-bit-timing, stm32, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Configure STM32 FDCAN (G4, H7, L5, U5) with HAL: classic CAN and CAN FD bit timing, message RAM, filters, Rx FIFOs, Tx FIFO/queue and bus-off handling."
sources:
  - https://www.st.com/resource/en/application_note/an5348-introduction-to-fdcan-peripherals-for-stm32-product-classes-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FDCAN with HAL

## Init (G4, 80 MHz FDCAN kernel clock, 500 kbit/s nominal + 2 Mbit/s data)
```c
hfdcan1.Init.ClockDivider = FDCAN_CLOCK_DIV1;
hfdcan1.Init.FrameFormat = FDCAN_FRAME_FD_BRS;          /* or FDCAN_FRAME_CLASSIC */
hfdcan1.Init.Mode = FDCAN_MODE_NORMAL;
hfdcan1.Init.AutoRetransmission = ENABLE;
hfdcan1.Init.TransmitPause = DISABLE;
hfdcan1.Init.ProtocolException = DISABLE;
/* nominal: 80 MHz / 1 / (1 + 127 + 32) = 500 kbit/s, sample point 80% */
hfdcan1.Init.NominalPrescaler = 1; hfdcan1.Init.NominalTimeSeg1 = 127;
hfdcan1.Init.NominalTimeSeg2 = 32; hfdcan1.Init.NominalSyncJumpWidth = 32;
/* data: 80 MHz / 1 / (1 + 29 + 10) = 2 Mbit/s, SP 75% */
hfdcan1.Init.DataPrescaler = 1; hfdcan1.Init.DataTimeSeg1 = 29;
hfdcan1.Init.DataTimeSeg2 = 10; hfdcan1.Init.DataSyncJumpWidth = 10;
hfdcan1.Init.StdFiltersNbr = 2; hfdcan1.Init.ExtFiltersNbr = 0;
hfdcan1.Init.TxFifoQueueMode = FDCAN_TX_FIFO_OPERATION;
HAL_FDCAN_Init(&hfdcan1);
```
H7 has a configurable message RAM (element counts and sizes in Init); G4/L5/U5 have a fixed
layout (28 std filters, 8 ext filters, 2 Rx FIFOs x 3, 3 Tx buffers).
Use **TDC** (transmitter delay compensation, `HAL_FDCAN_ConfigTxDelayCompensation`) for data
rates above 1 Mbit/s.

## Filters
```c
FDCAN_FilterTypeDef f = { .IdType = FDCAN_STANDARD_ID, .FilterIndex = 0,
    .FilterType = FDCAN_FILTER_MASK, .FilterConfig = FDCAN_FILTER_TO_RXFIFO0,
    .FilterID1 = 0x100, .FilterID2 = 0x7F0 };          /* accept 0x100-0x10F */
HAL_FDCAN_ConfigFilter(&hfdcan1, &f);
HAL_FDCAN_ConfigGlobalFilter(&hfdcan1, FDCAN_REJECT, FDCAN_REJECT, FDCAN_FILTER_REMOTE, FDCAN_FILTER_REMOTE);
```
Without the global filter call, non-matching frames go to FIFO0 by default (accept all).

## Run
```c
HAL_FDCAN_ActivateNotification(&hfdcan1, FDCAN_IT_RX_FIFO0_NEW_MESSAGE | FDCAN_IT_BUS_OFF, 0);
HAL_FDCAN_Start(&hfdcan1);

FDCAN_TxHeaderTypeDef th = { .Identifier = 0x123, .IdType = FDCAN_STANDARD_ID,
    .TxFrameType = FDCAN_DATA_FRAME, .DataLength = FDCAN_DLC_BYTES_64,
    .ErrorStateIndicator = FDCAN_ESI_ACTIVE, .BitRateSwitch = FDCAN_BRS_ON,
    .FDFormat = FDCAN_FD_CAN, .TxEventFifoControl = FDCAN_NO_TX_EVENTS };
HAL_FDCAN_AddMessageToTxFifoQ(&hfdcan1, &th, data);

void HAL_FDCAN_RxFifo0Callback(FDCAN_HandleTypeDef *h, uint32_t its) {
    FDCAN_RxHeaderTypeDef rh; uint8_t d[64];
    while (HAL_FDCAN_GetRxMessage(h, FDCAN_RX_FIFO0, &rh, d) == HAL_OK) handle(&rh, d);
}
```
In older HAL versions `DataLength` takes `FDCAN_DLC_BYTES_x` constants (shifted values), not byte counts.

## Bus-off
FDCAN enters INIT on bus-off (`PSR.BO`). Recover: in `HAL_FDCAN_ErrorStatusCallback` with
`FDCAN_IT_BUS_OFF`, clear `CCCR.INIT` (`HAL_FDCAN_Stop`/`Start` or write CCCR) after a back-off delay.

## Verify
- [ ] Bus analyser decodes CAN FD frames with BRS at 2 Mbit/s without errors.
- [ ] Filters reject non-matching IDs (FIFO stays empty).
- [ ] Bus-off recovery tested by shorting CANH/CANL briefly.

## Checked

2026-10-31: Confirmed the G4 FDCAN HAL API (the `FDCAN_DLC_BYTES_0..64` family, `HAL_FDCAN_Init`, message-Rx/Tx and filter APIs) from stm32g4xx_hal_fdcan.h, and the `FDCAN_PSR_BO` (bus-off) and `FDCAN_CCCR_INIT` bit names from the CMSIS device headers.

Method: documentation only; no commands were run.
