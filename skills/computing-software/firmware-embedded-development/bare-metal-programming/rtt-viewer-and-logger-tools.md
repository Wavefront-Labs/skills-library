---
id: computing-software.firmware-embedded-development.bare-metal-programming.rtt-viewer-and-logger-tools
name: rtt-viewer-and-logger-tools
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [rtt-viewer, segger-rtt, jlinkrttlogger, openocd-rtt, probe-rs-rtt, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Read SEGGER RTT output on the host with J-Link RTT Viewer/Logger/Client, the OpenOCD rtt server or probe-rs, including control block search and blocking modes."
sources:
  - https://kb.segger.com/RTT
  - https://openocd.org/doc/html/General-Commands.html
  - https://probe.rs/docs/tools/probe-rs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RTT viewer and logger tools

RTT puts ring buffers in target RAM; the debug probe reads them in the background while the core
runs. The host side needs to find the RTT control block (`_SEGGER_RTT`) and poll it.

## J-Link tools
SEGGER provides J-Link RTT Viewer (several "virtual" terminals over one target buffer), J-Link
RTT Logger and J-Link RTT Client. While a J-Link connection is active (for example a debug
session), the J-Link software also opens a TELNET-like channel on localhost port 19021 (default)
that a Telnet client or your own application can use; the RTT channel is picked with a SEGGER
TELNET config string and defaults to channel 0.
- Only one application on the host should fetch RTT data: running several in parallel (for
  example Viewer and Client) lets one steal data from the other.
- The control block address, or the address ranges to search, can be set with J-Link command
  strings or in the RTT Viewer configuration dialog.

## OpenOCD
```tcl
rtt setup 0x20000000 2048          ;# address and size of the area to search
rtt start
rtt server start 9090 0            ;# TCP port and RTT channel
```
`rtt setup address size [ID]`; the OpenOCD manual's own example uses exactly these values. Connect a
TCP client (telnet or netcat) to the port. Use the exact address of the control block, taken from
your map file or symbol table, with a small size to make the search fast.

## probe-rs
`probe-rs attach` works like `probe-rs run` except that it does not reset or flash the target,
preserving the running state. See the probe-rs documentation for the RTT options of `run` and `attach`.

## Control block not found
- The search range does not cover the block's address (e.g. block in a different RAM region).
- Cache: SEGGER says `SEGGER_RTT_CPU_CACHE_LINE_SIZE` must be specified if the cache line size
  is larger than 32 bytes, so the control block and buffer 0 meet the alignment requirements.

## Throughput and blocking
SEGGER lists the buffer modes: `SEGGER_RTT_MODE_NO_BLOCK_SKIP` (nothing is written if the up
buffer lacks space), `SEGGER_RTT_MODE_NO_BLOCK_TRIM` (fills the available space, discards the
excess) and `SEGGER_RTT_MODE_BLOCK_IF_FIFO_FULL` (the writing call blocks when the buffer is
full). Every mode except the blocking one may lose data if the target writes faster than the
host reads. A blocking write with no host attached stalls the target, so do not ship it.
`BUFFER_SIZE_UP` sets the size of up channel 0; SEGGER recommends 1 kByte for up channels.

## Verify
- [ ] Log lines appear with the target running at full speed, no halts.
- [ ] Target runs normally with no probe attached (non-blocking mode).

## Checked
2026-10-31. Confirmed on the SEGGER RTT knowledge base page: viewer/logger/client tools, port 19021,
single-reader warning, buffer modes, `SEGGER_RTT_CPU_CACHE_LINE_SIZE`, `BUFFER_SIZE_UP`, size recommendation.
Confirmed in the OpenOCD manual: `rtt setup`, `rtt start`, `rtt server start`. Confirmed on the probe-rs page: `attach` behaviour.
Removed: JLinkRTTLogger/JLinkExe flags and device names, the `SEGGER_RTT_Init()` and `.bss` claims, pyOCD, the
Cortex-M7 DTCM advice, the ID-string duplicate claim, and the "default mode" claim.
Method: documentation only; no commands were run.
