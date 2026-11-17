---
id: hospitality-culinary.amusement-and-attraction-operations.queue-and-capacity-management.hourly-capacity-and-wait-time-estimation
name: hourly-capacity-and-wait-time-estimation
category: hospitality-culinary
field: amusement-and-attraction-operations
product: queue-and-capacity-management
tags: [queue-and-capacity-management, queue-management, queueing, hourly-capacity, thrc, ohrc, theoretical-hourly-ride-capacity, throughput, dispatch-interval, wait-time, posted-wait-time, littles-law, merge-point, merge-ratio, virtual-queue, fastpass, lightning-lane, express-pass, single-rider, queue-design, switchbacks, capacity-planning, theme-park, attraction-operations]
level: practitioner
status: draft
description: "Attraction throughput maths: theoretical vs operational hourly capacity, posting honest wait times, merge-point ratios for priority and virtual queues, and capacity planning."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hourly capacity and wait-time estimation

**Goal:** know how many guests an attraction really moves per hour, post wait times guests
can trust, and set merge ratios so priority and virtual queues don't starve the standby line.

## 1. Capacity
**Theoretical hourly ride capacity (THRC):**

`THRC = (3600 / dispatch interval in seconds) × seats per dispatch`

Example: a coaster with 24-seat trains on a 45 s interval → 80 dispatches × 24 = **1,920 pph**.
Shows/theatres: `seats × shows per hour`.

**Operational hourly ride capacity (OHRC)** is what you actually achieve — lower due to
empty seats, slow loading, downtime, fewer vehicles running:

`OHRC = riders counted in the hour` (from turnstile/dispatch counters)

The ratio OHRC/THRC (often 70–90 %) is your **efficiency**. Track it per hour and per crew.
Levers: run all vehicles/trains, fill seats (grouper skill, single-rider line), keep
dispatch intervals steady, cut downtime.

## 2. Wait time
Little's law: **wait (min) ≈ guests in queue ÷ throughput per minute**.
- Count the queue: place **markers** at known positions ("people from here = 300") or use a
  timed card: hand a guest a card at the queue entrance, collect it at load, record the
  real wait. Many parks run timed cards every 30–60 min to calibrate posted times.
- Example: 900 people in queue, OHRC 1,500 pph (25/min) → ~36 min.
- **Priority/virtual merges reduce standby throughput.** If half the seats go to the
  express line, standby moves at half the rate — recalculate.
- Rounding: post in 5-minute steps; many operators **slightly overstate** posted waits so
  guests are pleasantly surprised. Large deliberate inflation erodes trust.
  *Uncertain: policy varies by park.*

## 3. Merge points
Where two lines meet (standby + priority/virtual/single rider), the **merge ratio** controls who boards:
- Set ratio from expected return volume: e.g. if 30 % of capacity is sold/allocated to
  priority, merge roughly 3 priority : 7 standby.
- Merge staff count batches (e.g. "4 from priority, then 10 from standby") and adjust when
  the priority line empties or overflows.
- Virtual queue: guests get a return window; release only as many slots per window as
  your OHRC minus standby allocation can handle. Overbooking the return windows causes
  "virtual queue for a physical queue" complaints.
- Single-rider lines fill empty seats; they shouldn't consume standby throughput.

## 4. Queue design and management
- Switchbacks that can be opened/closed in sections so an empty queue isn't a long walk.
- Entertainment, shade, fans, and visible progress (queue moving) reduce perceived wait.
- Fixed "wait from here" signs at points of the queue.
- Close the queue in time for ride close: last guest at close should ride, but no one
  enters after the time when the queue can't clear.

## 5. Capacity planning
- Forecast attendance by day; estimate rides per guest per hour; compare demand vs total
  park OHRC. If demand exceeds supply, expect long waits — add entertainment capacity,
  extend hours, or open more vehicles/stations.
- Plan downtime response: if a headliner goes down, waits spike elsewhere — redeploy staff
  and update posted times quickly.

## Gotchas
- Using THRC to post waits makes every posted time too short.
- A ride running with one train fewer can lose 30–50 % of capacity.
- Not updating posted times after a breakdown is the top complaint driver.

## Verify
- [ ] THRC and actual OHRC known per attraction; efficiency tracked.
- [ ] Posted waits calibrated against timed cards at least every hour or two.
- [ ] Merge ratio matches allocated priority/virtual share and is adjusted live.
- [ ] Queue closure time set from throughput.
- [ ] Downtime triggers immediate posted-time updates.
