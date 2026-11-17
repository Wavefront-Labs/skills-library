---
id: computing-software.firmware-embedded-development.device-driver-development.i2c-multi-master-arbitration
name: i2c-multi-master-arbitration
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [i2c-arbitration, multi-master, arbitration-lost, clock-synchronization, bus-busy, i2c-driver, smbus, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run multiple I2C controllers on one bus: wired-AND arbitration and clock sync, handling arbitration-lost and bus-busy, retry policy, and cases arbitration cannot resolve."
sources:
  - https://www.nxp.com/docs/en/user-guide/UM10204.pdf
  - http://smbus.org/specs/SMBus_3_2_20220112.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# I2C multi-master arbitration

**Goal:** two or more controllers (the I2C specification's current term for masters) share an I2C
bus without corrupting each other's transfers.

## How arbitration works (UM10204 sections 3.1.7 and 3.1.8)
- SDA and SCL are open-drain, wired-AND. A controller may start a transfer only if the bus is
  free. Two controllers can generate a START within the minimum hold time (tHD;STA) and both
  get a valid START; arbitration then decides who completes.
- Arbitration proceeds bit by bit. While SCL is HIGH each controller checks that the SDA level
  matches what it sent. The first time a controller tries to send a HIGH but sees SDA LOW, it
  has lost arbitration and turns off its SDA output driver. The other controller completes its
  transaction; no information is lost.
- A controller that loses can keep generating clock pulses until the end of the byte in which it
  lost, and must restart its transaction when the bus is free.
- Control is decided solely by the address and data sent, so there is no central controller and
  no order of priority.
- Two controllers can complete a whole transaction without error as long as their transmissions
  are identical.
- Clock synchronisation: the synchronised SCL has its LOW period set by the controller with the
  longest LOW period and its HIGH period set by the one with the shortest HIGH period.
- Targets are not involved in arbitration.

## Driver handling
1. Before START, check the hardware bus-busy state; do not start while the bus is busy.
2. On an arbitration-lost interrupt or status flag, clear it, abandon the transfer and return a
   retryable error (for example `-EAGAIN`). Check your controller's reference manual for the
   flag name and whether the peripheral already released the lines.
3. Retry once the bus is idle, with a bounded retry count and some randomised backoff.
4. If the controller also has a target function and loses during the addressing stage, it must
   switch to target mode immediately, because the winner may be addressing it.

## Cases arbitration cannot resolve
UM10204 lists these as undefined conditions: while arbitration is still in progress,
- controller 1 sends a repeated START and controller 2 sends a data bit;
- controller 1 sends a STOP and controller 2 sends a data bit;
- controller 1 sends a repeated START and controller 2 sends a STOP.
Design the protocol so controllers do not access the same device in conflicting ways.

## Stuck bus
If SDA is stuck LOW, the controller should send nine clock pulses; the device holding the bus
should release it within those nine clocks (UM10204 3.1.16). If not, use the hardware reset or
cycle power. If SCL is stuck LOW, reset the bus with a hardware reset signal if the devices have
one, otherwise cycle power.

## SMBus
SMBus 3.2 defines a clock-low timeout (tTIMEOUT) so devices can recover from a bus held low: the
timing table gives 25 ms minimum and 35 ms maximum. A device that detects a clock held low
longer than tTIMEOUT,MIN should release the bus, and must be able to receive a new START by
tTIMEOUT,MAX.

## Design advice
- Prefer avoiding multi-master where you can: separate buses, or a sideband request/grant GPIO.
- Every controller must support arbitration in hardware; a bit-banged controller must implement
  the SDA check on every bit.
- Keep transactions short so retries are cheap, and re-read state if arbitration was lost during
  a write rather than assuming it happened.

## Verify
- [ ] Stress test with both controllers hammering the bus: the only errors are arbitration-lost
      with successful retries, and a logic analyser decodes no malformed frames.
- [ ] Device registers end in a consistent state after the stress run.

## Checked
2026-11-09. Read: NXP UM10204 Rev 7.0 sections 3.1.7 (clock synchronisation), 3.1.8
(arbitration, undefined conditions), 3.1.16 (bus clear), and the SMBus 3.2 specification
device-timeout text and AC table (tTIMEOUT 25 to 35 ms). Corrected: a losing controller may
keep clocking to the end of the byte (the skill said it must switch off its clock immediately),
and the SMBus timeout is 25 to 35 ms, not a flat 35 ms. Removed: STM32 ARLO and NXP ALF flag
names, the nRF TWIM statement, the PCA9541 selector, and the slva704 source (not used).
Method: docs-checked 2026-11-09 against UM10204 Rev 7.0 and SMBus Specification 3.2.
