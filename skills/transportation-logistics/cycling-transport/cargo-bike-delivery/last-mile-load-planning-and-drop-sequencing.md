---
id: transportation-logistics.cycling-transport.cargo-bike-delivery.last-mile-load-planning-and-drop-sequencing
name: last-mile-load-planning-and-drop-sequencing
category: transportation-logistics
field: cycling-transport
product: cargo-bike-delivery
tags: [cycling-transport, cargo-bike-delivery, last-mile, last-mile-delivery, urban-logistics, micro-hub, micro-depot, consolidation, load-planning, drop-sequencing, route-planning, stop-density, parcel-delivery, lifo, load-order, cargo-box, trailer, weather-proofing, waterproofing, cold-chain, failed-delivery, proof-of-delivery, e-cargo-bike, dpd, ups, routing-software, delivery-round]
level: practitioner
status: draft
description: "Run cargo-bike last-mile rounds: size loads to the box, load in reverse drop order, sequence stops, work from micro-hubs, and keep parcels dry and intact."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Last-mile load planning and drop sequencing (cargo-bike delivery)

**Goal:** a round where every parcel fits, comes out of the box in the order you need
it, stays dry, and the bike returns to the hub empty and on time.

> Draft: general practice for e-cargo-bike parcel and grocery rounds from a micro-hub.
> Productivity figures are rough illustrations; company systems (routing software,
> scanners) differ.

## 1. Size the round
- Constraints: **volume** (box capacity, e.g. ~1–2 m³ for a large e-cargo trike or
  trailer), **payload** (often 100–250 kg on trikes, much less on two-wheelers),
  **battery range**, and **time** (shift length, delivery windows).
- Typical cargo-bike productivity in dense cores is often quoted at **~10–15+ stops per
  hour** when drops are close together — less in sprawl, more with locker drops.
  Measure your own.
- Reject or split oversized items before loading (long, heavy, fragile) — a single
  bulky item can block access to everything else.

## 2. Load in reverse drop order (LIFO)
1. Print or view the **sequenced manifest**.
2. **Last drops go in first, at the back/bottom**; first drops on top or nearest the
   opening.
3. Group by **zone/street**, not individually, so one opening of the box serves a cluster.
4. Heavy items low and central (stability); fragile on top, never under heavy items.
5. Use crates, dividers or labelled bags per zone; you shouldn't need to dig.
6. Scan every item as loaded; the count must match the manifest before leaving.

## 3. Sequencing drops
- Start with the **time-windowed** deliveries (e.g. 09:00–11:00, signature-required
  businesses before lunch closures).
- Then a loop that avoids crossing your own path and minimises left/right-across-traffic
  turns at busy junctions.
- Park once, deliver many: in dense blocks, park the bike securely and walk 2–5 drops.
- Use routing software's sequence as a starting point, then adjust with local knowledge
  (one-way streets, bike lanes, pedestrian zones, loading bays).

## 4. Micro-hub workflow
- Hubs are **consolidation points** (container, small depot, van parked as a mobile hub)
  fed by trucks/vans.
- Typical pattern: morning load → round 1 → return, swap battery, reload → round 2.
- Keep the hub tidy by zone and round; label shelves; batteries on chargers in a
  safe area.
- Returns and failed deliveries come back to the hub and are logged immediately.

## 5. Weather-proofing and cargo care
- **Waterproof box** with a closing lid; check seals. Use liners or bags inside for
  paper and electronics.
- In heavy rain, keep the lid closed between drops; a quick-access front flap reduces
  open time.
- Temperature-sensitive goods (groceries, pharma): insulated boxes, cool packs, and
  a maximum time out of the chain; deliver them first.
- Secure with straps or nets; trikes on rough cobbles shake parcels apart.

## 6. At the drop and after
- Proof of delivery per company rules (signature, photo, PIN, safe-place).
- **Failed delivery**: card/notification, correct status in the scanner — don't scan
  "delivered" to save a trip.
- Record anomalies (damage, wrong address) at the time; it saves disputes.

## 7. Gotchas
- Volume runs out before weight: plan by box space for light bulky parcels.
- Leaving the bike unlocked "for 30 seconds" in a busy street invites theft of parcels;
  lock the box, not just the bike.
- Battery range drops sharply with heavy loads in cold weather — carry a spare on long
  rounds.

## Verify
- [ ] Round fits box volume, payload and battery range.
- [ ] Items were loaded in reverse drop order and grouped by zone.
- [ ] Time-windowed and temperature-sensitive drops come first.
- [ ] Loaded count matched the manifest before departure.
- [ ] Every drop has POD and every failure has the correct status.
