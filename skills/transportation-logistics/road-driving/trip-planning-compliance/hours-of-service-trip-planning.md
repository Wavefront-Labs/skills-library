---
id: transportation-logistics.road-driving.trip-planning-compliance.hours-of-service-trip-planning
name: hours-of-service-trip-planning
category: transportation-logistics
field: road-driving
product: trip-planning-compliance
tags: [trip-planning-compliance, hours-of-service, hos, 11-hour-rule, 14-hour-rule, 30-minute-break, 60-70-hour-rule, 34-hour-restart, sleeper-berth-split, eu-drivers-hours, regulation-561-2006, 45-minute-break, daily-rest, weekly-rest, tachograph, fatigue-management, rest-stop-planning, truck-parking, delivery-windows, appointment-scheduling, trip-planner, fuel-stops, detention-time]
level: practitioner
status: verified
description: "Plan a commercial road trip inside hours-of-service rules: budget driving and duty time, place breaks and rests at real parking spots, sequence delivery windows, and manage fatigue."
sources: ["https://www.ecfr.gov/current/title-49/section-395.3","https://www.ecfr.gov/current/title-49/section-395.1","https://eur-lex.europa.eu/eli/reg/2006/561/oj"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hours-of-service trip planning

**Goal:** a trip plan that is legal on paper *and* realistic on the road — with breaks
where you can actually park, and buffer for the things that always happen.

*Summary of US FMCSA property-carrying rules (49 CFR 395.3, eCFR 2026-10-15) and EU Regulation
(EC) 561/2006 (EUR-Lex consolidated text). Planning heuristics below (speed factor, buffer, detention) are judgement, not rules. Exceptions (short-haul, adverse conditions,
agricultural, passenger carriers) change the numbers. Verify with current rules.*

## 1. Know your limits
**US (property-carrying), in summary:**
- **11 hours** driving, within a **14-hour** on-duty window, after **10 consecutive
  hours** off duty.
- **30-minute break:** driving is not permitted once more than 8 hours of driving time have passed without a
  consecutive 30-minute interruption (off duty, sleeper or on-duty not driving all count).
- **60/70 hours** on duty in 7/8 days; a **34-hour** off-duty restart resets it.
- Sleeper-berth split options (7/3 or 8/2: one period of at least 7 consecutive hours in the berth plus a
  shorter period, 395.1(g)) can pause the 14-hour window.

**EU, in summary:**
- **9 hours** daily driving (10 hours twice a week); **56 hours** weekly; **90 hours**
  in two consecutive weeks.
- **45-minute break** after 4.5 hours driving (can be split 15 + 30 in that order).
- **11 hours** daily rest (reducible to 9 hours at most 3 times between weekly rests; or taken as
  3 h + 9 h); regular weekly rest 45 hours (reduced weekly rest of at least 24 hours, with compensation).

## 2. Build the plan
1. **Fixed points first:** pickup and delivery appointments, ferry/tunnel slots,
   opening hours, required rest periods.
2. **Driving time:** route distance ÷ realistic average speed for the vehicle (trucks:
   often ~70–80% of the speed limit average on mixed routes, much lower in cities).
   Use a truck routing tool for restrictions.
3. **Add on-duty non-driving time:** pre-trip inspection, loading/unloading,
   fuelling, paperwork, and **detention** (waiting at shippers — budget 1–2 hours
   unless you know the site).
4. **Place breaks and rests at real locations:** truck stops, services, secure parks.
   Truck parking fills in the evening — plan to arrive earlier or reserve.
5. **Buffer:** at least 10–15% of driving time, or one hour per day, for traffic and
   weather.
6. Check the plan against **both** daily window and weekly totals.

## 3. Worked example (US)
Start 06:00 after 10 h off. Load 06:30–08:00 (on duty). Drive 08:00–14:00 (6 h).
30-min break 14:00–14:30. Drive 14:30–19:00 (4.5 h, 10.5 h total). Window ends 20:00
(14 h from 06:00). Park by 19:00 at a pre-chosen truck stop → 30 minutes' buffer for
parking, legal margin on both the 11 h and 14 h limits.

## 4. When the day goes wrong
- Delays at a shipper eat the 14-hour window, not the 11 hours: re-plan the
  remaining drive the moment you're delayed.
- Never "make up" time by skipping breaks. Inform dispatch early that an appointment
  will be missed.
- Adverse-driving exceptions exist in both regimes but are narrow — know them before
  relying on them.

## 5. Fatigue — the rules are a ceiling, not a target
- Body-clock low points: roughly 02:00–06:00 and mid-afternoon.
- Warning signs: heavy eyes, yawning, drifting, missed signs. Stop and rest — a
  short nap may help short-term, but only sleep fixes fatigue.
- Sleep quality matters: screen sleep apnoea if snoring/daytime sleepiness.

## Gotchas
- Planning with car travel times from consumer maps.
- Forgetting the last part of the trip still needs parking for the next rest.
- EU: ferry/train crossings have specific rest-interruption rules.

## Verify
- [ ] Plan checked against daily window, driving limit, break rule and weekly totals.
- [ ] Every break and rest placed at a named parking location.
- [ ] Buffer included; detention time budgeted.
- [ ] Actual logs compared with the plan after the trip.
