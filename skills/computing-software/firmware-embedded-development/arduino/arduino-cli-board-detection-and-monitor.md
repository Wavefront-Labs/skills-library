---
id: computing-software.firmware-embedded-development.arduino.arduino-cli-board-detection-and-monitor
name: arduino-cli-board-detection-and-monitor
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-cli-monitor, board-list, serial-monitor, monitor-config, pluggable-discovery, upload-port, arduino-cli, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Find boards and talk to them with arduino-cli: board list/attach, pluggable discovery, monitor baud and settings, DTR/RTS reset behaviour, and scripting serial capture."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/monitor/monitor.go
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/board/list.go
  - https://github.com/arduino/serial-monitor/blob/main/main.go
  - https://github.com/arduino/arduino-cli/blob/master/docs/platform-specification.md
  - https://github.com/arduino/arduino-cli/blob/master/docs/pluggable-discovery-specification.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Board detection and serial monitor (arduino-cli)

## Detect
```sh
arduino-cli board list                      # port, protocol, board name, FQBN (if recognised)
arduino-cli board list --format json        # for scripts: matching_boards[].fqbn, port.address
arduino-cli board list --watch              # live attach/detach events
arduino-cli board listall esp32             # all FQBNs from installed cores
arduino-cli board details -b esp32:esp32:esp32s3   # menu options (PSRAM, partitions, USB mode)
```
Boards are matched by USB VID/PID from installed cores. Boards that are not recognised have no FQBN: pass `-b` explicitly. Discovery is pluggable
(see the pluggable discovery specification).

## Upload to a specific port
```sh
arduino-cli upload -p /dev/ttyACM0 -b arduino:samd:mkrwifi1010 --input-dir build/
arduino-cli compile -u -p COM5 -b arduino:avr:uno sketch/     # compile then upload
```
Boards whose platform sets `upload.use_1200bps_touch=true` get a brief 1200 bps open of the port before upload, and with `upload.wait_for_upload_port=true` the upload waits for the port to reappear (platform specification).

## Monitor
```sh
arduino-cli monitor -p /dev/ttyUSB0 --config 115200
arduino-cli monitor -p COM5 --config baudrate=115200,parity=none,bits=8,stop_bits=1,dtr=off,rts=off
arduino-cli monitor -p /dev/ttyACM0 --describe          # list supported settings
arduino-cli monitor -p /dev/ttyACM0 -q --raw > log.txt   # quiet/raw for capture
```
- Opening the port asserts DTR on many boards, resetting an Uno/ESP32 (auto-reset circuit). Use
  `dtr=off,rts=off` to attach without reset (test per board).
- `--timestamp` adds a timestamp to each incoming line.
- Only one program can open a serial port; close the monitor before uploading.

## Scripting
For automated tests, prefer pyserial or `pytest-embedded` reading the port, using `board list
--format json` to locate it by VID/PID or serial number (`port.properties.serialNumber`).

## Verify
- [ ] Script finds the board by serial number, uploads, and captures boot output.
- [ ] Monitor settings documented per board (baud, reset behaviour).

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 source and docs on master (commit 2026-10-22); arduino/serial-monitor main.

Confirmed: `board list --watch`; JSON output has `matching_boards` and port `serialNumber`; `monitor` flags `--config/-c` (`<ID>=<value>` list, a bare `115200` is used in the CLI's own example), `--describe`, `--quiet`, `--raw`, `--timestamp`; serial monitor setting ids `baudrate`, `parity` (none, even, odd, mark, space), `bits`, `stop_bits`, `dtr` and `rts` (on or off); `use_1200bps_touch` and `wait_for_upload_port` platform properties. Removed unconfirmed claims: the CH340/CP2102 "Unknown" remark, the named discoveries and vendor tools, and the ESP32 EN/IO0 remark.

Method: documentation only; no commands were run.
