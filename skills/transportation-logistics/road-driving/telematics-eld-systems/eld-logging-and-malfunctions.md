---
id: transportation-logistics.road-driving.telematics-eld-systems.eld-logging-and-malfunctions
name: eld-logging-and-malfunctions
category: transportation-logistics
field: road-driving
product: telematics-eld-systems
tags: [telematics-eld-systems, eld, electronic-logging-device, aobrd, hours-of-service, hos, duty-status, on-duty, off-duty, sleeper-berth, personal-conveyance, yard-move, unassigned-driving, log-edits, annotations, eld-malfunction, data-transfer, roadside-inspection, dvir, telematics, fleet-tracking, geofence, driver-scorecard, samsara, motive, geotab, tachograph]
level: practitioner
status: docs-checked
description: "Use an ELD correctly as driver or fleet admin: duty statuses, personal conveyance and yard moves, unassigned driving, edits, roadside data transfer, and ELD malfunction procedure."
sources: ["https://www.ecfr.gov/current/title-49/section-395.34", "https://www.ecfr.gov/current/title-49/section-395.8", "https://www.fmcsa.dot.gov/hours-service/elds/electronic-logging-devices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ELD logging and malfunctions

**Goal:** logs that are accurate, defensible at a roadside inspection, and compliant
even when the device fails.

*Draft: written to the US FMCSA ELD rule (49 CFR Part 395); vendor apps (Samsara,
Motive, Geotab partners, etc.) differ in screens. EU/UK drivers use digital
tachographs with different rules — the principles of accuracy and annotation carry
over. Check the current regulation text and your carrier's policy.*

## 1. Duty statuses
- **Off duty**, **Sleeper berth**, **Driving** (set automatically when the vehicle
  moves above the device's threshold speed), **On duty not driving** (loading,
  fuelling, inspections, paperwork).
- Change status as it happens — not at the end of the day from memory.
- Log pre-trip inspection time as on-duty (ON status, 49 CFR 395.8(b)); inspectors notice 0-minute pre-trips.

## 2. Special driving categories
- **Personal conveyance (PC):** using the truck as personal transport while off duty
  (e.g. from shipper to a nearby rest location). Only if your carrier allows it, the
  movement is genuinely personal, and you are relieved from work. Add an annotation
  saying why.
- **Yard moves:** movement within a yard/terminal; select the yard-move status so
  driving time isn't logged incorrectly. Don't use it on public roads.
- Misusing PC or yard move is a common violation finding.

## 3. Unassigned driving
- When the truck moves with no driver logged in, the ELD records **unassigned driving**.
- Drivers: at login, review unassigned events for that truck and accept those that
  were you.
- Fleet admins: review the unassigned log daily; assign to the right driver or
  annotate why (e.g. mechanic test drive). Leaving it unresolved is a compliance gap.

## 4. Edits and annotations
- Drivers can propose edits to non-driving time with an annotation; automatically
  recorded driving time can't simply be deleted.
- Carrier-proposed edits must be accepted by the driver.
- Write useful annotations: "Waiting at dock — on duty", "Detour due to road closure".
- **Certify** each day's log.

## 5. Roadside inspection
- Know how to show the log on the screen *and* how to transfer it (telematics/web
  services or email; USB/Bluetooth on some devices). Keep the in-cab **instruction
  sheet**: user manual, data-transfer instructions, malfunction instructions, and a
  supply of blank paper logs (carrying a blank supply is the standard practice; 49 CFR 395.8(k)(2) requires the driver to keep the previous 7 days of records available).
- Hand the inspector the device or display per their request; don't hand over your
  personal phone unlocked unless required.

## 6. Malfunctions
If the ELD fails (malfunction indicator or the device is dead), the US rule's driver
duties are, in summary:
1. Note the malfunction and give the carrier **written notice within 24 hours** (49 CFR 395.34).
2. **Reconstruct the current day and the past 7 days** of logs on paper (or another
   approved method) unless retrievable.
3. Keep paper logs until the ELD is repaired.
The carrier must repair or replace it within 8 days of discovering the problem or of the driver notice, whichever is first; for more time it must ask the FMCSA Division Administrator within 5 days after the driver notice (49 CFR 395.34). *Confirm current text of §395.34.*

## 7. Telematics beyond logs
Fleet dashboards also track location, geofences (arrival/departure at sites), harsh
events and fault codes. Use driver scorecards as coaching data — review events with
video where available before drawing conclusions.

## Gotchas
- Forgetting to log out: the next driver's driving lands on your log.
- Device in driving mode when stopped in traffic — it only switches to on-duty when
  you change it after stopping.
- Mobile-based ELDs: phone battery or mount failures count as malfunctions too.

## Verify
- [ ] Every day certified; no unexplained gaps.
- [ ] Unassigned driving reviewed and resolved daily.
- [ ] PC and yard move uses are annotated and legitimate.
- [ ] Instruction sheet and blank paper logs in the cab.

## Checked

Jurisdiction: United States, FMCSA 49 CFR Part 395. Checked 2026-10-25 against current eCFR: 395.34 (written notice within 24 hours; reconstruct current 24-hour period and prior 7 consecutive days; carrier repair within 8 days; extension request within 5 days to the Division Administrator), 395.8(b) (four duty statuses) and 395.8(k)(2) (previous 7 days of records). Corrected: the draft implied an 8-day paper-log supply requirement and a looser repair period.

Method: documentation only; no commands were run.
