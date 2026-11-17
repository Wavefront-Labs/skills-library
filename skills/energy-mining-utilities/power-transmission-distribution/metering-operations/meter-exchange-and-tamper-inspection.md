---
id: energy-mining-utilities.power-transmission-distribution.metering-operations.meter-exchange-and-tamper-inspection
name: meter-exchange-and-tamper-inspection
category: energy-mining-utilities
field: power-transmission-distribution
product: metering-operations
tags: [metering-operations, metering, meter-exchange, meter-replacement, smart-meter, ami, amr, smart-meter-installation, socket-meter, ansi-meter-socket, bottom-connected-meter, single-phase-meter, whole-current-meter, ct-metering, meter-seal, tamper-detection, revenue-protection, energy-theft, bypass, meter-bypass, reverse-energy, line-load-reversal, head-end, commissioning, final-read, arc-flash, meter-puller]
level: practitioner
status: draft
description: "Swap a whole-current electricity meter safely and spot tampering: final read and seal check, pulling or disconnecting under load, line/load polarity, commissioning to the AMI head-end."
sources:
  - "General utility metering field practice for socket (ANSI) and bottom-connected (IEC/BS) meters; paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Meter exchange and tamper inspection

**Goal:** replace a domestic or small-commercial whole-current meter so the customer
is billed correctly from the first minute, with evidence captured if the old meter
was interfered with. Two physical meter worlds exist: **socket meters** (North
American ANSI style — the meter plugs into jaws) and **bottom-connected meters**
(IEC/BS style — wired to a terminal block). Steps differ; principles don't.
CT-connected meters (large loads) need their own procedure: never open-circuit a CT.

## 1. Arrive and look before touching
- Photograph the installation **as found**: meter face and display, serial number,
  seals, socket or terminal cover, surrounding wiring.
- Record the **final read(s)** — every register (import, export, time-of-use bands).
  Many utilities need a photo of the display as evidence.
- **Seal check:** seals present, intact, the right type and number matching records.
  A broken or wrong seal is the first tamper flag.

## 2. Tamper and theft indicators
- **Bypass:** extra conductors or jumpers around the meter, inside the socket, or
  a tap ahead of the meter (look at the service cable entry).
- **Meter interference:** drilled cases, foreign objects, magnets on the meter case,
  a meter installed upside down (old electromechanical meters) or line/load swapped.
- **Inconsistency:** consumption far below what the visible appliances, heating or
  premises size would suggest; a meter not advancing with load on.
- **Heat damage** to sockets or terminals — burned jaws are both a theft clue
  (poor bypass connections) and a fire risk.
If you find signs of theft: stop, don't disturb evidence, photograph, follow the
revenue-protection procedure. Don't confront the customer. In some places a
dangerous bypass means you must make the installation safe immediately.

## 3. Removing the meter
**Socket meters:** confirm the socket is rated for meter removal under load (some
need the main switched off first). Wear arc-rated face protection and gloves; use a
meter puller and pull straight out — rocking draws arcs. Fit a blank cover if the
customer will be off for any time.
**Bottom-connected meters:** isolate at the cutout or service fuse (or the
isolator if fitted), prove dead at the meter terminals with a proved tester, then
disconnect. Loose or overheated terminals are common — note them.

## 4. Fitting the new meter
- Check model, rating and configuration (single/multi-phase, export capability,
  tariff programme) match the job.
- Bottom-connected: terminate **line in / line out / neutral** exactly as the
  terminal diagram shows; torque to the meter's spec. **Line/load reversal** can make
  the meter record import as export, or leave the meter energised from the wrong side.
- Socket: inspect jaws for tension and damage before inserting; seat fully.
- Fit new seals and record their numbers.

## 5. Commissioning
- Restore supply; the meter should power up and pass its display self-test.
- **Load test:** apply a known load (a kettle or heater) and confirm the meter
  registers import, the right phase, and roughly the right kW.
- Check the customer's supply works (lights on, no tripped devices) and any solar
  inverter reconnects.
- Smart meters: confirm the meter **joins the communications network** and the
  head-end receives an initial read before you leave, or log it for follow-up.

## 6. Records
Old and new serial numbers, final and initial reads, seal numbers, photos and any
defects or tamper findings go into the job record. A missing final read is a billing
dispute waiting to happen.

## Verify
- [ ] As-found photos, final reads of every register and seal numbers recorded.
- [ ] Tamper indicators checked; any found handled under the procedure.
- [ ] Meter removed with correct isolation/arc PPE; terminals inspected.
- [ ] Wiring polarity correct and torqued; new seals recorded.
- [ ] Load test shows import; meter visible to the head-end.
