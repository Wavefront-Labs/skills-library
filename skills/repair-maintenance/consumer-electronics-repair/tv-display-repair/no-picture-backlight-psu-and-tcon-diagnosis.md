---
id: repair-maintenance.consumer-electronics-repair.tv-display-repair.no-picture-backlight-psu-and-tcon-diagnosis
name: no-picture-backlight-psu-and-tcon-diagnosis
category: repair-maintenance
field: consumer-electronics-repair
product: tv-display-repair
tags: [tv-display-repair, tv-repair, monitor-repair, lcd-tv, led-tv, backlight, led-strip, led-tester, backlight-driver, power-supply-board, smps, primary-capacitor, bulging-capacitor, t-con, tcon-board, mainboard, panel-assessment, lvds, v-by-one, standby-led, flashing-codes, flashlight-test, crt-safety, isolation-transformer, oled, mini-led]
level: practitioner
status: draft
description: "Diagnose TVs and monitors with no picture, dark screen or lines: split power supply, backlight, mainboard, T-con and panel faults, test LED strips, and work safely on mains boards."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TV and monitor no-picture diagnosis: PSU, backlight, T-con, panel

**Goal:** locate which of the four boards (power supply, mainboard, T-con, panel with
its backlight) has failed, using cheap observations first, and decide whether the
repair is worth doing before buying parts.

## 1. Safety first
- The power supply's **primary capacitor** (often 400–450 V rated, 50–150 µF) can stay
  charged after unplugging. Discharge it through a ~10 kΩ 5 W resistor with insulated
  leads and confirm 0 V with a meter before touching the PSU.
- Work on mains-live boards only with an **isolation transformer** and one hand in
  your pocket; a scope ground clip on the primary side without isolation creates a
  short through the earth.
- Backlight drivers output 60–200+ V DC on large TVs. Treat it as dangerous.
- **CRT sets:** the anode holds tens of kV for days. Discharge with a grounded
  screwdriver under the anode cap only if trained; otherwise do not open them.
- Lay the panel face-down on a soft, clean blanket; panels crack from twist, not weight.

## 2. Read the symptoms
| Symptom | First suspect |
|---|---|
| No standby LED, dead | PSU (fuse, primary side, standby supply) |
| Standby LED on, won't turn on / clicks | PSU main rails or mainboard |
| Sound and menus work, screen black | **Backlight** (LEDs or driver) |
| Picture faint when lit by a torch | Backlight confirmed |
| Picture on, then goes dark after seconds | Backlight protection tripping (one dead LED) |
| Lines, half-screen, colour inversion, ghosting | T-con or panel |
| Fixed vertical/horizontal lines at one position | Panel (COF/tab bond) — usually uneconomic |
| Boots, no inputs, logo loop | Mainboard / firmware |

Many TVs blink the standby LED in a code pattern; the service manual decodes it.

## 3. Backlight (most common)
1. Remove the back, the PSU/mainboard if needed, then the panel stack (bezel,
   panel, diffuser sheets) to expose the LED strips. Photograph sheet order.
2. Test each LED with an **LED/backlight tester** (adjustable 0–300 V, current-
   limited). A dead LED stays dark and breaks the whole series string; a dimmed or
   discoloured one is about to fail.
3. Replace the full strip set where possible (the others are the same age), not
   single LEDs. Re-stick any loose diffuser lenses (cups) over each LED with the
   right glue; missing lenses give bright spots.
4. Common cause is running at high brightness; some techs lower the driver current
   slightly. (Draft note: current-reduction resistor values are model-specific; not
   given here.)

## 4. Power supply
- Visual check: bulging/leaking electrolytics, burnt resistors, cracked solder on
  big parts. Replace bulged caps with the same capacitance, equal or higher voltage,
  105 °C low-ESR type.
- Measure output rails (commonly 12 V, 24 V, standby 5 V) with only the PSU
  connected; some need the PS_ON line pulled to standby voltage to start.
- Blown mains fuse = something shorted on the primary (MOSFET, bridge rectifier);
  never just replace the fuse and plug in. Use a **dim-bulb tester** (incandescent
  bulb in series) for first power-up.

## 5. T-con, mainboard and panel
- T-con: check its input voltage (often 12 V) and output gamma voltages; reseat or
  clean the LVDS / V-by-One cable and the fragile flat flex to the panel.
- Swap test is the fastest proof: a known-good board of the **same part number**
  (not just the same TV model; revisions differ).
- Panel faults (cracked glass, line defects from the COF bonding) are generally
  beyond economic repair — replacement panels cost close to a new TV.

## Gotchas
- Removing the panel incorrectly bends or tears the COF ribbons along its edge.
- OLED TVs have no backlight; "black screen" there is PSU, mainboard or panel.
- Some new supplies refuse to start without the backlight load; test with the
  strips connected.
- Never touch the panel's tab bonds with a hot iron.

## Verify
- [ ] Every LED lights evenly on the tester before reassembly.
- [ ] PSU rails within ±5 % of rated under load.
- [ ] Picture uniform on full white, black, red, green and blue test screens.
- [ ] Runs for at least 1 hour at normal brightness without shutting down.
- [ ] Diffuser sheets in original order; no dust, hot spots or clouding visible.
