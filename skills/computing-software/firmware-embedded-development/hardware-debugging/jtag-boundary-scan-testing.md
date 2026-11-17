---
id: computing-software.firmware-embedded-development.hardware-debugging.jtag-boundary-scan-testing
name: jtag-boundary-scan-testing
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [board-bring-up, boundary-scan, ieee-1149-1, bsdl, interconnect-test, jtag-chain, svf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Test board interconnects with JTAG boundary scan (IEEE 1149.1): BSR cells, BSDL files, connection tests, non-JTAG parts, and OpenOCD SVF support."
sources:
  - https://standards.ieee.org/ieee/1149.1/4484/
  - https://www.xjtag.com/about-jtag/what-is-jtag/
  - https://openocd.org/doc/html/Boundary-Scan-Commands.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JTAG boundary scan testing

**Goal:** check solder joints and nets of BGAs and fine-pitch parts on boards with no working firmware yet, or as a
production test without functional firmware.

## Concept
- JTAG here means the boundary scan architecture of IEEE 1149.1: the Test Access Port (TAP) and its registers. The TAP
  signals are TCK, TMS, TDI, TDO plus an optional TRST*, and they let devices be chained in a scan chain.
- The Boundary Scan Register (BSR) has cells at the boundary of each device, between the functional core and the
  pins or balls, so each pin can be independently driven or sampled in test mode.
- Cells have a functional mode (no effect on the device, used when the board runs normally) and a test mode that
  disconnects the core from the pins. In test mode you control the value driven onto a net and monitor it, with no
  device configuration or booting needed.
- IEEE 1149.1-2013 is listed by IEEE as "Inactive-Reserved" with a purchase-by-subscription page, so the standard text
  is not freely readable here; the P1149.1 project page describes its scope (interconnect testing, testing the IC
  itself, and observing or loading data during test, programming, configuration or debug).

## What you need
- A BSDL (Boundary Scan Description Language) file for each device. XJTAG states BSDL files must be made available by
  the silicon vendor for a device to be compliant with 1149.1.
- A JTAG chain on the board with the TAP signals routed to a header (most boards already have one for programming or
  debug).
- The board netlist, so a tool can generate connection tests automatically.

## Connection test
Per XJTAG, a connection test checks that the connections around JTAG-enabled devices match the design:
- Where two JTAG pins should be connected, one pin must be controllable from the other.
- Where pins should not be connected, drive one and check the value is not read on the others (short circuits).
- It can also find missing pull resistors and stuck-at faults.

## Non-JTAG devices
Parts such as RAM, flash, PHYs, sensors, RTCs and ADCs are not scan-capable. A connection test still gives good
coverage for shorts on their nets, but it cannot detect open circuits at either end. To cover opens, communicate with
the peripheral through a JTAG-enabled device: if communication works there is no open. This can be as simple as
lighting an LED, or as thorough as writing and reading back a RAM array.

## Tools
- Commercial boundary-scan systems import netlist plus BSDL and generate tests (XJTAG is one; its library has models
  for non-JTAG parts).
- OpenOCD is mainly an on-chip debugger but includes boundary scan commands: `svf filename [-tap tapname] [-quiet]
  [-nil] [-progress] [-ignore_error] [-noreset] [-addcycles cyclecount]` runs a Serial Vector Format (SVF) file after a
  JTAG reset (`-nil` is a dry run), and `xsvf` does the same for XSVF (not all XSVF commands are supported).

## Practical uses
- Prototype bring-up: find manufacturing defects before system testing and before firmware is complete.
- Production test with only a JTAG controller as hardware; usable throughout the lifecycle, including field
  diagnostics.
- Dead boards: tests can run on any board with a working JTAG interface even if it does not boot.

## Gotchas
- Driving pins in test mode can conflict with other drivers on a net; use the safe values and pin directions the BSDL
  describes.
- Devices whose JTAG access is disabled or locked drop out of the chain; check the part's documentation.

## Verify
- [ ] The chain is detected with the expected devices in order.
- [ ] A connection test flags a deliberately lifted pin or bridged net on a test board.

## Checked
Method: docs-checked 2026-11-09 against the XJTAG page What is JTAG (read in full), the OpenOCD manual page Boundary Scan Commands (read in full) and the IEEE 1149.1 landing page (read in full; standard text is paywalled). Removed unconfirmed claims: SAMPLE/PRELOAD/EXTEST/IDCODE/BYPASS instruction details, SWD-only and STM32 notes, UrJTAG and TopJTAG commands, other vendors, SPI-flash programming through scan pins, compliance-enable pins.
