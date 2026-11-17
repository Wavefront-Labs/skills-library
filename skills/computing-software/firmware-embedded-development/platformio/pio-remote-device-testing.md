---
id: computing-software.firmware-embedded-development.platformio.pio-remote-device-testing
name: pio-remote-device-testing
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [pio-ci, pio-remote, remote-agent, remote-upload, remote-test, device-farm, hardware-ci, platformio, firmware-embedded-development]
level: advanced
status: draft
description: "Use PlatformIO Remote to upload, monitor and run on-target tests on boards attached to another machine, building a small hardware-in-the-loop farm for CI."
sources:
  - https://docs.platformio.org/en/latest/plus/pio-remote.html
  - https://docs.platformio.org/en/latest/core/userguide/remote/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PlatformIO Remote device testing

**Goal:** run uploads and `pio test` against real boards plugged into a lab machine from your
laptop or CI, without sharing USB over the network yourself.

## Pieces
- **Agent** on the machine with the boards: `pio remote agent start --name lab-pi-1`
  (run as a service; needs a PlatformIO account login: `pio account login`).
- **Client** anywhere: commands prefixed with `pio remote`.
```
pio remote agent list                       # which agents are online
pio remote device list                      # serial ports on agents
pio remote run -e board -t upload           # builds locally, uploads via the agent
pio remote device monitor --agent lab-pi-1 -p /dev/ttyACM0 -b 115200
pio remote test -e board --upload-port /dev/ttyACM0   # build here, flash + test there
```
`-r` / `--force-remote` builds on the agent instead of locally (agent needs the toolchains).

## CI usage
- Store a PlatformIO account token as a CI secret (`PLATFORMIO_AUTH_TOKEN` env var) instead of
  interactive login.
- Pin each job to an agent and port (`--agent`, `--upload-port`) so parallel jobs don't fight
  over one board; or serialise hardware jobs with a CI concurrency group.
- Put boards behind a USB hub with per-port power control (uhubctl) and a debug probe, so CI
  can power-cycle a hung board before each run.

## Gotchas
- Serial port names change after reboots on Linux: use udev symlinks
  (`/dev/serial/by-id/...` or a rule creating `/dev/board-a`).
- On-target tests need a reliable reset after upload; boards with native USB re-enumerate and
  the port briefly disappears, set `test_port`/`upload_port` explicitly and `test_speed`.
- Remote relies on PlatformIO's cloud relay; check availability and data policies for your
  organisation. Self-hosted alternatives: a CI runner on the lab machine (GitHub self-hosted
  runner with the boards attached) achieves the same with plain `pio test`.

## Verify
- [ ] `pio remote test` passes from a second machine against the lab board.
- [ ] CI job fails (not hangs) when the board is unplugged (timeouts configured).
