---
id: computing-software.firmware-embedded-development.device-driver-development.socketcan-on-linux
name: socketcan-on-linux
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [socketcan, can-bus, can-utils, ip-link-can, raw-can-socket, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Bring up and use CAN on Linux with SocketCAN: ip link bitrate/FD settings, can-utils (candump, cansend, cangen), raw sockets with filters, vcan, and error frame reporting."
sources:
  - https://docs.kernel.org/networking/can.html
  - https://github.com/linux-can/can-utils
  - https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/net/can/microchip,mcp2510.yaml
  - https://man7.org/linux/man-pages/man8/ip-link.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SocketCAN on Linux

SocketCAN exposes CAN controllers as network interfaces (`can0`): USB adapters, SPI controllers (MCP2515/MCP251xFD via device tree), and SoC controllers.

## Bring-up
```sh
sudo ip link set can0 type can bitrate 500000 sample-point 0.875 restart-ms 100
sudo ip link set can0 up
ip -details -statistics link show can0        # state ERROR-ACTIVE/PASSIVE/BUS-OFF, counters, bit timing
# CAN FD
sudo ip link set can0 type can bitrate 500000 dbitrate 2000000 fd on
# virtual bus for tests
sudo modprobe vcan && sudo ip link add dev vcan0 type vcan && sudo ip link set vcan0 up
```
`restart-ms` re-enables the controller automatically after bus-off; without it, bus-off is
permanent until `ip link set can0 type can restart`.

## can-utils
```sh
candump -tA -x can0                 # absolute timestamps with date, extra details (RX/TX, BRS/ESI flags)
candump can0,123:7FF                # filter: ID 0x123 only
candump -l can0                     # log to candump-<date>.log; replay with canplayer -I file.log
cansend can0 123#DEADBEEF           # classic frame
cansend can0 1F334455#1122          # 29-bit ID (8 hex digits)
cansend can0 123##1.112233445566778899AA   # CAN FD, flags 1 = BRS
cangen can0 -g 1 -I r -L 8          # random load generator
canbusload can0@500000 -r           # bus load %
```

## Raw socket in C
```c
int s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
struct ifreq ifr; strcpy(ifr.ifr_name, "can0"); ioctl(s, SIOCGIFINDEX, &ifr);
struct sockaddr_can addr = { .can_family = AF_CAN, .can_ifindex = ifr.ifr_ifindex };
bind(s, (struct sockaddr *)&addr, sizeof addr);
struct can_filter f = { .can_id = 0x123, .can_mask = CAN_SFF_MASK };
setsockopt(s, SOL_CAN_RAW, CAN_RAW_FILTER, &f, sizeof f);
can_err_mask_t em = CAN_ERR_MASK;  setsockopt(s, SOL_CAN_RAW, CAN_RAW_ERR_FILTER, &em, sizeof em);
struct can_frame fr; read(s, &fr, sizeof fr);       /* error frames have CAN_ERR_FLAG in can_id */
```
Use `CAN_RAW_FD_FRAMES` and `struct canfd_frame` for FD. Python: `python-can` with
`interface='socketcan'`.

## Gotchas
- `write()` can fail with `ENOBUFS` when the interface cannot queue more frames (`cangen -i` ignores it).
  Look for the cause on the bus (no ACK, bus-off) before changing queue sizes.
- Wrong bit rate shows up as bus errors in `ip -s link` and error frames in `candump -e`.
- MCP2515 on SPI needs the oscillator described in the device tree node's `clocks` property,
  with the real crystal frequency, or every bit rate is off.

## Verify
- [ ] `ip -details link show can0` shows the intended bitrate and sample point.
- [ ] `cansend` on one node appears in `candump` on another, with zero error counters.

## Checked

2026-10-27, Linux kernel documentation (mainline v7.3) and can-utils master.
Confirmed in Documentation/networking/can.rst: ip link set can0 type can options (bitrate, sample-point, dbitrate, fd on, restart-ms, restart), the ERROR-ACTIVE/ERROR-PASSIVE/BUS-OFF state display, restart-ms re-starting after bus-off (off by default), ip link add type vcan, CAN_RAW_ERR_FILTER with CAN_ERR_MASK, CAN_RAW_FD_FRAMES, CAN_FILTER can_id/can_mask with CAN_SFF_MASK, and the SIOCGIFINDEX bind sequence. Confirmed in can-utils source: candump -t A (absolute with date), -x, -l, -e and the id:mask filter, candump-<date>.log naming, cansend 3 or 8 hex digit IDs and the ## flags form (1 = BRS), cangen -g/-I/-L/-i with 'r' random mode, canbusload ifname@bitrate and -r, canplayer -I. Confirmed in the mcp2510 binding that the oscillator is given with clocks. Removed the unconfirmed USB adapter vendor list, the oscillator-frequency property name and the txqueuelen advice.

Method: documentation only; no commands were run.
