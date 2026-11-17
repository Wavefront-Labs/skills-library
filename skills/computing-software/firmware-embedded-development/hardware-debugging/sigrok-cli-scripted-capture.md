---
id: computing-software.firmware-embedded-development.hardware-debugging.sigrok-cli-scripted-capture
name: sigrok-cli-scripted-capture
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [sigrok-cli, sigrok, pulseview, logic-analyzer, protocol-decoder, fx2lafw, automated-capture, hil-testing, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Automate logic analyzer captures with sigrok-cli: scanning devices, sample rate and channel config, triggers, protocol decoders, annotation filters and output formats."
sources:
  - https://sigrok.org/wiki/Sigrok-cli
  - https://sigrok.org/wiki/Protocol_decoders
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scripted capture with sigrok-cli

**Goal:** capture and decode bus traffic from a script (bench regression, HIL test, CI) with supported logic analysers,
instead of clicking through a GUI. The sigrok-cli man page on the wiki is dated October 2018, so check
`sigrok-cli --version` and `-L` on your install for current options.

## Find the device
```sh
sigrok-cli --scan                       # lists auto-detectable devices and their channel names
sigrok-cli --driver fx2lafw --show      # device options, supported samplerates, channel names and triggers
sigrok-cli -L                           # supported drivers, input and output formats, protocol decoders
```
Serial-port devices are not auto-detectable; give the `conn` option, for example
`--driver ols:conn=/dev/ttyACM0`. USB devices without a unique ID use `conn=VID.PID` or `conn=bus.address`.

## Capture
```sh
sigrok-cli -d fx2lafw --config samplerate=1m --channels 0-3 --time 2s -o capture.sr
sigrok-cli -d fx2lafw --config samplerate=1m --channels 1=SCL,2=SDA --triggers SDA=f --wait-trigger --samples 3m -o i2c.sr
```
- `--config samplerate=` takes Hz or `k`/`m`/`g` forms (`1m`, `"1 MHz"`).
- Stop conditions: `--time <ms>` (suffix `s` for seconds), `--samples <n>` (suffix k/m/g), `--frames <n>`, or
  `--continuous` (not supported by all devices).
- Triggers are `<channel>=<trigger>` with `0`, `1`, `r` (rising), `f` (falling), `e` (either edge). Not every device
  supports every type; `--show` lists what yours supports. `--wait-trigger` discards pre-trigger data.
- Name channels with `--channels 1=CLK,2-4,7`; the list is processed left to right, later items override earlier ones.
  Channel numbers are those printed on the hardware.
- Output defaults to the sigrok session format (`.sr`, which PulseView opens); change it with `-O <format>`, for example
  `-O csv`, `-O bits`, `-O hex:width=128`.
- Capture first and decode later. The wiki warns sigrok-cli is single-threaded and heavy load causes early
  termination; for high sample rates use the binary output format, optionally with a buffer.

## Decode
```sh
sigrok-cli -i i2c.sr -P i2c -A i2c=address-read:address-write:data-read:data-write
sigrok-cli -i uart.sr -P uart:baudrate=115200:rx=0 -A uart
sigrok-cli -i uart.sr -P uart:baudrate=115200:rx=0 -B uart=rx > rx.bin     # raw decoder output
sigrok-cli -i spi.sr -P spi:clk=0:mosi=1:miso=2:cs=3 -A spi
```
- Decoder options and channel assignments are `key=value` pairs separated by colons. Anything that is not a decoder
  option is read as a channel assignment. There is no name matching: signals follow the decoder's input order unless
  assigned explicitly.
- Stack decoders with commas in one `-P` (`i2c,eeprom24xx`); several `-P` options create parallel stacks.
- `-A decoder=class1:class2` filters annotation classes; `-B decoder=class` writes the decoder's binary output (only
  some decoders have it) so it can be piped or saved; `--protocol-decoder-samplenum` adds sample numbers.
- `--protocol-decoders <id> --show` lists a decoder's options.

## Automation
- Exit status is 0 on success and 1 on most failures, so a script can check it.
- Capture during a stimulus, decode with `-B` or `-A`, then assert on the output in your test harness.

## Gotchas
- Sample fast enough for the bus you decode; check the device's samplerates with `--show`.
- Firmware for fx2lafw-based devices comes from the sigrok firmware packages (see sigrok Downloads).

## Verify
- [ ] A known UART "Hello" stream decodes correctly from the script.
- [ ] The script fails (non-zero) when the decoded-data assertion fails.

## Checked
Method: docs-checked 2026-11-09 against the sigrok wiki page Sigrok-cli (read in full, including the embedded man page) and the Protocol decoders list (fetched; only used to confirm decoder IDs exist). The sigrok.org/doc/sigrok-cli.1.html URL returned 404 and was dropped. Removed unconfirmed claims: FX2 throughput figures, 4x-10x sampling rule, VCD and ASCII output formats, pysigrok and Python bindings, level-threshold and grounding notes, `-L`/`--show` for decoders by other spelling.
