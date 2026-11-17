---
id: health-medicine.pharmacy.pharmacy-information-systems.automated-dispensing-cabinet-override-and-discrepancy-management
name: automated-dispensing-cabinet-override-and-discrepancy-management
category: health-medicine
field: pharmacy
product: pharmacy-information-systems
tags: [pharmacy-information-systems, pharmacy, automated-dispensing-cabinet, adc, pyxis, omnicell, profiled-cabinet, override, override-list, pharmacist-verification, discrepancy, count-discrepancy, controlled-substances, diversion, diversion-surveillance, blind-count, par-levels, restocking, barcode-restock, carousel, inventory-management, ismp-adc-guidelines, waste-witness, reporting-analytics]
level: practitioner
status: draft
description: "Run automated dispensing cabinets safely: profiled access, a tight override list, restock scanning, same-shift discrepancy resolution, and controlled-substance diversion surveillance."
sources: ["ISMP Guidelines for the Safe Use of Automated Dispensing Cabinets (2019)", "ASHP Guidelines on Preventing Diversion of Controlled Substances (2022)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated dispensing cabinet: overrides and discrepancy management

> General professional reference; vendor-neutral (Pyxis/BD, Omnicell and similar behave alike). Menu names, report names and default timers vary by vendor and version — confirm in your system. Override lists and thresholds are institutional decisions.

**Goal:** cabinets put medicines close to the patient; their safety depends on keeping the
pharmacist's prospective order review in the loop (profiling), keeping overrides rare and
justified, and resolving every count discrepancy before the trail goes cold.

## 1. Profile the cabinet
- **Profiled mode:** nurses can remove only medicines on a pharmacist-verified order for
  that patient. Non-profiled mode is for areas where it is genuinely impractical (OR,
  ED, procedural) and needs other controls.
- Stock only what the unit needs at sensible par levels; remove high-alert items that
  shouldn't be on the unit (e.g. concentrated electrolytes); use lidded/locked single-dose pockets for high-alert and controlled drugs.

## 2. Keep overrides rare and meaningful
- **Override list** (medicines removable before pharmacist review): only drugs where a
  delay would harm the patient — emergency drugs, reversal agents (naloxone, flumazenil,
  glucose), first doses in genuine urgency per policy. Review the list at least annually
  through P&T/medication safety.
- Each override requires a reason; pharmacy reviews **all overrides** retrospectively
  (daily report) to check that an order exists and was appropriate.
- Track override rate by unit and drug; a high rate means the list is too broad, orders
  are slow to be verified, or the cabinet is being used as a workaround.
- Speed up verification instead (pharmacist turnaround targets), so nurses don't need overrides.

## 3. Restocking and accuracy
- **Barcode-scan every item at restock** (and ideally at the carousel/pick station); a
  wrong-drug-in-pocket error is replicated for every patient who draws from it.
- Separate LASA items in different drawers; avoid adjacent pockets.
- Return bins: returned medicines go into a return bin, not back into a pocket.

## 4. Discrepancies (especially controlled substances)
- Use **blind counts** (user counts without seeing the expected number).
- A discrepancy must be **resolved by the end of the shift** by the people involved:
  check recent transactions, MAR, wastes, returns, other pockets, previous counts.
- Unresolved → escalate to the pharmacy/nurse manager per policy; document; for controlled
  drugs, investigate and report as the law requires (e.g. loss reporting in the US).
- Waste of partial controlled-substance doses needs a **witness** recorded in the cabinet
  at the time — not later.

## 5. Diversion surveillance
Run analytics reports and investigate outliers: a user's removals far above unit peers,
frequent wastes or cancelled transactions, removals for patients not assigned, removals
after discharge, unresolved discrepancies clustering on one user, PRN opioid removed but
not charted. Act through a diversion committee with HR, nursing and pharmacy.

## Gotchas
- Shared logins or witnessing without watching ("just sign my waste") defeat every control.
- Downtime: know the downtime procedure (critical-override key, paper records) and reconcile afterwards.
- Unit-dose packaging changes (new manufacturer) need the barcode/item file updated before stocking.
- Profiling off "temporarily" tends to stay off; audit the cabinet mode.

## Verify
- [ ] Cabinets profiled where feasible; non-profiled areas justified and controlled.
- [ ] Override list approved, short, and reviewed; all overrides reviewed daily.
- [ ] Every restock is barcode-scanned; LASA items separated.
- [ ] Discrepancies resolved the same shift; unresolved ones escalated and documented.
- [ ] Diversion reports run on schedule and outliers investigated.
