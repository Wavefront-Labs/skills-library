---
id: transportation-logistics.spaceflight-spacecraft-operations.mission-control-systems.telemetry-limits-and-safe-command-uplink
name: telemetry-limits-and-safe-command-uplink
category: transportation-logistics
field: spaceflight-spacecraft-operations
product: mission-control-systems
tags: [mission-control, ground-segment, ground-control-software, openc3, cosmos, yamcs, itos, scos-2000, telemetry, telecommand, command-uplink, limits, red-limits, yellow-limits, pass-automation, procedures, scripting, ccsds, ground-station, pass-planning, critical-commands, two-step-commanding]
level: practitioner
status: draft
description: "Setting telemetry limits, building scripted command procedures with verification (OpenC3 COSMOS/Yamcs-style), two-step critical commands and automated pass plans in satellite ground software."
sources: ["OpenC3 COSMOS documentation (docs.openc3.com)", "Yamcs documentation (docs.yamcs.org)", "CCSDS 232.0-B TC Space Data Link Protocol"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Telemetry limits and safe command uplink

**Goal:** see problems in telemetry the moment they appear, and send commands that
can't be sent by accident, in the wrong mode, or without checking they worked.
Examples use OpenC3 COSMOS syntax (open source, widely used for small missions);
Yamcs, ITOS and SCOS-2000 have equivalent concepts.

## 1. Telemetry limits
- Define **four limits per analogue point**: red-low, yellow-low, yellow-high,
  red-high. Yellow = act this pass; red = act now / procedure.
- Derive values from the qualification range, not from first-week flight data —
  then tighten yellows once you know the flight trend.
- Use **limit sets per mode** (eclipse vs. sun, safe mode vs. nominal) — a heater
  temperature that's fine in sun may be alarming in eclipse.
- Add **staleness** checks: a value that stops updating is worse than one out of
  limits. Alarm on packet age, not just value.
- Persistence: require N consecutive samples out of limits before alarming noisy
  points; never on safety-critical ones.
COSMOS definition fragment:
```
TELEMETRY EPS HK BIG_ENDIAN "EPS housekeeping"
  APPEND_ITEM BATT_V 16 UINT "Battery voltage"
    POLY_READ_CONVERSION 0 0.001
    UNITS Volts V
    LIMITS DEFAULT 3 ENABLED 24.0 25.5 33.0 34.0
```
(`LIMITS <set> <persistence> <state> red_low yellow_low yellow_high red_high`.)

## 2. Scripted procedures with verification
Never send a command without checking its effect. Pattern:
```ruby
# preconditions
check("EPS HK MODE == 'NOMINAL'")
check("EPS HK BATT_V > 26.0")
# command
cmd("EPS HEATER_SET with ZONE 2, STATE 'ON'")
# verification: command counter and effect
wait_check("EPS HK CMD_ACPT_CNT > #{start_cnt}", 10)
wait_check("EPS HK HTR2_STATE == 'ON'", 30)
```
- Check the **command-accept counter** and the **command-reject counter** — an
  accepted-but-rejected-by-the-flight-software command is common.
- Put timeouts on every wait; a hung procedure during a short pass is a lost pass.

## 3. Critical (hazardous) commands
- Mark in the command database as hazardous (COSMOS: `HAZARDOUS` keyword) so the GUI
  asks for confirmation.
- Use **arm-then-fire** two-step commanding onboard for anything irreversible
  (deployments, propulsion valve opens, safe-mode exit, software uploads).
- Require a **second operator verbal Go** and log it; for constellations, prevent
  sending to the wrong spacecraft by binding procedures to a spacecraft ID check.

## 4. Pass automation
1. Build pass schedules from predicted AOS/LOS (ground-station contact plans).
2. Each pass: auto-dump housekeeping and stored telemetry, run limit checks, uplink
   the pre-approved time-tagged command load, verify, close out.
3. Anything out-of-limits or a failed verification pages an on-call operator rather
   than retrying blindly.
4. Keep manual override and a "stop all scripts" control on every console.

## Gotchas
- Time-tagged commands use spacecraft time — verify clock correlation before loading.
- Database version mismatch between ground and flight software silently decodes
  telemetry wrongly; version the command/telemetry DB with the flight build.
- Uplink encryption/authentication counters (if used) can desync; know the recovery
  procedure before you need it.
- *COSMOS syntax shown is from v5/OpenC3; older Ball COSMOS 4 differs slightly.*

## Verify
- [ ] Every analogue point has red and yellow limits, and mode-specific sets where needed.
- [ ] Staleness alarms exist for each telemetry packet.
- [ ] Every procedure step that commands has a precondition check and a verification wait with timeout.
- [ ] Hazardous commands require confirmation and arm/fire.
- [ ] A dry run against a simulator passes before first use in flight.
