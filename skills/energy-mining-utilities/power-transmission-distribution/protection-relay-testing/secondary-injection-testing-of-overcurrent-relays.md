---
id: energy-mining-utilities.power-transmission-distribution.protection-relay-testing.secondary-injection-testing-of-overcurrent-relays
name: secondary-injection-testing-of-overcurrent-relays
category: energy-mining-utilities
field: power-transmission-distribution
product: protection-relay-testing
tags: [protection-relay-testing, protection-testing, relay-testing, secondary-injection, primary-injection, overcurrent, earth-fault, idmt, iec-standard-inverse, ieee-inverse, pickup, drop-off, time-multiplier, tms, time-dial, instantaneous, test-block, test-plug, ct-shorting, ct-open-circuit, trip-isolation, relay-test-set, omicron, megger, doble, numerical-relay, settings-verification, fault-record, disturbance-record, comtrade]
level: advanced
status: draft
description: "Secondary-inject an in-service overcurrent/earth-fault relay safely: isolate trips and short CTs, verify pickup and IDMT times against settings, restore, and read the fault record."
sources:
  - "IEC 60255-151 characteristic equations (standard inverse 0.14/(M^0.02-1)); general protection-testing practice and test-set user manuals, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secondary injection testing of overcurrent relays

**Goal:** prove an overcurrent/earth-fault relay picks up and trips at the times its
approved settings say, without tripping the live feeder or open-circuiting a CT
along the way. The two classic disasters are an **unintended trip** of in-service
plant and an **open-circuited CT secondary** (which can develop lethal voltage and
damage the CT).

## 1. Prepare
- Get the **approved settings file** (the issued version, not "what's in the relay")
  and the scheme drawings. Note CT ratio, pickup, curve, TMS/time dial,
  instantaneous stage and any directional or blocking logic.
- Download the relay's present settings and **compare** them with the approved file
  before testing. Differences are a finding in their own right.
- Agree the outage or "protection out of service" arrangement with control: who else
  protects this circuit while the relay is under test?

## 2. Isolate safely
Use the test block / test plug if fitted; otherwise follow the isolation list on
the drawing.
1. **Isolate trip outputs** first (trip links, test plug fingers), and also
   breaker-fail initiation, inter-trips and any outputs to other schemes (bus
   protection, SCADA alarms you don't want to send).
2. **Short the CT secondaries, then disconnect** the relay side. A proper test plug does
   this in the right order automatically; with links, short first, open second.
3. Open VT circuits to the relay if directional elements are involved, so you can't
   backfeed the VT.
4. Connect the test set to the relay side only. Double-check by measuring.

## 3. Test pickup and timing
- **Pickup:** ramp current slowly until the start/pickup flag; then ramp down to find
  drop-off. Both should be within the relay's stated tolerance.
- **Timing:** inject at several multiples of setting (commonly 2×, 5×, 10×, 20×) and
  compare measured time with the curve. For the IEC standard-inverse curve
  `t = TMS × 0.14 / ((I/Is)^0.02 − 1)`:
  at TMS 1.0, 2× gives about 10.0 s, 10× about 3.0 s. Scale by your TMS.
- **Instantaneous / high-set stage:** inject just below and just above (e.g. 0.9× and
  1.1×); check it doesn't operate below and operates fast above.
- **Earth fault:** repeat on the residual/earth input; check directional elements with
  the correct polarising voltage angle.
- Test each phase; a wrong-phase result often reveals a wiring fault, not a relay fault.

## 4. Primary checks (commissioning or after CT work)
Secondary injection doesn't prove the CTs. After CT work, primary injection or
on-load checks confirm **CT ratio, polarity and the relay seeing the right phase**.
Compare measured currents in the relay with a clamp meter or SCADA once on load.

## 5. Restore
Reverse the isolation in exact order: remove test leads, **restore CT connections
before removing shorts**, restore VTs, then trips last — and only after confirming
the relay shows no operated/latched trip output. Clear flags and LEDs. Check the
relay is healthy and measuring load correctly before declaring it back in service.

## 6. Fault-record analysis (after a real trip)
Download the disturbance record (often COMTRADE). Check: which phases saw fault
current, magnitude vs settings, which element tripped, time to trip, breaker clearing
time, and whether reclose behaved as expected. A trip that operated "correctly" on
wrong inputs is still a defect.

## Verify
- [ ] Present settings compared with approved settings before testing.
- [ ] Trips and inter-trips isolated; CTs shorted before disconnection.
- [ ] Pickup, drop-off and times within tolerance at each multiple and phase.
- [ ] Restoration done in reverse order; no CT ever opened under load.
- [ ] Relay healthy on load; test record signed and filed.
