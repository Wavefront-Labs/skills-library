---
id: computing-software.firmware-embedded-development.zephyr.network-buffer-sizing
name: network-buffer-sizing
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [net-buf-pool, net-pkt-rx-count, net-buf-data-size, net-mem-stats, network-memory-tuning, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Size Zephyr networking memory: net_pkt and net_buf counts, buffer data size, TCP windows, and diagnosing drops and allocation failures with net mem and stats."
sources:
  - https://docs.zephyrproject.org/latest/connectivity/networking/api/net_pkt.html
  - https://docs.zephyrproject.org/latest/connectivity/networking/net-stack-architecture.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/ip/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/ip/Kconfig.tcp
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/lib/net_buf/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network buffer sizing

Zephyr's IP stack holds packets as a `net_pkt` (metadata) plus a chain of `net_buf` fragments
(data). Both come from fixed pools sized by Kconfig.

## Key options
Defaults are 14 RX and 14 TX packets and 36 RX and 36 TX buffers with Ethernet (4 and 16 without it),
and a 128-byte fragment. Illustrative values:
```
CONFIG_NET_PKT_RX_COUNT=16        # RX packet headers
CONFIG_NET_PKT_TX_COUNT=16
CONFIG_NET_BUF_RX_COUNT=48        # RX data fragments
CONFIG_NET_BUF_TX_COUNT=48
CONFIG_NET_BUF_DATA_SIZE=128      # bytes per fragment (fixed-size mode)
# or variable-size:
CONFIG_NET_BUF_VARIABLE_DATA_SIZE=y    # marked EXPERIMENTAL in Kconfig
CONFIG_NET_PKT_BUF_RX_DATA_POOL_SIZE=8192
CONFIG_NET_PKT_BUF_TX_DATA_POOL_SIZE=8192
```
A 1514-byte Ethernet frame with 128-byte fragments needs 12 net_bufs; so `NET_BUF_RX_COUNT` must
be roughly `packets_in_flight * ceil(MTU / DATA_SIZE)`.

## TCP
```
CONFIG_NET_TCP_MAX_RECV_WINDOW_SIZE=...   # 0 (default) = stack picks from the buffer count; range 0..65535
CONFIG_NET_TCP_MAX_SEND_WINDOW_SIZE=...   # 0 (default) = stack picks
CONFIG_NET_MAX_CONN / CONFIG_NET_MAX_CONTEXTS   # connections / network contexts
```
The Kconfig help says a larger receive window can improve throughput but needs more receive
buffers; the default lets the stack derive it from the configured buffer count. Throughput is
roughly window / RTT, so a 2 KB window on a 50 ms link caps at 40 KB/s.

## Diagnose
```
CONFIG_NET_STATISTICS=y
CONFIG_NET_SHELL=y
CONFIG_NET_BUF_POOL_USAGE=y
```
```
uart:~$ net mem          # pools: total, free (and minimum free with POOL_USAGE)
uart:~$ net stats        # drops by layer, TCP retransmits
uart:~$ net allocs       # outstanding allocations (CONFIG_NET_DEBUG_NET_PKT_ALLOC)
```
Log lines like `Data buffer (<n>) allocation failed` mean the pools are
too small for the load, or something leaks (an app holding `net_pkt`s, e.g. not reading sockets).

## Tuning procedure
1. Run worst-case traffic (iperf via `zperf` sample, bulk TLS download).
2. Watch `net mem` minimum free; keep 20-30 percent headroom.
3. Raise the exhausted pool; prefer more buffers to bigger windows on RAM-limited parts.
4. Variable-size data pools (`CONFIG_NET_BUF_VARIABLE_DATA_SIZE`, experimental) allocate each buffer
   from the size requested at run time, which can suit mixed packet sizes.

## Verify
- [ ] `net mem` minimum-free headroom recorded under worst-case load.
- [ ] No allocation-failure logs during a 24 h traffic soak.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed in the Kconfig files: NET_PKT_RX_COUNT/TX_COUNT (defaults 14 with Ethernet, else 4), NET_BUF_RX_COUNT/TX_COUNT (36 with Ethernet, else 16), NET_BUF_DATA_SIZE (128, fixed-size mode), NET_BUF_VARIABLE_DATA_SIZE (EXPERIMENTAL), NET_PKT_BUF_RX/TX_DATA_POOL_SIZE (variable-size mode), NET_TCP_MAX_RECV_WINDOW_SIZE and SEND window (default 0, range 0 to 65535, help text on buffers), NET_MAX_CONN, NET_MAX_CONTEXTS, NET_STATISTICS, NET_SHELL, NET_BUF_POOL_USAGE, NET_DEBUG_NET_PKT_ALLOC; shell commands `net mem`, `net stats`, `net allocs` exist in subsys/net/lib/shell; the log text "Data buffer (%zu) allocation failed" is in net_pkt.c. Arithmetic checked: ceil(1514/128) = 12 fragments; 2048 bytes / 0.05 s = 40.96 KB/s.
Removed: the "Cannot allocate rx pkt" message (not found in the sources) and the Bluetooth, offload and Wi-Fi buffer remarks, which no documentation confirms.

Method: documentation only; no commands were run.
