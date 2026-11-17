---
id: computing-software.firmware-embedded-development.hardware-debugging.orbuculum-swo-tools
name: orbuculum-swo-tools
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [orbuculum, swo, itm, orbcat, orbtop, orbmortem, tpiu, parallel-trace, hardware-debugging, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Capture and decode SWO/ITM and parallel trace with Orbuculum: the mux server, orbcat channels, orbtop PC sampling, orbmortem, and gdbtrace.init target setup."
sources:
  - https://github.com/orbcode/orbuculum
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Orbuculum SWO tools

Orbuculum is an open-source set of tools for decoding output flows from the trace pins of a
Cortex-M CPU: SWO (UART/NRZ or Manchester/RZ) or parallel TRACE pins through ORBTrace hardware.
Everything below is from the README of version 2.2.0.

## Pieces
- `orbuculum`: the mux. It talks to the trace probe and offers a network interface that any number
  of clients connect to. Configure it for your probe once and leave it running.
- `orbcat`: cat utility for ITM channel data, for example `orbcat -c 0,"%c"`.
- `orbtop`: top-style profiler from Program Counter samples; `orbtop -e firmware.elf` (the elf is
  always needed for symbols).
- `orbmortem`: post-mortem analysis tool; needs a parallel trace source such as ORBTrace Mini
  streaming ETM data (the gdb `startETM` macro); the README says it is not thoroughly tested.
- `orbdump` (raw SWO to file), `orbstat` (statistics, KCacheGrind input), `orbzmq` (ZeroMQ
  publisher), `orblcd` (LCD emulator), `orbtrace` (ORBTrace FPGA controller).

## Sources it supports
Black Magic Probe, SEGGER J-Link, generic USB TTL serial, FTDI high speed serial, OpenOCD, PyOCD,
ECPIX-5 for parallel trace, a raw SWO file, anything offering SWO on a TCP port, and ORBTrace Mini.
With no source options, `orbuculum --monitor 1000` takes input from a Black Magic probe USB SWO feed
or an ORBTrace Mini.

## Ports and protocol
- Orbflow (the packet protocol clients use by default) is carried on TCP 3402; the legacy raw
  stream is on 3443 (3443+x for further TPIU streams).
- Clients default to `localhost:3443` for orbcat (`-s` to change, for example `localhost:2332` for a
  J-Link). For orbtop, if you set the source with `-s` you must also set `-p OFLOW|ITM`.
- TPIU: pass `-T` if your probe does not strip TPIU framing; `-t 1,2` selects tags to reflect over
  the legacy protocol (default stream 1 only). The ITM decoder complains if it sees TPIU syncs and
  you left `-T` off. In parallel trace the TPIU is mandatory and must be stripped by the probe or
  by orbuculum.
- A client that cannot keep up is disconnected and may reconnect (file sources slow down instead).

## Target setup
Trace must be enabled on the target, from code (Orbcode's libtrace) or from gdb. The Support
directory has `gdbtrace.init`; `source` it, then `help orbuculum` lists the macros. The README
example for an STM32F4 on a Black Magic Probe:
```gdb
source Support/gdbtrace.init
enableSTM32SWO 4
monitor traceswo
prepareSWO SystemCoreClock 200000 0 1
dwtSamplePC 1
dwtSyncTap 3
dwtPostTap 1
dwtPostInit 1
dwtPostReset 15
dwtCycEna 1
ITMId 1 ; ITMGTSFreq 3 ; ITMTSPrescale 3 ; ITMTXEna 1 ; ITMSYNCEna 1 ; ITMEna 1
ITMTER 0 0xFFFFFFFF
ITMTPR 0xFFFFFFFF
```
For parallel trace via ORBTrace use `enableSTM32TRACE` instead of the SWO lines and match the trace
width to the FPGA configuration (default four bits). Text output needs your firmware to write ITM
channels (the README shows a CMSIS-style `ITM_SendChar` taking a channel number).

## Profiling with orbtop
- Sampling is set by `dwtSamplePC`, `dwtPostTap`, `dwtPostInit`, `dwtPostReset` and `dwtCycEna`
  (nothing works without `dwtCycEna`). Running too fast floods SWO and can lose channel data;
  too slow can miss short frequent routines, so vary the rate and check results are consistent.
- Change the settings in gdb without restarting orbuculum: interrupt, change, resume.
- `-l` aggregates per line instead of per function; `-E` adds interrupt measurements, which also
  need `dwtTraceException` and `ITMTSEna`. If the debug channel is overfull those data are
  discarded first and are untrustworthy (a V in the flags column).

## OpenOCD as source
The README's older recipe adds `tpiu config internal :3443 uart off 168000000` to the OpenOCD
config (the CPU clock is the last argument) and prints a deprecation notice. Then
`orbcat -s localhost:3443 -c0,"%c"` connects directly. Check the OpenOCD version's TPIU syntax
before copying.

## SWO speed
- In NRZ (UART) mode the rate leaving the chip must match what the probe expects. On a Black Magic
  Probe set it with `monitor traceswo <rate>`; for a TTL serial device set it on the orbuculum
  command line.
- Manchester encoding is autobauding and survives target clock changes (for example low-power
  modes), if the probe supports it.

## Verify
- [ ] `orbcat -c 0,"%c"` prints text from ITM channel 0 in step with firmware events.
- [ ] `orbtop -e firmware.elf` shows hot functions consistent with the known workload.

## Checked
Confirmed from the Orbuculum README (v2.2.0): tool list and roles, supported sources, ports 3402 and
3443, -T, -t, -s and -p behaviour, gdbtrace.init macros and example, orbtop sampling guidance,
orbmortem requirements, the OpenOCD tpiu recipe and Manchester versus NRZ notes. Removed as
unconfirmed: the OpenOCD `tpiu create` syntax and version claim, ST-LINK as a source, the SWO divisor
formula, overflow packet remedies, `orbmortem` MTB claims beyond the README, and the Arm ddi0403 and
orbcode.org sources (not read).

Method: docs-checked 2026-11-09 against the Orbuculum GitHub README (version 2.2.0), read in full.
