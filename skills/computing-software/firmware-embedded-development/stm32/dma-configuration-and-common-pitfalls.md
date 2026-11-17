---
id: computing-software.firmware-embedded-development.stm32.dma-configuration-and-common-pitfalls
name: dma-configuration-and-common-pitfalls
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32, dma, dma-stream, dma-channel-request, circular-mode, half-transfer-interrupt, transfer-complete, fifo-threshold, memory-to-memory, peripheral-to-memory, cache-coherency, dcache-invalidate, dma-mux, stm32h7, firmware-embedded-development, dma-request-mapping]
level: advanced
status: draft
description: "Configure STM32 DMA correctly: stream/channel-to-peripheral mapping, circular vs normal mode, half-transfer vs transfer-complete callback timing, and cache-coherency on DCache-equipped parts."
sources:
  - https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STM32 DMA configuration and common pitfalls

**Goal:** move data between peripherals and memory without the CPU, correctly
the first time — a layer below the UART-DMA usage pattern already shown in
`computing-software.firmware-embedded-development.stm32.cubemx-hal-project-setup`,
generalized to any peripheral and the failure modes specific to STM32's DMA
controller family.

## Stream/channel-to-peripheral mapping is fixed silicon, not configurable
On F4/F7-era parts, each DMA stream has a fixed table of which peripheral
request lines it can serve (DMA1 Stream 5 Channel 4 might be USART2_RX, for
example) — this mapping is in the reference manual's DMA request mapping
table, not something CubeMX invents; picking a peripheral whose only
available DMA stream is already used by something else forces a redesign of
which stream serves what. H7-series and newer parts use DMAMUX, which
decouples requests from fixed streams and removes most of this constraint —
know which generation you're on before assuming stream assignment is
flexible.

## Circular mode and the half-transfer interrupt
Circular mode re-arms automatically on completion instead of stopping —
essential for continuous peripheral-to-memory capture (audio, ADC streaming)
without CPU re-arming it every buffer. Pair it with the **half-transfer
interrupt** for double-buffering: it fires when DMA has filled the first half
of the buffer, signaling "start processing/draining that half while DMA fills
the second half" — the exact ping-pong pattern referenced in
`computing-software.firmware-embedded-development.device-driver-development.interrupt-driven-driver-architecture`.
Forgetting to disable the half-transfer interrupt when you don't need it
means unnecessary ISR overhead at twice the rate; forgetting to use it when
you do need double-buffering means the processing code races the DMA filling
the same half it's reading.

## Transfer-complete fires before the last byte is necessarily "settled"
On some peripheral/DMA combinations, the transfer-complete interrupt
indicates the DMA engine has issued its last bus transaction, not necessarily
that the peripheral has finished whatever it does with that data (write
posting, FIFO drain) — a buffer read or CS deassertion triggered directly
from this callback can occasionally race the peripheral's own completion,
particularly noticeable on SPI at high clock rates. Check the specific
peripheral's errata/reference manual notes on this interaction before
assuming transfer-complete means "fully done" in every case.

## Cache coherency on DCache-equipped parts (H7, some F7 configurations)
DMA reads/writes main memory directly, bypassing the CPU's data cache. If a
buffer the CPU wrote (and which sits in cache) is then read by DMA, DMA can
see stale data unless the cache is explicitly cleaned (`SCB_CleanDCache_by_Addr`)
before the DMA transfer starts; conversely, data DMA wrote into memory can be
invisible to the CPU reading through a stale cache line unless it's
invalidated (`SCB_InvalidateDCache_by_Addr`) after the transfer completes.
This is one of the most common "DMA transfer works on F4 (no cache) but
corrupts data on H7 (cache)" porting bugs — alternatively, place DMA buffers
in a non-cacheable memory region (MPU-configured) to sidestep manual
clean/invalidate calls entirely, at some cost to CPU access speed for that
region.

## Verify
- [ ] DMA stream/channel assignment matches the reference manual's fixed request-mapping table for this exact part (pre-DMAMUX generations).
- [ ] Circular-mode buffers with double-buffering use the half-transfer interrupt correctly, verified with the processing side never reading the half still being written.
- [ ] Transfer-complete-triggered actions (CS deassert, buffer handoff) were checked against the specific peripheral's documented completion semantics.
- [ ] On DCache-equipped parts, DMA buffers are either in a non-cacheable MPU region or explicitly clean/invalidated around every transfer, confirmed by a test that would fail on stale cache data.
